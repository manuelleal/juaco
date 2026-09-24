# Bitácora de la nube — noche del 23→24-sep-2026

> Sesión en la nube (Claude Code, `session_01RQB2Z9Hj9yA4LEoLeUWGcA`), rama **`nube/noche-20260924`**. Encargo: `NUBE.md` §2b.
> Horas en **UTC** (Bogotá = UTC − 5). Esta bitácora reemplaza, para la nube, a `ESTADO.md`, `REGISTRO_etapas_1_2.md` y `HANDOFF.md`,
> que no se tocan porque el PC los está usando. Mañana el coordinador integra.
> Los candidatos a ERR llevan numeración provisional **nube-N**, para no chocar con los ERR que el PC numere esta noche (último conocido:
> ERR-121).

## 0. Arranque (01:39)
- `git pull` de main: `81dea3e`. La rama `nube/noche-20260924` sale de `origin/main`.
- `python --version` da **3.11.15**: la línea del PATH no está en `~/.bashrc`. O el Setup script no la corrió, o todavía no está puesto.
  El contenedor se reinició a las 01:37, pero `/root/venv-juaco` sigue ahí. Todo se corre con `/root/venv-juaco/bin/python`: 3.13.12,
  numpy 2.4.3, numba 0.67.0 y scipy 1.17.1.
- `manifiesto.py --check`: los 20 congelados están intactos.
- Pool = 3 para las series. El cuarto núcleo queda para arneses y para lo exploratorio, con un proceso a la vez.

## 1. Series (veredicto por la letra del preregistro)

### 1a. `subida_n10b` — la familia pasa su tabla en vida
- **01:41 — arnés** `identidad_familia_b.py` (070e6524f79e3cc4): **42/42** en 75 s (PC: 126 s). Salida idéntica a la del PC; el diff
  normaliza sólo CRLF, fechas y tiempos.
- **01:42 — serie 12701–12720**, lanzada con este comando:
  `/root/venv-juaco/bin/python experimentos/subida_n10b/corre_n10b.py --serie --desde 12701 --n 20 --pool 3`
  - `corre_n10b.py` b7808bbb83fb038e · `PREREGISTRO_n10b.md` 100f83f74446a973.
  - Log: `experimentos/subida_n10b/datos/n10b_serie_s12701-12720_T100000_20260924_014236.log`.
  - **02:29 — la serie terminó en 2796 s de pared, con Pool 3.**
    - JSON: `experimentos/subida_n10b/datos/n10b_serie_s12701-12720_T100000_20260924_014236.json` (eb3b800aa1e66437) y su crudo `.json.gz`.

    | carro | R0_nacidos (mediana) | vida de nacidos | gen_max |
    |---|---|---|---|
    | NADA | 0.114 | 99 | 3 |
    | RES | **0.688** | 466 | 23.5 |
    | RES1 | 0.400 | — | — |
    | BAR | 0.167 | — | — |
    | ORÁCULO | 0.520 | — | — |

    - Validez: V-ANCLA-b y V-TECHO-b pasan.
    - F-1 a F-5: **20/20 en cada una**, incluidas MIX (F-3 y F-4) y F-5, ACUMULA.
    - **VEREDICTO por la letra del §6: FUNCIONA + ACUMULA.**
  - **ALARMA DEL §8 ACTIVADA — no se lee todavía.**
    - El §8 del preregistro dice *"RES por encima del ORÁCULO en ≥ 15/20 sería sospechoso; revisar antes de leer"*. Aquí pasó en 20/20
      (0.688 contra 0.520).
    - Fuera de sus rangos predichos: P3 (RES en [0.25, 0.55]), P5 (brecha en [0.50, 1.00]; salió 1.46) y P9 (razón de vida en
      [1.4, 2.2]; salió 4.7).
    - El runner no aplica el chequeo del §8. Es candidato a **ERR nube-2**: el veredicto impreso no incluye una condición que el
      preregistro sí pone.
  - **Revisión en curso (exploratoria), hipótesis H-NEUTRAS.**
    - La tabla del ORÁCULO trae 8 entradas, 4 de ellas neutras (R = 0). Las de RES suelen estar incompletas: 6–7 claves; la completa
      aparece sólo en el 2–12 % de los casos.
    - Las entradas neutras entrenan a 0 el valor de una letra en una necesidad y borran la generalización protectora entre letras que
      comparten píxeles (D|sed = −3 generaliza a B).
    - Con sed, la boca del hijo del ORÁCULO vería B "neutro" y lo mordería.
    - Prueba: `revisa_n10b_oraculo.py` compara ORA_SIN0 (la tabla verdadera sin entradas neutras) con ORÁCULO, RES y NADA, en semillas
      de práctica 12794–12797.
  - **02:57 — la revisión de la alarma apoya H-NEUTRAS (exploratorio, 4/4 semillas de práctica 12794–12797).**
    - ORÁCULO sin sus 4 entradas neutras: 0.997.
    - ORÁCULO completo: 0.530.
    - RES: 0.714.
    - La alarma tiene causa mecánica (la verdad completa borra una generalización protectora), no de instrumento. Detalle en
      `experimentos/exploratorio_nube_20260924/NOTA_EXPLORATORIA.md`.
    - Consecuencia para la lectura de n10b: "techo" en V-TECHO-b y "brecha" no significan lo que el preregistro supuso. El veredicto por
      la letra (§6) no cambia; lo que cambia es la frase declarable, que decide el director.
  - **02:33 — réplica 12721–12740, lanzada con este comando:**
    `/root/venv-juaco/bin/python experimentos/subida_n10b/corre_n10b.py --serie --desde 12721 --n 20 --pool 3`
    - **03:20 — terminó.** JSON: `experimentos/subida_n10b/datos/n10b_serie_s12721-12740_T100000_20260924_022952.json` (cc285d187403ce11).

    | carro | R0_nacidos (mediana) |
    |---|---|
    | NADA | 0.122 |
    | RES | **0.737** |
    | RES1 | 0.382 |
    | BAR | 0.168 |
    | ORÁCULO | 0.545 |

    - Validez: V-ANCLA-b y V-TECHO-b pasan.
    - F-1 a F-5: 20/20.
    - **VEREDICTO por la letra: FUNCIONA + ACUMULA.**
    - Alarma del §8 otra vez: RES > ORÁCULO en 18/20. La explica H-NEUTRAS (exploratorio).
  - **n10b, por la letra: FUNCIONA + ACUMULA ×2** (serie y réplica, mismo veredicto).
    - Propuesta del preregistro (§11): +8 por FUNCIONA y +2 por ACUMULA en los niveles 10–13. Lo fija el director.
    - La frase declarable debe decir que el ORÁCULO de 8 entradas NO es un techo (H-NEUTRAS), y que ningún linaje se declara sostenido
      por esta serie. H-1 sigue en pie como medida del carro.

### 1b. JUACO-ECO (frente 2)
- **01:43 — arnés** `identidad_eco.py` (b70ec2f05915dc2e): **41/41** en 118 s (PC: 208 s). Salida idéntica a la del PC. Corrió en el
  núcleo libre mientras n10b usa los otros 3.
- **Observación, candidato a ERR nube-1 (menor, no bloquea):** el sha del runner en el preregistro no está al día.
  - El §0 de `PREREGISTRO_eco.md` cita `corre_eco.py` 0627f237b597523a.
  - El runner en main es 47d9cee4d6462116 (commit `bdb0aab`, 23-sep 19:51). Es el mismo que usó el humo `eco_humo_s19001_20260923_194831`,
    el que ejercita el juez actual (ERR-120).
  - La diferencia es la enmienda ERR-121 (P3c pasa a decidir), escrita antes de cualquier serie. El §0 no se actualizó.
  - La serie corre con el runner de main, y su log imprime el sha.
- **03:21 — prueba de la ruta del Pool** (sin valor por construcción).
  - Comando: `/root/venv-juaco/bin/python experimentos/juaco_eco/corre_eco.py --serie --prueba_pool --desde 19031 --n 2 --pool 2`.
  - Antes: `git diff` contra main de los originales de ECO, generaciones y carrera, vacío; `corre_eco.py` 47d9cee4d6462116.

