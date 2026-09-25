# PREREGISTRO — F1 ARRANQUE EN FRÍO: ¿el linaje con la tabla de la familia arranca y se mantiene SIN vivero? (25-sep-2026)

Misión: llegar a la AGI por este camino. Meta del director: **mantener el linaje sin andamio**. Ficha F1 del comité de linaje
(`experimentos/organelos/comite/investigador/FICHAS_LINAJE.md`), recomendada por el investigador. Carpeta: `experimentos/organelos/frio/`.
Nivel 10 (JUACO-ECO), frente 2. No es candidato a tronco. Escrito por un creador **antes del humo**; lo integra y lo corre el coordinador.

## 0. Instrumento (sha a 16)
| archivo | sha | origen |
|---|---|---|
| `corre_frio.py` | 3ba8b0f5cf1fbbfa | envoltorio nuevo; importa sin tocar `juaco_eco/corre_eco_v12.py` (1340d268e1fd93d8) |
| `motor_frio_rapido.py` | ff9d890a5cce9dec | `construye_frio.py` desde `juaco_eco/motor_eco_rapido_fam.py` (d1f16769a53bb51c, arnés 132/132) |
| `carros/BAR0_ECO.py` | a4b899611bd71197 | `construye_frio.py` desde `juaco_eco/carros/FAMB_RES0_ECO.py` (94ea78589bc2ce24): `MODO = 'bar'` |
| `construye_frio.py` | 5dec635e6ffe55d4 | — |
| `identidad_frio.py` | 14020f2dd126c23b | arnés (46/46; salida 46fdc008477ab0d8) |
| `ancla_1e6.py` | c3409e22b6ded85f | ancla de máquina a 1e6 contra el JSON guardado de MUT0_T s19701 (SÓLO el coordinador) |
| orígenes leídos | `motor_eco.py` bca3033878b59622 · `corre_eco.py` 47d9cee4d6462116 · `FABRICA_ECO.py` f1163009cb5193a2 | = los de la serie v1.2 19701–19720 |

- **Arnés `identidad_frio.py`** (salida en `identidad_frio_salida.txt`), sin él no hay serie:
  (K) construcción por anclas; (A) motor copiado == gemelo original en TODA la salida (FAMB y FABRICA, con vivero y en frío, MUT0 y
  VIDA); (B) envoltorio `RES0_60k` == `corre_eco_v12.trabajo(MUT0_T)` bit a bit en todas las claves de v1.2; (C) motor copiado ==
  motor Python en los 5 brazos (con BAR0: el gemelo permuta como el carro); (D) frío = 0 refundados y 0 fundadores repuestos, con el
  control que puede fallar (con vivero SÍ refunda); (E) BAR permuta de verdad; (F) nube-9; (V) la letra; (R) banderas.
- **BAR0** = `BAR_SIN0` de `subida_n10c/carros_n10c.py` (FAMB_BAR + filtro SIN0 antes de permutar) con el `_see` de ECO. `FAMB_BAR` y
  `FAMB_RES` de subida_n10b difieren sólo en `MODO` (diff); la rama `'bar'` ya estaba, verbatim, en el carro de ECO.

## 1. Hipótesis y por qué
Toda persistencia del bicho real pasó por un vivero (≥ 77 % de los cuerpos antes del corte) o por refundación. En ECO v1.2, `MUT0_T`
(familia sin neutras, sin mutación) persistió **20/20** a 1e6 con vivero hasta 60 000 (descriptivo por ERR-60; JSON verificados en
`juaco_eco/datos/eco_v12_serie_s19701-19720/`: 20/20, R0 tras el corte 0.9945–0.9970, 22–44 cuerpos vivos en T, 1 linaje). El
mismo mundo con FABRICA y MUT0 (sin familia, sin selección) persistió **0/20** en ECO v1 (×2, a 120 000) y v1.1 (a 1e6).
**H-F1:** la tabla de la familia sin neutras basta para que el linaje ARRANQUE desde 90 fundadores ingenuos y se mantenga 1e6 pasos,
sin ningún fundador repuesto desde t = 0.

## 2. Qué cambia (un solo cambio de mecanismo por brazo; todo lo demás = ECO v1.2)
Mundo w90 (esc 90, L 3600, quimiostato, 90 fundadores, tope 3000, muestra 1000), `CR.eco_cfg` de ECO (banco 200, 8 sombras,
checkpoint cada 10 000), genética **MUT0** (sin mutación) en todos, T = 1 000 000. Por brazo sólo cambian el carro y `t_corte`:

| brazo | carro | t_corte | papel |
|---|---|---|---|
| **RES0_FRIO** | FAMB_RES0_ECO | **1** | hipótesis: sin vivero (el vivero sólo podría refundar en t = 0, y en t = 0 nadie muere) |
| RES0_10k | FAMB_RES0_ECO | 10 000 | dosis de vivero (descriptivo) |
| RES0_60k | FAMB_RES0_ECO | 60 000 | **ancla** = MUT0_T de v1.2 bit a bit (arnés B) |
| BAR0_FRIO | BAR0_ECO | 1 | control de CONTENIDO que puede ganar (BAR_SIN0 dio 0.828 en un humo de n10c) |
| FAB_FRIO | FABRICA_ECO | 1 | sin familia |

