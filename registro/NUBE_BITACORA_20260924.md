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

### 1b. JUACO-ECO (frente 2)
- **01:43 — arnés** `identidad_eco.py` (b70ec2f05915dc2e): **41/41** en 118 s (PC: 208 s). Salida idéntica a la del PC. Corrió en el
  núcleo libre mientras n10b usa los otros 3.
- **Observación, candidato a ERR nube-1 (menor, no bloquea):** el sha del runner en el preregistro no está al día.
  - El §0 de `PREREGISTRO_eco.md` cita `corre_eco.py` 0627f237b597523a.
  - El runner en main es 47d9cee4d6462116 (commit `bdb0aab`, 23-sep 19:51). Es el mismo que usó el humo `eco_humo_s19001_20260923_194831`,
    el que ejercita el juez actual (ERR-120).
  - La diferencia es la enmienda ERR-121 (P3c pasa a decidir), escrita antes de cualquier serie. El §0 no se actualizó.
  - La serie corre con el runner de main, y su log imprime el sha.

## 2. Exploratorio — **EXPLORATORIO, no es dato**
Carpeta: `experimentos/exploratorio_nube_20260924/` (su `NOTA_EXPLORATORIA.md` manda). Aquí va sólo el resumen.

_(pendiente)_

## 3. Decisiones del coordinador de la nube (hora, opción, alternativa descartada, porqué)
- **01:43 — el arnés de ECO corre ahora, en el núcleo libre, y no justo antes de su serie.**
  - Alternativa descartada: esperar a que termine n10b.
  - Por qué: ningún archivo de ECO se toca esta noche, y así un fallo aparece con horas de margen. Antes de lanzar la serie de ECO se
    vuelve a verificar el sha del runner.
- **01:45 — los candidatos a ERR se numeran como nube-N.** Así no chocan con el PC, que también numera esta noche.
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