- **03:23 — serie 19101–19120**, lanzada con este comando:
  `/root/venv-juaco/bin/python experimentos/juaco_eco/corre_eco.py --serie --desde 19101 --n 20 --pool 3`
  - Terminó a las 06:30 UTC, en 11 252 s de pared (80 trabajos con Pool 3). Salidas en
    `experimentos/juaco_eco/datos/eco_serie_s19101-19120/`.
  - Persisten tras el corte (vivos en T): **VIDA 16/20 · CEREBRO 17/20 · AZAR 11/20 · MUT0 0/20**.
  - P2: genes seleccionados en VIDA, fuera de sus 8 sombras con el mismo signo: **alpha 19/20 (+) y aversion 16/20 (+)**. AZAR no
    tiene falsos positivos (> 8/20 en ningún gen).
  - P3, juez: supervivencia mediana en la batería sellada 19201–19220, contra G0 (2219.5):
    - **VIDA gana 20/20** (mediana 9736);
    - CEREBRO gana 20/20 (9888);
    - AZAR gana 12/20 (2409).
  - P1 ✓, P1c ✓, P2 ✓, P3 ✓, H-c ✓. **P3c ✗ (AZAR 12/20 > 10/20)**. P4 ✗: VIDA − AZAR = 5 < 8.
  - **VEREDICTO POR LA LETRA: NO EVALUABLE.** Lo decide la enmienda ERR-121: si AZAR gana el juez en > 10/20, el juez no distingue
    selección de azar.
  - **Candidato a ERR nube-4 (serio, no se aplica; regla 11):** la condición de ERR-121 tiene el umbral en la mediana de la nula.
    - Bajo neutralidad, AZAR "gana" cada semilla con p ≈ 0.5, y entonces P(AZAR > 10/20) = **0.41**. El NO EVALUABLE salta casi por
      azar.
    - Aquí AZAR gana por poco (2409 contra 2219), mientras VIDA vive 4.4× lo de G0 en 20/20.
    - Propuesta para el director: un criterio nuevo, escrito ANTES de otra serie. Por ejemplo, P3c con umbral de cola (≤ 14/20,
      p < 0.05 bajo la nula) o la magnitud de VIDA contra AZAR. No se recalifica esta serie.
  - **Observación (no es criterio):** la selección en VIDA sube *alpha* (el peso del valor aprendido en la boca) y *aversion* (la
    fuerza del aprendizaje aversivo). Coincide con el diagnóstico exploratorio de esta noche: FABRICA muere porque el hambre le gana al
    valor en la boca (H-BOCA) y lo malo conocido por la vía lenta no pesa lo suficiente. La evolución encontró la misma perilla.
  - MUT0 = 0/20: sin mutación nadie persiste tras el corte. La mutación con vivero es necesaria; la selección suma (VIDA 16 contra
    AZAR 11), pero P4 pedía una diferencia de ≥ 8.
- **06:31 — réplica 19121–19140** lanzada con Pool 3 (mismo comando, `--desde 19121`). El bloque se declara sólo si serie y réplica
  dan el mismo veredicto; si no, vale el menor.
  - Terminó a las 09:38 UTC, en 11 301 s. Salidas en `experimentos/juaco_eco/datos/eco_serie_s19121-19140/`.
  - Persisten: **VIDA 18/20 · CEREBRO 18/20 · AZAR 14/20 · MUT0 0/20**.
  - P2: **alpha 20/20 (+)**.
  - P3, juez: **VIDA 20/20** (mediana 12 161 contra G0 2219.5, 5.5×); CEREBRO 20/20 (12 209); AZAR 15/20 (4559).
  - P1 ✓, P1c ✓, P2 ✓, P3 ✓, H-c ✓. **P3c ✗ (15/20)**. P4 ✗ (VIDA − AZAR = 4).
  - **VEREDICTO POR LA LETRA: NO EVALUABLE.**
- **BLOQUE ECO v1, por la letra: NO EVALUABLE ×2** (serie y réplica dan el mismo veredicto). No se declara selección.
  - **Qué se repite en las dos series, como dato y no como veredicto:**
    - sin mutación (MUT0) nadie persiste tras el corte;
    - con mutación y vivero persisten 16–18/20;
    - la selección sube alpha en 19–20/20;
    - los genomas del banco de VIDA viven 4.4–5.5× lo de G0 en la batería sellada, en 20/20.
  - **Candidato a ERR nube-6 (hipótesis, no medida): el juez compara una colonia DIVERSA contra una CLONAL.**
    - La colonia diversa son 9 entradas distintas del banco; la clonal, 9 copias de G0.
    - Si la diversidad sola alarga la supervivencia de la colonia, AZAR (deriva sin selección) le gana a G0 sin selección.
    - Control propuesto para un juez v2: comparar contra 9 entradas del banco de AZAR, o contra 9 mutantes de G0 sin selección.
    - Junto con nube-4 (umbral de P3c en la mediana de la nula), el juez de ECO v1 no puede decidir sobre la selección tal como está
      escrito. Se reescribe ANTES de ECO v2.
- **09:40 — ruta de Pool del gemelo verificada.**
  - `corre_eco_rapido.py --serie --prueba_pool --desde 19033 --n 2 --pool 2`: 8 trabajos en 2 s.
  - Después, el original con las mismas semillas: **10 JSON idénticos, 0 distintos**, sin contar los campos de tiempo y motor.
  - La carpeta del gemelo quedó como `datos/eco_prueba_pool_s19033_GEMELO`: se renombró, no se borró.
- **09:42 — ECO largo con el gemelo** (exploratorio por el preregistro: "SOLO tras la serie"; ya hubo serie y réplica). Comando:
  `/root/venv-juaco/bin/python experimentos/juaco_eco/corre_eco_rapido.py --largo --desde 19301 --n 3 --pool 3`
  - T = 1e6, corte en 100 000, brazos VIDA y AZAR, semillas 19301–19303.
  - En Python puro eran 3–32 h de CPU por corrida.
  - **09:45 — terminó: 14–27 s por corrida con el gemelo.** Salidas en `experimentos/juaco_eco/datos/eco_largo_s19301-19303/`.
  - Resultado (EXPLORATORIO, 3 semillas, sin veredicto por diseño):
    - **VIDA:** persisten 19301 (9 vivos en T) y 19302 (10 vivos); 19303 se extingue en t = 611 377.
    - **AZAR:** persiste 19302 (2 vivos); 19301 se extingue en 150 321 y 19303 en 310 816.
  - Lectura: linajes del bicho real (FABRICA con sus perillas evolucionadas) sobreviven 900 000 pasos DESPUÉS del corte, sin fundadores
    repuestos y con flujo fijo de comida, en 2/3 semillas (AZAR en 1/3). Es la primera pregunta del frente 2, pero sin juez válido
    (nube-4 y nube-6) y con 3 semillas. **Propuesta:** ECO v1.1 con juez v2 y horizonte 1e6 en 20 semillas más réplica. Con el gemelo
    cuesta minutos.

### 1c. `subida_n10c` — la familia pasa SÓLO LO QUE IMPORTA (paquete nuevo, decisión del coordinador; ver §3)
- **03:28 — preregistro escrito** (`experimentos/subida_n10c/PREREGISTRO_n10c.md`), a partir de lo exploratorio y ANTES del arnés.
  - Candidato: RES_SIN0.
  - Comparadores: RES, BAR_SIN0 (control de contenido que puede ganar), ORA_SIN0 (referencia), NADA y MIX.
  - Anclas: NADA [0.085, 0.135] y RES [0.60, 0.82].
  - Calificadores que NO son H-1: R0N-90 y PER-c.
  - Predicciones firmadas: FUNCIONA sin PERSISTE, lo más probable. P4 (S-1) 0.75, P5 (S-2) 0.90, P7 (R0N-90) 0.45, P8 (PER-c) 0.05.
- **03:32 — arnés** `identidad_n10c.py`: **16/16** (95 s).
  - Atrapó un bug de construcción antes del humo: `carros_n10c.base()` entraba en recursión tras reasignar `corre_n10b.carga`. Se corrigió
    cargando el carro por ruta. No es un cambio de criterio.
  - Sha fijado: `carros_n10c.py` 67f149c81f880cb1.