Memoria nueva: **cero**. Constantes nuevas: `t_corte` por brazo.

## 3. Semillas NUEVAS (grep en `*.py` y `*.md` de organelos y bundle el 25-sep: ninguna 35001–35999 en uso)
Serie **35001–35020**; réplica **35021–35040**; práctica **35901–35909** (arnés 35901–35904; humo 35905).

## 4. Medidas
- **persiste:** cuerpos vivos en T = 1e6 (`t_ext` None y vivos > 0), como v1.2.
- **R0 de NACIDOS:** media de hijos de los cuerpos NACIDOS (fund = 0: sin los 90 fundadores ni refundados) con `tn` en
  [10 000, T − 20 000]; los vivos en T cuentan los hijos que llevan. Por semilla; **cohorte vacía = 0** (la semilla es la unidad).
- **fundadores repuestos:** `n_refund` del motor y la suma de `fundadores` por linaje. En los brazos FRÍO deben ser 0.
- Descriptivo: `t_ext`, vivos en T, `max_vivos`, vivos cada 1000 pasos hasta 10 000, `r0_post` de v1.2, la curva de dosis 1/10k/60k.

## 5. nube-9 / ERR-60, declarado ANTES de correr
- Con familia a 1e6 un linaje puede pasar de 100 000 cuerpos (17/20 VIDA_T de v1.2) y la guardia lanza `SystemExit`, que cuelga el Pool.
- **ERR-146 (este bloque):** en `motor_frio_rapido.py` el límite sube de 100 000 a 1e9. La guardia protegía la fórmula escalar
  `700000 + 1000000·seed + k` de H-1 (ERR-60); en este motor la semilla de cada cuerpo es la LISTA `[seed, linaje, ETQ, k]`
  (SeedSequence), que no colisiona para k distintos. Mientras ningún linaje pase de 100 000 la salida es idéntica (arnés A y B).
  MUT0_T de v1.2 tuvo 21 400–21 900 nacimientos en total por corrida: se espera que ni la vieja guardia dispare.
- `trabajo()` atrapa TODA excepción del motor (SystemExit incluida) y escribe un JSON marcado; ningún trabajador del Pool muere.
  **Si la guardia ERR-60 dispara: el linaje estaba vivo → persiste = 1 con marca `guardia = 1`**, y su R0 se calcula con la cohorte
  registrada hasta el aborto. Cualquier otro aborto → `persiste = None` y la serie es NO EVALUABLE.

## 6. Criterio por la letra (`corre_frio.veredicto`)
**Validez (NO EVALUABLE si falla alguna):** serie completa (5 × 20, T = 1e6, `t_corte` del brazo, sin abortos que no sean la guardia);
bloqueados = 0; **V2** 0 refundados y 0 fundadores repuestos en los 60 JSON FRÍO; **V1** ancla RES0_60k ≥ 17/20.

**Puertas (la letra de la ficha, tal cual)**
- **P1:** RES0_FRIO persiste en 1e6 en ≥ 15/20.
- **P2:** mediana (sobre las 20 semillas) del R0 de nacidos de RES0_FRIO ≥ 0.90.
- **P3:** FAB_FRIO persiste ≤ 2/20.
- **P4:** BAR0_FRIO persiste ≤ 5/20.

**Veredicto**
- **FUNCIONA: EL LINAJE ARRANCA EN FRÍO CON LA TABLA DE LA FAMILIA** = P1 + P2 + P3 + P4.
- **HAY ALGO MODESTO: ARRANCA EN FRÍO A MEDIAS** = no FUNCIONA, y RES0_FRIO ≥ 8/20, RES0_FRIO − BAR0_FRIO ≥ 6 y RES0_FRIO − FAB_FRIO ≥ 6
  (se escribe qué puertas cayeron).
- **NO:** cualquier otro caso.
- El bloque se declara sólo si serie y réplica dan el mismo veredicto; si no, vale el menor.

**Nulos (regla 15)**
| puerta | nulo | umbral | P(pasa ∣ nulo) | potencia |
|---|---|---|---|---|
| P1 | la tabla no arranca nada: RES0_FRIO como FAB (0/20 ×3 con vivero, p ≤ 0.05); nulo duro p = 0.5 | 15/20 | ≈ 0 (p 0.05) · 0.021 (p 0.5) | 0.93 si p = 0.85; 0.62 si p = 0.75 |
| P2 | R0 de nacidos como RES con neutras (0.67 / 0.77, n10c) o BAR_SIN0 (0.49 / 0.54) | 0.90 | margen 0.13 sobre el nulo más alto | — |
| P3 | FAB arranca como la selección con vivero (VIDA 7 y 9/20 a 1e6, p = 0.4) | ≤ 2/20 | 0.004 | 0.99 si p = 0.02 |
| P4 | el contenido no importa: BAR0 = RES0 (p = 0.75); nulo duro p = 0.5 | ≤ 5/20 | 4e-6 · 0.021 | 0.99 si p = 0.1; 0.80 si p = 0.2 |
| V1 | el instrumento no reproduce: p = 0.6 | ≥ 17/20 | 0.016 | 0.98 si p = 0.95 (única serie previa: 20/20) |
| M | RES0 = BAR0 = FAB con p = 0.25 / 0.5 (independientes) | ≥ 8 y Δ ≥ 6 ×2 | ≤ 0.018 / ≤ 0.040 | — |

