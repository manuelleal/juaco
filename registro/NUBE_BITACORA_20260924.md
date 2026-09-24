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

## 2. Exploratorio — **EXPLORATORIO, no es dato**
Carpeta: `experimentos/exploratorio_nube_20260924/` (su `NOTA_EXPLORATORIA.md` manda). Aquí va sólo el resumen.

_(pendiente)_

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

## 4. Qué falló y qué propongo para mañana
_(al cierre)_