- **03:34 — humo** (práctica 12891, T 20 000): NADA 0.070 · RES 0.316 · RES_SIN0 0.875 · BAR_SIN0 0.828 · ORA_SIN0 1.12. No se lee.
  - Aviso: BAR_SIN0 alto en esta semilla, así que S-2 puede caer. Las predicciones NO se tocan tras el humo.
  - JSON: `experimentos/subida_n10c/datos/humo/n10c_humo_s12891_T20000_20260924_033423.json`.
- **~03:55 — auditoría (`juaco-auditor`, agente 2/2): LISTO PARA SERIE.** Hallazgos, todos BAJA y no bloqueantes:
  - H-1: `corre_n10b.agrega` calcula `_brecha_RES` con 'ORACULO'. Aquí no existe, así que sale None. Es inerte: el veredicto no la lee.
  - H-2: (D) no cubre ORA_SIN0. Es un filtro puro en `__init__`, sin rng, e (I) ya lo cubre con el filtro apagado.
  - H-3: no hay identidad dedicada para MIX. Es el mecanismo de n10b sin cambios; el humo separa bien las 3 claves.
  - H-4: la banda de RES [0.60, 0.82] es informal (dos series de n10b), no sale de un bootstrap. Sólo pesa en la validez.
  - H-5: BAR_SIN0 controla dosis, multiset y número de entradas. No puede distinguir "quitar lo neutro" de "quitar cualquier
    subconjunto de 4", porque en este mundo no hay otro subconjunto construible. Va a la frase declarable.
  - Verificó a mano: 12 shas contra los fijados, nada escrito tras el humo (sha y mtime) y semillas libres (grep en todo el repo).
  - Decisión: se corre la serie sin cambios. Los hallazgos van a la lectura, no al código: ninguno toca el criterio.
- **03:51 — serie 12801–12820 lanzada** con Pool 1, en el núcleo libre, en paralelo con ECO en Pool 3:
  `/root/venv-juaco/bin/python experimentos/subida_n10c/corre_n10c.py --serie --desde 12801 --n 20 --pool 1`
  - Decisión: Pool 1 en el núcleo libre, en vez de esperar a que termine ECO para correr con Pool 3.
  - Por qué: usa CPU que estaba ociosa y adelanta el veredicto ~4 h. La réplica va con Pool 3 al terminar la serie de ECO.
  - Costo aceptado: durante ~10 min se solapa con el final de la tanda exploratoria i3 (5 procesos en 4 núcleos). Sólo afecta los
    tiempos, no los resultados, que son deterministas.

- **06:52 — la serie 12801–12820 terminó** (Pool 1, 3.0 h).
  - JSON: `experimentos/subida_n10c/datos/n10c_serie_s12801-12820_T100000_20260924_035021.json` (ed080446ee64c3d3).

  | carro | R0_nacidos (mediana) | semillas ≥ 0.90 | persiste_carro | frac_mala_nacidos |
  |---|---|---|---|---|
  | NADA | 0.100 | 0 | 0/20 | 1.00 |
  | RES | 0.670 | 0 | 2/20 | 0.87 |
  | **RES_SIN0** | **0.950** | **19/20** | **17/20** | 0.57 |
  | BAR_SIN0 | 0.489 | 0 | 0/20 | 0.97 |
  | ORA_SIN0 | 0.987 | 20/20 | 7/20 | 0.60 |

  - Validez: V-ANCLA-c y V-RES-c pasan.
  - Puertas:
    - S-1: RES_SIN0 > RES, 20/20 (+0.28);
    - S-2: RES_SIN0 > BAR_SIN0, 20/20 (+0.46);
    - S-3: MIX, RES_SIN0 > NADA, 20/20;
    - S-4: MIX, RES_SIN0 > BAR_SIN0, 20/20.
  - Calificadores: R0N-90 en 19/20 y PER-c en 17/20.
  - **VEREDICTO POR LA LETRA: FUNCIONA + R0 DE NACIDOS ≥ 0.90 + PERSISTE.**
  - Predicciones:
    - se cumplieron P1, P2, P3, P4, P5 (S-2), P6 y P9;
    - P5, en su rango de BAR_SIN0, NO: 0.489 cae fuera de [0.03, 0.30];
    - P7 (R0N-90, p 0.45) se cumplió;
    - **P8 (PER-c, firmada con p 0.05) se cumplió contra mi predicción.**
  - **Lectura honesta de "PERSISTE", candidato a ERR nube-5:**
    - `persiste_carro` es "algún linaje sin fundadores tras t = 10 000". En las 17 semillas persiste **exactamente 1 de los 9 linajes**
      (`linajes_sin_ext` = 1). Los otros 8 se extinguen y se refundan: ~3400–3600 fundadores por corrida, igual que RES y ORA_SIN0.
    - Es la medida que **ERR-118 ya había marcado** ("mide cuánto les ganan los descendientes a los fundadores repuestos").
    - Usarla como PER-c fue un error de diseño del preregistro; el auditor tampoco lo vio. El veredicto por la letra no se cambia
      (regla 11).
    - Lo que NO se puede declarar: "la familia se sostiene" o "el linaje persiste". Lo que sí: "en 17/20 semillas uno de los 9 linajes
      de RES_SIN0 no se extingue tras t = 10 000 (RES 2/20, ORA_SIN0 7/20, NADA y BAR_SIN0 0/20)".
    - La comparación relativa es informativa: con la misma medida, RES_SIN0 supera a ORA_SIN0 (17 contra 7) aunque su R0 de nacidos sea
      menor. Hipótesis sin medir: la tabla propia hace linajes heterogéneos y uno gana la competencia por el flujo fijo.
  - **Lo que sí se sostiene por la letra, pendiente de réplica:** cuando la familia pasa sólo lo que le hizo bien o mal, el R0 de los
    nacidos sube de 0.67 a 0.95 (20/20), y con la misma tabla barajada no (0.49). La muerte por lo malo baja de 0.87 a 0.57.
- **06:53 — réplica 12821–12840 lanzada** con Pool 1, en el núcleo libre. La réplica de ECO ocupa el Pool 3.
  - **10:10 — terminó.** JSON: `experimentos/subida_n10c/datos/n10c_serie_s12821-12840_T100000_20260924_065441.json` (75263d554e211f74).

    | carro | R0_nacidos (mediana) | semillas ≥ 0.90 | persiste_carro |
    |---|---|---|---|
    | NADA | 0.109 | 0 | 0/20 |
    | RES | 0.774 | 0 | 5/20 |
    | **RES_SIN0** | **0.946** | **18/20** | **16/20** |
    | BAR_SIN0 | 0.539 | 0 | 0/20 |
    | ORA_SIN0 | 0.981 | 20/20 | 8/20 |

    - Validez: V-ANCLA-c y V-RES-c pasan. Puertas S-1..S-4 pasan.
    - **VEREDICTO POR LA LETRA: FUNCIONA + R0 DE NACIDOS ≥ 0.90 + PERSISTE**, el mismo que la serie.
    - `linajes_sin_ext` de RES_SIN0 por semilla: 0 en 4 semillas, 1 en 15, 2 en 1.
- **BLOQUE n10c, por la letra: FUNCIONA + R0 DE NACIDOS ≥ 0.90 + PERSISTE ×2** (serie y réplica, mismo veredicto).
  - **Frase declarable propuesta** (la decide el director): "en un mundo con flujo fijo de comida y generaciones que conviven, cuando la
    familia pasa en el parto sólo lo que le hizo bien o mal (sin lo neutro), los nacidos tienen más hijos que con la tabla completa y
    que con la misma tabla barajada, también compitiendo en el mismo mundo (20/20 ×2). El R0 de los nacidos llega a ≥ 0.90 en 19/20 y
    18/20 semillas".
  - **Límite, por ERR-118 y nube-5:** en 16–17/20 semillas, uno de los 9 linajes no se extingue tras t = 10 000. Los demás se refundan
    (~3500 fundadores por corrida). **No se declara "la familia se sostiene".**
  - **Puntos (propuesta del preregistro §11; decide el director):** FUNCIONA replicado +3 y R0N-90 replicado +2. PER-c replicado +5,
    pero se recomienda NO darlos por nube-5.