**Aviso honesto sobre P2:** en el quimiostato, un linaje que persiste tiene R0 ≈ 1 por construcción (ficha, diagnóstico 5); P2 casi
no es independiente de P1. Se mantiene porque es la letra de la ficha; no suma evidencia propia.

## 7. Predicciones firmadas (creador F1, antes del humo; informadas por los JSON de v1, v1.1 y v1.2 citados en §1)
| cantidad | rango | probabilidad |
|---|---|---|
| **RES0_FRIO persiste /20 — la que puede fallar** | 12–20 | P1 (≥ 15) con **0.65** |
| mediana R0 nacidos RES0_FRIO | 0.95–1.01 si P1 | P2 con 0.65 |
| RES0_10k persiste /20 | 15–20 | — |
| RES0_60k persiste /20 (ancla) | 18–20 | V1 con 0.92 |
| BAR0_FRIO persiste /20 | 0–3 | P4 con 0.90 |
| FAB_FRIO persiste /20 | 0–1 | P3 con 0.97 |
| 0 refundados en FRÍO | — | V2 con 0.99 |
| veredicto de una serie | FUNCIONA 0.45 · MODESTO 0.18 · NO 0.25 · NO EVALUABLE 0.12 | — |
| bloque (serie + réplica iguales) | FUNCIONA ×2 0.35 | — |

(El investigador firmó FUNCIONA 0.35, MODESTO 0.30, NO 0.35; mi cambio sale de FAB/MUT0 0/20 ×3, que no estaba en la ficha.)

## 8. Qué refuta
- **H-F1:** P1 cae con validez intacta (la tabla de la familia no arranca el linaje sin vivero en ≥ 15/20).
- **"Es el contenido":** P4 cae (la misma tabla barajada también arranca) → la dosis de lectura, no lo que dice, sostiene el arranque.
- **"Es la familia":** P3 cae (FABRICA sola también arranca en frío) → el frío no necesitaba familia.

## 9. Vocabulario
- Permitido: «linaje», «arranca en frío», «sin fundadores repuestos desde t = 0», «la familia pasa su tabla», «persiste 1e6 pasos».
- Prohibido: «población» sin la medida; «evoluciona», «especie», «cultura», «vida artificial abierta», «autosuficiente».

## 10. Costo (medido en un proceso por el creador; el detalle en `INFORME.md`)
Referencia de v1.2 (nube, Pool 3): MUT0_T 47–50 s por corrida a 1e6 con el gemelo. Los brazos FRÍO que se extinguen pronto cuestan
segundos. Estimación: ≤ 100 corridas × ≤ 50 s / 6 ≈ 15 min por serie con Pool 6 (el PC comparte núcleos con los exploradores).

## 11. Humo, arnés y enmiendas (esta sección y las filas de sha de §0 se completaron DESPUÉS del humo; §1–§10 son las del sha 6ef3b4b5c95806c6 que registra el log del humo)
- **Arnés 13:58, antes del humo: 44/44** (167 s, python 3.14.2, numpy 2.4.3). Los números del arnés (corridas de 3 000–80 000 pasos)
  aparecieron mientras §7 ya estaba escrito.
- **Humo 14:01** (`corre_frio.py --humo`, 35905, T 200 000, un proceso, 33.6 s en total): RES0_FRIO persiste (32 vivos; 0 refundados;
  r0_nac 1.003) · RES0_10k persiste (37) · RES0_60k persiste (34; 21 325 refundados) · **BAR0_FRIO persiste (11 vivos, bajó a 1–3 cuerpos
  entre t 5 000 y 10 000)** · FAB_FRIO se extingue en t 2 792. Escribió su JSON:
  `datos/humo/frio_humo_s35905_T200000_20260925_140109.json` (a0bcca22020acdf1). Una semilla a 200 000: no se lee. **Las predicciones
  NO se tocan** (aviso, como en n10c: BAR0 puede ganar).
- **ERR-147 (tras el humo; sólo el arnés, ni runner ni letra):** se añade (Q) corte de luz simulado a mitad + `--reanuda` == la corrida
  entera, en RES0_FRIO y BAR0_FRIO. Primera versión: 45/46, porque BAR0_FRIO en 35904 se extinguía antes del corte y el caso no probaba
  nada (fallo del diseño del caso, no del instrumento); se toma la primera semilla de práctica que llega viva al corte. **Arnés final 46/46**
  (84 s). Sha del runner sin cambios (3ba8b0f5cf1fbbfa).
- Sin otras enmiendas.