### 1d. Gemelo numba de ECO (compilador, agente 1/2) — entregado a las ~03:34
- **Arnés `identidad_eco_rapido.py`: 120/120** bit a bit en E1 (`eco=None`), E2 (genoma, mutación, banco, vivero y corte) y E3 (juez,
  checkpoints, `trabajo()` y `--reanuda` de `corre_eco`). Un proceso nuevo lee la caché y compila 0 funciones.
- **Aceleración:** ×38–41 en el mundo de ECO (esc 90, 74–81 cuerpos) y ×76 en la pista v2 (9 FABRICA). `trabajo()` pasa de 52.1 s a 1.2 s.
  ECO largo (1e6 pasos) quedaría en ~3 min con N = 100 y ~28 min con N = 1000.
- **Archivos:** `motor_eco_rapido.py` (edb8a15090b0f0dd), `corre_eco_rapido.py` (07bf5be9dc5d634a), `identidad_eco_rapido.py`
  (cb868264dec5004e), `identidad_eco_rapido_salida.txt` e `INFORME_eco_rapido.md`.
- **03:43 — verificado por el coordinador:** re-corrí `identidad_eco_rapido.py` y dio **120/120** (317 s). Las líneas de chequeo son las
  mismas que dio el compilador; sólo cambian los tiempos (×38–43 en ECO, ×59 en pista v2). Log:
  scratchpad → `identidad_eco_rapido_salida.txt` (la versión commiteada es la de esta corrida).
- **Falta:** la ruta con Pool del lanzador (`corre_eco_rapido.py --serie --prueba_pool …`) no se ejecutó.
- **La serie de ECO de esta noche sigue con el original:** sus checkpoints no se reanudan con el gemelo, porque la firma aborta.
- **Candidato a ERR nube-3 (del compilador; sin verificar):** los gemelos `organismo_f9_rapido.py` y `organismo_v13_rapido.py` usan
  `np.exp` dentro de numba, es decir libm.
  - En esta máquina (AVX-512), el `exp` de NumPy difiere del de libm en el 4.6 % de los argumentos.
  - Sus arneses comparan sólo salidas, así que pueden coincidir en la salida y diferir en los pesos.
  - Hay que revisarlos comparando pesos. Afecta la lectura de "gemelo v14 42/42" de la calibración.
  - **11:25 — premisa VERIFICADA por el coordinador** (numpy 2.4.3, numba 0.67.0, esta máquina): sobre 1 000 000 de argumentos al azar en
    [−30, 30], [−5, 5] y [−50, 0], el `np.exp` compilado por numba difiere del de NumPy en **4.62–4.65 %**, siempre por **1 ulp**. NumPy
    da lo mismo con arreglos de 2 elementos que con arreglos largos (el organismo usa arreglos de 2).
  - **Alcance:** en los gemelos viejos (`organismo_v13_rapido.py`, `organismo_v14_rapido.py`, `organismo_f9_rapido.py`) la sigmoide de
    la marcha y la de la boca pueden diferir en 1 ulp del original. Eso mueve en el último bit las trazas y los pesos MOTORES (Wl, el),
    que no se devuelven; los pesos de VALOR (Wp, Wn, Wps, Wns) sólo cambian si cambia una decisión, y una decisión cambia sólo si el
    sorteo cae a 1 ulp del umbral (del orden de 1e−16 por decisión). Los arneses de esos gemelos comparan salidas y siguen valiendo para
    salidas; "bit a bit" no vale para los pesos motores internos en esta máquina.
  - El gemelo de ECO (`motor_eco_rapido.py`) NO tiene el problema: llama al bucle de `np.exp` de NumPy por ctypes (su INFORME).
  - Propuesta para el PC (no se aplica): decir "bit a bit en la salida" en los informes de los gemelos viejos, o portarles el `exp` de
    NumPy en archivos nuevos. No cambia ningún veredicto registrado.

### 1e. ECO v1.1 — el mismo vivero con un juez que distingue selección de deriva (paquete nuevo, decisión del coordinador; ver §3)
- **Qué es:** ECO v1 sin tocar ningún archivo del PC, con dos cambios de INSTRUMENTO y ninguno de mecanismo:
  - **juez v2** (responde a nube-4 y nube-6): la colonia del banco de VIDA contra la del banco de AZAR de la MISMA semilla, en una batería
    sellada nueva (19501–19520); VIDA gana una semilla si su mediana es estrictamente mayor; P3 pide ≥ 15/20 (P = 0.021 bajo la nula);
  - **placebo** que calibra el juez: otra muestra de 9 del mismo banco (rng [s, 8]); vale si su puntaje queda en [5, 15] de 20;
  - **lectura larga** con el gemelo: cada corrida sigue hasta 1e6; el veredicto se lee en 120 000, como v1, y el bloque L en 1e6.
- **Dato visto antes de escribirlo (declarado en el preregistro):** con los JSON de v1, VIDA > AZAR pareado da 18/20 y 15/20. El umbral
  sale de la nula, no de ahí.
- **10:23 — arnés `identidad_eco_v11.py` (a674b0f689b6d5f7): 34/34.** (A) juez v2 con flujo 7 = juez de v1; (B) el placebo saca otros
  índices; (C) v1.1 con T = T_lect = v1 en sus 26 claves; (H) la dinámica no depende de T; (V) cada rama de la letra; (R) banderas.
  - Dos fallos del arnés antes de pasar, los dos del arnés o de la copia: (B) comparaba el contenido de las muestras (un banco corto
    repite genomas: 14 distintos de 157) y ahora compara índices; (C) halló que la copia había perdido la clave `tam_total` de v1.
- **10:25 — humo** (19601, 3.8 s) y **prueba del Pool** (19602–19603, 3.6 s): la letra corre y dice NO EVALUABLE, como debe con 1–2 semillas.
- **Commit df98831 (10:28): preregistro, runner (5655c93419511162) y arnés subidos ANTES de cualquier dato de v1.1.**
- **10:34 — gemelo re-verificado: 120/120** (`identidad_eco_rapido.py`, 316 s; salida en el scratchpad, la commiteada no se toca).
- **10:34 — serie 19401–19420** (`corre_eco_v11.py --serie --desde 19401 --n 20 --pool 3`): 80 corridas de 1e6 pasos en **5.5 min** de pared.
  - Persisten en 120 000: **VIDA 19/20 · CEREBRO 20/20 · AZAR 16/20 · MUT0 0/20**.
  - P2: **alpha 20/20 (+)** y **aversion 15/20 (+)** fuera de sus 8 sombras; AZAR sin falsos positivos.
  - **Juez v2: VIDA > AZAR 16/20** (sin empates); CEREBRO > AZAR 16/20. Medianas de supervivencia de la colonia: VIDA 11 624, AZAR 3 634.
  - **Placebo: VIDA 10.0, AZAR 9.0 de 20 → el juez v2 VALE.**
  - Descriptivo (nube-6): contra G0 (mediana 1 905.5) ganan VIDA 20/20 y **AZAR 15/20 sin selección**: la diversidad o la deriva sola
    le gana a G0, como sospechaba nube-6. El juez de v1 no podía separar eso.
  - P1 ✓ (19) · P1c ✓ (0) · P2 ✓ · P3 ✓ (16) · **P4 ✗ (19 − 16 = 3)** · H-c ✓ (20).
  - **VEREDICTO v1.1 POR LA LETRA (serie): HAY ALGO MODESTO.**
  - **Bloque L (1e6): VIDA 7/20 · CEREBRO 7/20 · AZAR 0/20 · MUT0 0/20.** L1 ✗ (7 < 10), L1c ✓, L2 ✓ (7 − 0 ≥ 6).
    **VEREDICTO L (serie): NO PERSISTE LARGO.** R0 de la cohorte nacida tras el corte en los linajes que persisten: 0.993 (VIDA) y 0.997
    (CEREBRO): viven en el filo, como un proceso de Galton–Watson crítico.
  - Perillas elegidas (mediana del banco en el corte, exponenciada): VIDA alpha ×1.60, aversion ×1.24, eta_s ×1.17; CEREBRO alpha ×1.61,
    aversion ×1.29, eta_s ×1.26. AZAR deriva sin dirección (rep_X ×0.76, dote ×0.87, …).
- **10:40 — réplica 19421–19440** lanzada con el mismo comando (`--desde 19421`).
  - Terminó a las 10:45 (5.4 min). Persisten en 120 000: **VIDA 20/20 · CEREBRO 18/20 · AZAR 11/20 · MUT0 0/20**.
  - P2: **alpha 20/20 (+)**, **aversion 16/20 (+)** y **tau_e 16/20 (−)**; AZAR sin falsos positivos.
  - **Juez v2: VIDA > AZAR 20/20**; CEREBRO > AZAR 20/20. Medianas VIDA 12 643, AZAR 3 812.5. **Placebo 10.5 y 9.0: VALE.**
  - Descriptivo: contra G0 ganan VIDA 20/20 y AZAR 17/20.
  - P1 ✓ (20) · P1c ✓ · P2 ✓ · P3 ✓ (20) · **P4 ✓ (20 − 11 = 9)** · H-c ✓ (18). **VEREDICTO v1.1 (réplica): FUNCIONA.**
  - Bloque L (1e6): **VIDA 5/20 · CEREBRO 11/20 · AZAR 0/20 · MUT0 0/20** → L1 ✗, L2 ✗ (5 < 6). **VEREDICTO L (réplica): NO PERSISTE LARGO.**
- **BLOQUE ECO v1.1, por la letra: HAY ALGO MODESTO ×2** (serie MODESTO, réplica FUNCIONA; si no coinciden vale el menor).
  - Lo que se sostiene en las dos, con el juez calibrado por el placebo: **la colonia de genomas que pasaron por la selección vive
    3.2–3.3× más que la de genomas que sólo derivaron** (medianas; 16/20 y 20/20 semillas), y la selección elige lo mismo en las dos (alpha ↑ 20/20 ×2,
    aversion ↑ 15–16/20). Es la primera vez en JUACO que un control de deriva válido separa la selección.
  - Lo que NO se sostiene: FUNCIONA exigía además P4 (VIDA − AZAR ≥ 8 en persistencia a 120 000), que cae en la serie (3) y pasa en la
    réplica (9).
  - **BLOQUE L, por la letra: NO PERSISTE LARGO ×2.** A 940 000 pasos del corte persisten VIDA 7 y 5 de 20, CEREBRO 7 y 11, AZAR 0 y 0.
    La selección sí distingue en el largo plazo (AZAR nunca persiste), pero los linajes seleccionados viven en el filo (R0 ≈ 0.99).
  - Vocabulario: "la colonia del banco de VIDA vive más que la de AZAR"; no "evoluciona", no "población" sin la medida.
  - Puntos: los de `PREREGISTRO_eco.md` §9; los decide el director (la nube no declara porcentajes).

### 1f. ECO v1.2 (selección + familia) y ECO-T (transferencia) — paquetes nuevos del frente 2
- **ECO v1.2** (`PREREGISTRO_eco_v12.md`, commit 060af2f, antes de cualquier serie): VIDA_T / AZAR_T / MUT0_T con el carro FAMB_RES0_ECO (la
  familia pasa su tabla sin neutras) y VIDA sin familia; T 1e6; juez v2 con placebo en una batería sellada nueva (19801–19820) con
  T_b 100 000. Arnés `identidad_eco_v12.py` 18/19 (falta (G): el gemelo del compilador). Humo Python: VIDA_T 43 cuerpos vivos a los
  12 000 pasos (máximo 189). **Sin el gemelo N/N no hay serie.**
- **ECO-T** (`transfiere/PREREGISTRO_transfiere.md`, commit 9ea2cc6, antes de la serie): los bancos del corte de ECO v1.1 en OTRO mundo, la
  carrera. Colonia de 9 genomas del banco de VIDA contra la del banco de AZAR y contra 9 × G0; placebo con otra muestra del mismo banco.
  T1: VIDA > AZAR ≥ 15/20; T2: VIDA > G0 ≥ 15/20. Arnés 14/14. **11:20 — ventana serie (bancos 19401–19420) lanzada con Pool 3.**
  - **11:57 — ventana serie, por la letra: TRANSFIERE.** R0 real en la carrera (mediana de las medianas de 9 líneas): **VIDA 0.275**,
    VIDA_P 0.272, **AZAR 0.153, G0 0.151**. T1 VIDA > AZAR **15/20** (justo en el umbral), T2 VIDA > G0 **20/20**; AZAR > G0 9/20 (la
    deriva sola no mejora a G0). **Placebo 9.0: vale.** Descriptivo curioso: líneas que persisten en T, VIDA 9, AZAR 16, G0 1 (de 180):
    los genomas derivados sostienen más líneas pero reproducen menos (a mirar en la réplica; no decide).
  - **11:58 — ventana réplica (bancos 19421–19440) lanzada.**
  - **12:35 — ventana réplica, por la letra: NO EVALUABLE.** El placebo (VIDA contra otra muestra del mismo banco) dio **16/20**, fuera
    de [5, 15] (bajo la nula pasa ~1 % de las veces). Descriptivo, igual que la serie: VIDA 0.300, VIDA_P 0.270, AZAR 0.143, G0 0.153;
    VIDA > AZAR 18/20, VIDA > G0 20/20, AZAR > G0 8/20; líneas que persisten VIDA 2, AZAR 18, G0 0.
  - **BLOQUE ECO-T, por la letra: NO EVALUABLE** (serie TRANSFIERE, réplica NO EVALUABLE; vale el menor). No se declara transferencia.
    - Lo que sí queda escrito como descriptivo de dos ventanas: los genomas seleccionados en ECO dan en la carrera ~0.29 de R0 real
      contra ~0.15 de la deriva y de G0, 40 de 40 semillas por encima de G0. El placebo que falló no es un defecto del criterio: es la
      comprobación que impide declarar con un juez que en esa ventana no quedó calibrado.
    - Si se quiere cerrar: una ventana nueva con bancos nuevos (los de ECO v1.2 o v2) y el mismo preregistro. No se corre hoy.

### 1g. ECO v2 — ÓRGANOS COMO GENES, en tres mundos a la vez (aprobado por el director ~11:35)
- **Instrumento Python** (`construye_eco_org.py`, por anclas): `motor_eco2.py` = motor_eco + dos genes de órgano al final del genoma
  (`ensena`: el padre pasa su tabla; `filtra0`: el hijo quita lo neutro), rasgos con umbral (se expresan si ≥ 1.0; nacen en 0.9,
  apagados; una mutación los prende con p ≈ 0.24); `carros/FAMB_ORG_ECO.py` lee los órganos del genoma de cada cuerpo.
  Arnés `identidad_eco_org.py` **9/9**: apagados = FABRICA_ECO; prendidos = FAMB_RES0_ECO; ensena sí y filtra0 no = FAMB_RES; la
  expresión sigue al gen; la mutación los prende (90 de 828 cuerpos en una corrida corta); checkpoint igual.
  - Un fallo del arnés antes de pasar, del instrumento: comparaba corridas con carros de nombre distinto, y el nombre va en el registro
    del linaje. Con la misma etiqueta en las dos corridas, la física es idéntica.
- **Preregistro `PREREGISTRO_eco_v2.md`** (commit befb71f, antes de cualquier serie): VIDA y AZAR en tres mundos (esc 30, 90 y 270),
  T 120 000, corte 60 000; O1 (ensena sobre sus sombras ≥ 15/20) y O2 (el banco de VIDA lo lleva más que el de AZAR ≥ 15/20) en ≥ 2 de 3
  mundos → FUNCIONA. Con auditoría propia de cinco riesgos (arrastre por alpha, deriva sobre el umbral, mundo chico, tope, el beneficio es
  del hijo). Semillas 20011–20030 y 20031–20050.
- Humo Python (w30, T 20 000): VIDA 24 % del banco con ensena y 5 de 6 vivos; AZAR 12 % (sin valor). Runner: arnés **15/16** (falta el gemelo).
- **11:40 — el gemelo de los órganos se le encarga al MISMO compilador** (mensaje al agente en curso: fase 2 tras la fase 1). Alternativa
  descartada: un agente nuevo (tendría que volver a leer todo; el que ya está conoce el gemelo de la familia).
- **12:20 — gemelos entregados por el compilador:** `motor_eco_rapido_fam.py` (132/132) y `motor_eco_rapido_org.py` (99/99), ×42–48
  (×32 en esc 270). Arneses de los runners con el gemelo, corridos por un agente Haiku (lo pidió el director): **v1.2 22/22, v2 21/21**
  (los preregistros decían 19 y 22: conté mal los casos; corregido con nota). Aviso del compilador: el juez de los arneses y de las pruebas
  del Pool tocaba las primeras semillas de la batería sellada con bancos de práctica; el arnés de v1.2 se pasó a práctica y queda el
  candidato **nube-7** (menor: no informa ningún resultado, rompe la letra de "sellada").
- **12:35 — serie 20011–20030** (`corre_eco_v2.py --serie --ventana serie --pool 3`), 15.5 min de pared:
  - w30: `ensena` sobre sombras en VIDA **15/20** (AZAR 5); banco con `ensena` VIDA 0.97 contra AZAR 0.31, VIDA > AZAR **16/20**;
    vivos en T con `ensena` VIDA 1.00 contra AZAR 0.00; persisten VIDA 19, AZAR 9 → **ELEGIDO**.
  - w90: sobre sombras **12/20**; banco 0.98 contra 0.41, VIDA > AZAR **19/20**; vivos 1.00 contra 0.18; alpha 15/20 (+).
  - w270: sobre sombras **13/20**; banco 0.99 contra 0.43, VIDA > AZAR **18/20**; vivos 0.99 contra 0.14; alpha 18/20 (+), tau_e 18/20 (−).
  - `filtra0`: no se selecciona (6, 7 y 10 de 20). Correlación alpha–ensena en el banco ≈ 0 (no hay arrastre por alpha).
  - **VEREDICTO POR LA LETRA (serie): HAY ALGO MODESTO** (O1 y O2 juntos en 1 mundo; alguno de los dos en los 3).
  - **Candidato nube-8 (instrumento, no se aplica):** O1 compara la MEDIA del gen en el banco con la de sus 8 sombras. Para un rasgo con
    umbral la selección sólo necesita pasar el umbral (el banco de VIDA se queda justo arriba de 1.0), mientras las sombras neutrales derivan
    libres y pueden quedar más arriba en promedio. Con el 98 % del banco y ~100 % de los vivos expresando el órgano, O1 da 12–13/20.
    La prueba adecuada es la fracción que EXPRESA el órgano contra la de las sombras (hoy el corte no guarda los genomas sombra por
    entrada). Para una v2.1: guardar las sombras del banco y medir la expresión.
- **12:52 — réplica 20031–20050 lanzada.**
  - Terminó a las 13:07 (15 min). w30: banco con `ensena` VIDA 0.90 contra AZAR 0.37, VIDA > AZAR 13/20; vivos en T 1.00 contra 0.13.
    w90: sombras 13/20, banco 0.98 contra 0.45, **VIDA > AZAR 20/20**, vivos 1.00 contra 0.00, alpha 17/20. **w270: sombras 17/20 y
    VIDA > AZAR 18/20 → los dos**, banco 0.99 contra 0.37, vivos 1.00 contra 0.50, alpha 20/20, tau_e 16/20 (−). `filtra0` no.
  - **VEREDICTO POR LA LETRA (réplica): HAY ALGO MODESTO.**
- **BLOQUE ECO v2, por la letra: HAY ALGO MODESTO ×2.** Lo que se sostiene en las dos: en los tres mundos el banco de VIDA expresa el
  órgano de enseñar en 90–99 % y los vivos al final en ~100 %, contra 31–45 % y 0–50 % en AZAR. La prueba contra sombras que pedía la letra
  (media del gen) queda corta en la mitad de los mundos por nube-8; ECO v2.1 repite la pregunta con la prueba de expresión (preregistrada a
  las 13:05, semillas nuevas).

### 1h. ECO v3 — los 7 órganos del Frankenstein como genes (preregistro `PREREGISTRO_eco_v3.md`, con ENMIENDA 1 antes de la serie)
- **Serie 20111–20130** (Python, Pool 3, 13:07–14:31; runner 7bb44da802508b37, arnés 14/14). Letra: ELEGIDO = la fracción del banco que
  EXPRESA el órgano supera a la media de sus 8 sombras (O1\*) en ≥ 15/20 **y** el banco de VIDA lo lleva más que el de AZAR (O2) en
  ≥ 15/20; "sube" = uno de los dos; FUNCIONA si algún órgano queda ELEGIDO en los dos mundos; MODESTO si ELEGIDO en uno o "sube" en los dos.
  - **w30:** `herencia` O1\* **19/20**, banco VIDA 0.975 contra AZAR 0.395, VIDA > AZAR **14/20** (a uno del umbral) → "sube".
    `curiosidad` 4/20 y `modelo` 2/20 por encima de sus sombras (debajo 16 y 18), VIDA < AZAR 18 y 16/20 → "baja". Resto neutro.
    Persisten en T: VIDA 18, AZAR 9.
  - **w9:** `interruptor` O1\* **17/20**, VIDA > AZAR 12/20 → "sube". `curiosidad` y `modelo` "baja" (5 y 4/20; VIDA < AZAR 19 y 20/20).
    Persisten en T: VIDA 0, AZAR 0 (el mundo de 9 fundadores se extingue en los dos brazos).
  - Guardias de AZAR vacías (ningún gen > 8/20 contra sombras por la media; su expresión sobre sombras ≤ 11/20, bajo el 15 de la
    ENMIENDA 1). Perillas seleccionadas sin órganos: ninguna en los dos mundos.
  - **VEREDICTO POR LA LETRA (serie): NO** (ningún órgano ELEGIDO; ninguno "sube" en los dos mundos). Los predichos (§4): herencia
    ELEGIDO en w30 (p 0.70) quedó a un punto de O2; interruptor "sube" en w9 como se predijo; curiosidad y modelo bajan en los dos mundos
    (predicho: neutros o descartados). DESCARTADO es descriptivo por la ENMIENDA 1.
  - Lectura (no se declara): la selección se queda con la herencia donde hay linajes que duran (w30) y tira curiosidad y modelo en los dos
    mundos, lo mismo que dijeron las ablaciones a mano del Frankenstein. La réplica 20131–20150 va en la cola.

## 2. Exploratorio — **EXPLORATORIO, no es dato**
Carpeta: `experimentos/exploratorio_nube_20260924/` (su `NOTA_EXPLORATORIA.md` manda). Aquí va sólo el resumen. Todo en la pista de
la carrera (9 carros iguales, fundador limpio), semillas exploratorias 24001–24099, con arneses de identidad bit a bit de cada subclase.
- **(i) Arriesgar según la reserva, sobre FABRICA (T 30 000):** la neofobia sola no ayuda; limpiar desde 1.4 rompe la ventana de parto;
  dejar de morder lo malo tapa el mundo. La regla completa con limpieza costeable (RESC) sube los linajes que persisten de 1/54 a 17/54
  (O1 20/54) sin mover el R0.
- **(i) sobre v14.3 (T 100 000):** la pieza que su creador propuso, *neofobia regulada por la reserva*, lo EMPEORA (R0 0.587 → 0.449,
  1/6; por linaje 0.420).
- **Familia y perillas de ECO sobre v14.3 (T 100 000):** nada lo mejora en la carrera (tabla de la familia −0.15/−0.19, nodo sin
  neutras ≈ 0, perillas de ECO −0.25, alpha ±). v14.3 está en un óptimo local respecto de lo probado. **Pero las perillas que eligió la
  selección en ECO mejoran a FABRICA en la carrera: 6/6, 0.147 → 0.269** (lo seleccionado en la pista v2 transfiere a la pista v1).
- **(ii) Aprender prediciendo lo que desaparece (T 30 000): negativo** (0.086 contra 0.116 de RES; 0/54 linajes persisten). La señal
  "lo que los otros comen" está contaminada: morder lo malo también lo quita.
- **Revisión de la alarma de n10b (T 100 000):** H-NEUTRAS se sostiene (ORA_SIN0 0.997, RES_SIN0 0.91–0.97) → paquete n10c (§1c).
- Lección de conjunto: las piezas no suman solas; dependen del mundo (la tabla sirve donde el hijo nace vacío y daña donde el linaje
  ya tiene memoria) y del resto del organismo (las perillas de ECO ayudan a FABRICA y le sobran a v14.3).

## 3. Decisiones del coordinador de la nube (hora, opción, alternativa descartada, porqué)
- **01:43 — el arnés de ECO corre ahora, en el núcleo libre, y no justo antes de su serie.**
  - Alternativa descartada: esperar a que termine n10b.
  - Por qué: ningún archivo de ECO se toca esta noche, y así un fallo aparece con horas de margen. Antes de lanzar la serie de ECO se
    vuelve a verificar el sha del runner.
- **01:45 — los candidatos a ERR se numeran como nube-N.** Así no chocan con el PC, que también numera esta noche.
- **03:37 — los checkpoints (`ckpt/*.pkl`) de la serie de ECO en curso dejan de versionarse.**
  - Qué se hizo: `git rm --cached` más la exclusión local en `.git/info/exclude`. Los archivos siguen en disco y en el commit 848df06.
  - Por qué: se reescriben cada 10 000 pasos, ocupan varios MB y versionarlos en cada push inflaría el repo.
  - Se suben sólo si la sesión va a cortarse, que es lo que pide el encargo. Los JSON de resultados sí se versionan.
  - **CORRECCIÓN, 09:50: esta decisión choca con la regla del director del 23-sep 22:20** (HANDOFF §15.33): *"no vayas a cambiar las
    cosas que están en github, ni retroceder en lo que estamos"*; en GitHub sólo se agrega. No la había leído: llegó a main durante la
    noche.
    - Sacar los 3 `.pkl` del árbol de la rama los quitó de GitHub, aunque sigan en el historial.
    - Se restauraron en su ruta desde 848df06, con `LEEME_ckpt.txt`: son intermedios y no sirven para reanudar, porque el runner borra
      cada checkpoint al terminar su trabajo.
    - Se retiró la exclusión local.
    - Desde ahora esta sesión no saca nada del árbol de GitHub, ni siquiera archivos efímeros.
- **03:40 — el auditor (agente 2/2) se usa ANTES de la serie de n10c y no al final.**
  - Alternativa descartada: auditar la bitácora al cierre.
  - Por qué: un fallo de diseño hallado antes de la serie ahorra CPU y evita un ERR. La bitácora queda para que la revise el
    coordinador en el PC.
- **02:24 — gemelo numba: se encarga a UN `juaco-compilador` (Opus), el agente 1 de los 2 que permite el presupuesto de la noche.**
  - Pedido del director (~02:10): *"sí, haz el gemelo numba hoy si puedes y sigue trabajando hasta mañana en la noche. Objetivo
    la AGI"*.
  - Objetivo del gemelo: ECO (mundo v2 de `motor_eco` + `FABRICA_ECO`), no la pista v1.
    - Por qué: ECO largo (1e6 pasos) y ECO a 10× y 100× son hoy inviables en Python (3–32 h de CPU por corrida). Es el paso 1 del
      frente 2.
    - La pista v1 (frente 1, v14.3) aguanta en Python: ~100 s por corrida con T = 100 000.
  - Etapas encargadas:
    - E1: mundo v2 con `eco=None` y FABRICA_ECO, bit a bit.
    - E2: genoma, mutación, banco, vivero y corte.
    - E3: juez y checkpoints.
  - Alternativa descartada: hacerlo yo. El trabajo de código pesado inflaría el contexto de la sesión, y cada llamada posterior
    costaría más.
  - Las series de esta noche (n10b, ECO v1) siguen con el instrumento en Python preregistrado. El gemelo sólo se usará tras su arnés
    N/N, para ECO largo y ECO v2.
  - La tanda exploratoria pasa a `nice 19`, para no quitarle CPU a las pruebas del compilador ni a las series.

- **10:12 — se detiene una espera colgada.** El lazo `until ! pgrep -f "tag ii1a"` de la tanda (ii) se encontraba a sí mismo en `pgrep`
  y no terminaba nunca; la tanda ya había acabado. Lección: esperar por PID o por el archivo de salida, no por `pgrep -f` de un texto que
  el propio lazo contiene.
- **10:15 — EXPLORATORIO: la pieza que el creador de v14.3 dejó propuesta.** Su INFORME (§"Qué queda") propone *"neofobia regulada por
  la reserva"* como lo que le falta a v14.3 para acercarse a O1. Es mi tema (i), así que la pruebo sobre V143 sin tocarlo (subclase
  cargada por ruta; identidad WV143 == V143 bit a bit) con dos definiciones de "desconocido": la del creador (por cuerpo) y otra por linaje.
  - Alternativa descartada: preregistrarla de una vez como paquete del frente 1. Sin una señal exploratoria sería gastar una serie.
- **10:20 — ECO v1.1 se escribe y se corre sin esperar respuesta del director** (le pregunté a las ~09:45; no contestó).
  - Por qué: la regla 12 da autonomía para criterios y siguiente paso, y el director avisó que no estaría dando sí o no. v1 quedó
    NO EVALUABLE ×2 por un juez mal calibrado; sin juez válido el frente 2 no puede contestar su segunda pregunta.
  - El veredicto de v1 no se recalifica. v1.1 son archivos nuevos, con semillas nuevas, y su criterio se subió antes de correr.
  - Se lee en 120 000 (como v1) para que el único cambio sea el juez; el horizonte de 1e6 va aparte, en el bloque L, con su letra.

- **10:50 — hallazgo de diseño para el frente 2: en la pista v2 (el mundo de ECO) el hijo nace SIN NADA del linaje.** El motor crea
  una instancia nueva del carro por cuerpo y FABRICA pasa `memoria=None` (hereda='nada'); el nodo de FABRICA, que en la carrera
  (pista v1) es la memoria del linaje porque el carro es uno por linaje, en ECO está siempre vacío. En ECO v1 y v1.1 la selección sólo
  pudo mover perillas, y aun así llevó el R0 tras el corte a 0.91–0.99. La pieza que n10c validó (la familia pasa su tabla SIN las
  entradas neutras) es exactamente lo que le falta ahí.
  - Construido por anclas `carros/FAMB_RES0_ECO.py` (`construye_eco_familia.py`, desde FAMB_RES de n10b, sha fijado): el `_see` de
    FABRICA_ECO + el filtro SIN0 de n10c. Arnés `identidad_eco_familia.py`: **7/7** (con SIN0 = 0 es FAMB_RES; con SIN0 = 1 es
    bit a bit el RES_SIN0 de n10c; checkpoint y reanudación iguales).
  - Humo de costo en Python (19601, VIDA, esc 90, T 12 000, corte 8 000): 60 µs por cuerpo y paso, igual que FABRICA_ECO, pero el
    linaje sostiene más cuerpos (115.8 contra 68.3 de media; 22 contra 4 vivos en T). Una serie en Python costaría ~6.5 h.
- **10:55 — se encarga al `juaco-compilador` (agente 1 del día, el del frente 2; NUBE.md §0: "uno por frente") el gemelo numba de
  FAMB_RES0_ECO**, en archivos NUEVOS (`motor_eco_rapido_fam.py` + arnés + informe; `motor_eco_rapido.py` no se toca).
  - Por qué: con el gemelo, ECO v1.2 (selección + familia) a 1e6 cuesta minutos; en Python, días. Es el paso 1 del frente 2 del plan
    del director ("primero el gemelo"), aplicado al carro que ahora importa.
  - Alternativa descartada: el gemelo de V143 para ECO. V143 en la pista v2 también nace sin memoria de linaje (sus piezas de linaje,
    nodo y opción TD, viven en el carro de la carrera); sin transmisión en el parto perdería justo lo que lo hace mejor.
  - Mientras tanto: preregistro de ECO v1.2 y tanda exploratoria del frente 1 (familia y perillas de ECO sobre V143).

- **11:15 — ECO-T se preregistra y corre mientras el compilador trabaja.** Tres núcleos libres. La tanda exploratoria mostró que las perillas
  de ECO transfieren a FABRICA en la carrera (6/6); en vez de declarar eso con perillas elegidas a mano, se prueba con los genomas enteros
  de los bancos y con la deriva como control (lo que ECO v1.1 dejó en disco). Es una pregunta del frente 2 (¿la selección produce algo
  que la deriva no?) medida fuera de su mundo. Alternativa descartada: esperar ocioso al gemelo.

- **13:25 — se repite el error de las 03:37 y se corrige igual.** Los commits parciales hechos DURANTE las series de ECO v2 (serie y réplica)
  y ECO v3 subieron checkpoints intermedios (`ckpt/*.pkl`), y el commit siguiente registró su borrado (el runner los borra al terminar
  cada trabajo): 9 archivos salieron del árbol. Para cumplir "en GitHub sólo se agrega" se restauraron los 9 desde el commit anterior a
  su borrado (con un `LEEME_ckpt.txt` en cada carpeta: no sirven para reanudar). Desde ahora: los checkpoints nuevos quedan fuera por
  exclusión local, y los que ya están en el árbol se congelan con `skip-worktree` para que su borrado en disco no llegue a GitHub.
  Lección: no hacer `git add` de una carpeta de datos con una serie corriendo; subir sólo los JSON terminados.

- **14:3x — el contenedor se reinició y la cola desatendida murió** justo después de subir ECO v3 serie (commit bc56cc8) y al empezar
  ECO v2.1 serie. Se relanzó (`cola_eco2.sh`, mismo orden) desde ECO v2.1 serie con `--reanuda` (el runner retoma lo terminado desde su
  checkpoint; los JSON ya escritos no se repiten). Antes de relanzar se subieron los JSON terminados y el log parcial (c47f12e, ef1c3ce).
  Alternativa descartada: repetir la serie desde cero (misma letra y mismas semillas, 10 min más de pared, sin ganancia).

## 3b. Pedidos del director durante la noche (sus palabras, para que no se pierdan)
- Prompt de la noche: `NUBE.md` §2b (en main).
- ~02:00, sobre el costo: *"Mientras tanto consume. ¿Muchos tokens las corridas o crees que alcancemos a algo significativo? ¿Cuándo pueden
  reducir los tiempos de corrida?"*
  - Respuesta: las corridas no gastan tokens; lo caro son las revisiones del coordinador. La palanca de tiempo es el gemelo numba.
- ~02:10: *"sí, haz el gemelo numba hoy si puedes y sigue trabajando hasta mañana en la noche. Objetivo la AGI"*. Se encargó al
  compilador (sección 3, 02:24).
- ~02:40: pide seguir intentándolo con el método, y que no se vuelva a mencionar la comparación con sus otras prioridades.
- ~02:45: *"avísame si ORA_SIN0 se sostiene y ¿crees que lleguemos a la evolución?"*
  - ORA_SIN0 se sostuvo 4/4 (exploratorio).
  - Respuesta sobre la evolución:
    - la adaptación por selección es alcanzable en semanas si los linajes persisten sin ayuda;
    - la evolución de la regla de aprendizaje es plausible con el gemelo y ECO v2;
    - la evolución abierta no se promete.
- ~03:00: *"no pierdas lo que te di, los .md… no dejes que se borren"*.
  - Verificado a las 03:00: main y esta rama tienen los mismos 358 `.md`, y ningún commit de los últimos 60 de main borra un `.md`.
  - Lo commiteado queda en el historial de GitHub aunque se borre del disco. La guardia bloquea `rm -r` de `registro/` y el push
    forzado.
  - En el contenedor no hay `.md` adjuntos fuera del repo. Si los `.md` estaban en otro chat, hay que volver a pasarlos y se guardan
    aquí al instante.

- ~11:25 UTC (24-sep), sobre ECO v1.1/v1.2: *"Si lo apruebo y además de eso pensar en llenar benchmark y que el bicho logre realmente la
  evolución! Proyecciones de evolución?"* → aprobación de la línea ECO (v1.1 ya corrida; v1.2 preregistrada). Respuesta con escalones de
  evolución medibles y su proyección en el chat; propuesta: que la selección elija la ARQUITECTURA (órganos como genes), no sólo perillas.

- ~11:35 UTC: *"sí, arranca ECO v2 con órganos como genes, pero la intención es que audites tú, manda agentes en modelos baratos cuando no
  necesites cosas expertas, réplica no construyas de 0 y yo sé que podemos lograrlo; otra cosa: no sólo dejes una muestra en el mundo, si
  puedes correr tres al tiempo con capacidades distintas aumentamos la cobertura de prueba. Y último: ten en cuenta la exploración, el
  camino escrito casi llega a su fin, queda comenzar a usar data sintética que hemos creado. ¡Confírmame!"*
  - Cómo se aplicó: ECO v2 con auditoría propia en el preregistro (§7) y sin agente auditor; agentes Haiku para tareas de rutina, Opus sólo
    para el gemelo; se construye por anclas sobre lo que ya existe; tres mundos de capacidad distinta en la misma serie.
  - Pedí confirmar qué "data sintética" quiere decir (en el repo no hay un conjunto con ese nombre; hay ~1 060 JSON de corridas).

- ~13:30 UTC: *"Quedan 100 dólares; la idea es lograr algo modesto pero real con eso, que de ahí sea más fácil evolucionarlo, y en su tesis
  ¿a qué llegamos? No hay data, es lo que tenéis, me refiero. ¿A qué hemos llegado, en humano? ¿Hay algo interesante?"*
  - Cómo se aplicó: se deja una COLA DESATENDIDA (un script que corre lo ya preregistrado, una serie a la vez, y sube cada resultado sin
    turnos del coordinador): ECO v3 serie → ECO v2.1 serie y réplica → ECO v3 réplica → ECO v1.2 serie y réplica. No se abre nada nuevo.
    El resultado "modesto pero real" que se busca asegurar es ECO v2.1 (la selección prende el órgano de enseñar). "La data" = lo que ya
    hay (bancos seleccionados, vidas, tablas).

## 4. Qué falló y qué propongo (borrador vivo; se completa al cierre)
**Qué falló o se corrigió (todo del instrumento o del coordinador):**
- El juez de ECO v1 no distinguía selección de deriva (nube-4: umbral en la mediana de la nula; nube-6: colonia diversa contra clonal).
  Se reescribió con placebo en v1.1 y ahora sí separa (16/20 y 20/20 con placebo válido).
- Sacar checkpoints del árbol (03:37) violaba "en GitHub sólo se agrega"; se restauraron.
- Una espera con `pgrep -f` se encontraba a sí misma y no terminaba.
- Arneses que al principio comparaban mal (contenido en vez de índices; carros de nombre distinto; una clave perdida en una copia):
  los tres se hallaron ANTES de correr, que es para lo que están.
- Candidato nube-3 verificado (1 ulp en el `exp` de numba en esta máquina): afecta pesos internos de gemelos viejos, no salidas.

**Qué se aprendió que cambia el rumbo:**
- En el mundo de ECO (pista v2) el hijo nace sin nada del linaje; en la carrera (pista v1) el carro ES la memoria del linaje. Las piezas
  de herencia valen distinto en cada mundo. Hay que decir en qué mundo vale cada pieza.
- A mano, las piezas no suman (0 de 7 mejoran a v14.3; el Frankenstein con todo es peor que sin mapa, curiosidad, modelo o lenta).
  La selección sí encuentra perillas que sirven en OTRO mundo (ECO-T serie: TRANSFIERE; FAB_EVO3 6/6).

**Propuesta para el director (orden):**
1. Auditar en el PC n10c, ECO v1.1, ECO-T y, cuando corran, ECO v1.2 y ECO v2. Aceptar o no nube-4, nube-5, nube-6 como ERR.
2. **ECO v3 = los seis órganos del Frankenstein como genes** (mapa, curiosidad, modelo, lenta, herencia, interruptor, y b5): ya existen
   con interruptores y arnés 33/33; en vez de elegir a mano qué órgano va, que la selección lo elija en cada mundo. Primero en Python y en
   un mundo chico; gemelo después si la señal lo pide.
3. Frente 1: dejar de agregar piezas a mano a v14.3 en la carrera; llevar su configuración a ECO para que la selección la ajuste.
4. "Data sintética": esperando la confirmación del director sobre a qué se refiere.
