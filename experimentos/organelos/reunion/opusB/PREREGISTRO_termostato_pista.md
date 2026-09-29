# PREREGISTRO — LA SELECCIÓN ENCUENTRA EL TERMOSTATO EN LA PISTA (Opus B, 28-sep-2026 ~22:05; escrito ANTES del humo)

Misión: llegar a la AGI por este camino. Principio del director: que la evolución construya el órgano, no nosotros, sólo con selección natural.

## 0. Qué NO es
**No es un intento contra el muro.** La letra es la del termostato (dos puertas: §6), no `cruza_real`/P1 del muro. La "mayoría que cruza" se
reporta como descriptivo. El muro sigue MAPEADO.

## 1. Pregunta y de dónde sale
¿Los pasajes seriados cortos (lo vivo al final de un pasaje siembra a los fundadores del siguiente, sin juez) llevan el margen `g` del
termostato de boca desde la zona letal hasta la banda que funciona, y con eso el bicho de la pista le gana a V143 y al mismo carro sin
transferencia?
- EXPLORATORIO de la reunión (`reunion/ACTA.md` §6, 20:55; commit f68223b): 4 cadenas × 10 pasajes de T 25k; g de la siembra de `pasg`
  0.036/0.038/0.051/0.023 (p0) → 0.126/0.184/0.206/0.259 (p9); `ctl` p9 0.013–0.051. Prueba a T 100k en 12 semillas: `pasg` R0 real 0.853,
  gana a v143 12/12 (+0.26), empata con TERMO 6/12 (0.00).
- **Sesgo declarado:** el diseño (T 25k, 10 pasajes, ventana 5k, sólo g) sale de ese exploratorio, con las mismas 4 cadenas en las que se vio.

## 2. Mecanismo y memoria nueva
- Carro `V143_PAS` (`construye_pas.py` db39a13617113793, por anclas desde `termo_banco/carros/V143_EVO_BAJO.py` 3187b373654e119f), con la
  mutación del cerebro en p = 0: el único gen que varía es `g` (el margen del termostato: muerde lo sentido bueno ⇔ ∃ j: s_j > 0 ∧
  nivel_j < rep_umbral + g). Hijo: g del padre + N(0, 0.03). Fundador: de la SIEMBRA + N(0, 0.03); sin siembra, g ~ U[−0.1, 0.1].
- Memoria nueva: un float por cuerpo (g). Los 15 genes del cerebro viajan fijos en G0 (con p 0 no cambian; arnés (b)).
- Transferencia (`corre_pas.siembra`): los (g, cerebro) de los cuerpos VIVOS muestreados cada 1 000 pasos en los últimos 5 000 pasos del
  pasaje, 9 linajes (~45 entradas). No ve R0, ni hijos, ni cruza: selección por viabilidad leída, no juez.

## 3. Brazos
| brazo | qué es |
|---|---|
| `pasg` | CANDIDATO: cadena de 10 pasajes con transferencia; en la prueba T 100k, fundadores de la siembra FIJA del último pasaje de SU cadena |
| `ctl` | CONTROL: el mismo carro, las mismas semillas de pasaje, SIN transferencia (fundadores siempre de U[−0.1, 0.1]); == V143_EVO_BAJO bit a bit |
| `v143` | base (el bicho real) |
| `termo` | V143_TERMO (g 0.40 diseñado): referencia; "pasg ≈ termo" sólo descriptivo |
| `o1` | ancla de la pista |
Diferencia con el exploratorio (declarada): allí `ctl` mutaba el cerebro (p 0.05); aquí p 0 (el control exacto de `pasg`).

## 4. Instrumento, semillas, T, costo
- Runner `corre_termostato.py` (`--humo`, `--serie`, `--replica`, `--bloque`, `--reanuda`, `--pool`); cada corrida ES `corre_pas.tarea` =
  `corre_v143.tarea` + telemetría de sólo lectura (regla 14). Shas de TODO lo que corre fijados en `SHAS` (corre_pas 49322105ff725569,
  construye_pas, V143_PAS d9dd7fb0187a0bc6, V143_TERMO, V143_EVO_BAJO, corre_v143, V143, pista, juez, O1); `verifica()` aborta si cambian.
  El sha del propio runner lo registra el log. nube-9, ERR-54, ERR-115.
- **Semillas NUEVAS (6 dígitos, 596xxx).** Grep 28-sep 21:55 en py/md/txt/log/json de `PROYECTOS/JUACO`: en .py/.md no aparece; en logs y
  JSON aparecen sólo números 596xxx que son CONTEOS (p. ej. "14169/596401" en `r2mono_O4_consola.log`), no semillas. Declarado.
  - serie: pasaje p de la cadena i → 596000 + 10i + p (596000–596199); prueba T 100k de i → 596201 + i (596201–596220);
  - réplica: 596300 + 10i + p (596300–596499); prueba 596501 + i (596501–596520);
  - práctica (arnés y humo): 596900–596999.
- T pasaje 25 000; 10 pasajes; T prueba 100 000; 20 índices por serie.
- **Costo** (tiempos del exploratorio con 4 procesos: pasaje ~41 s; prueba pasg 184 s, ctl 209, v143 220, termo 188, o1 406):
  ~2 030 s de CPU por índice → 40 600 s por serie → **≈ 2 h 15 min con Pool 6** (fase 1: 40 cadenas + 80 pruebas; fase 2: 20 pruebas pasg).
  Réplica igual. Total ≈ 4.5 h.

## 5. Medidas
- Por cadena: g medio de la siembra en cada pasaje (p0…p9); R0 real, fundadores y cruza por pasaje (descriptivos).
- Prueba T 100k: R0 real (mediana de 9 linajes) por índice; pareados por índice; mayorías que cruzan y fundadores por linaje (descriptivos).

## 6. LA LETRA (`corre_termostato.lee_serie`; el arnés la prueba en 10 casos sintéticos)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (40 cadenas, 100 pruebas), 0 abortos, contabilidad coherente.
- V2: pasaje 0 de `pasg` == pasaje 0 de `ctl` en el juez (R0_real, fund, fund_post10k, cruza) en 20/20 índices.
- V3: `v143` mediana del R0 real en [0.40, 0.80] (la ventana del muro).
- V4: `o1` con mayoría de linajes que cruzan en ≥ 15/20 (ENMIENDA 5).
- V5: la siembra actúa: en la prueba de `pasg`, todos los fundadores salen de la siembra, en los 20 índices.
**Puertas:**
- **PA (a):** pareado por índice (R0 real mediano, empate no gana): `pasg` > `v143` en ≥ 15/20 **y** `pasg` > `ctl` en ≥ 15/20.
- **PB (b):** g medio de la siembra de `pasg`: en p0 < 0.10 (zona letal) **y** en p9 dentro de [0.10, 0.60], en ≥ 15/20 cadenas.
- **PC (el control puede fallar):** g medio de la siembra de `ctl` en p9 dentro de [0.10, 0.60] en ≤ 5/20 cadenas.
**Veredictos:**
- FUNCIONA: V1–V5 y PA, PB, PC.
- HAY ALGO MODESTO: `pasg` > `ctl` en ≥ 15/20 con diferencia mediana ≥ 0.10, y mediana de cadenas del g de `pasg` en p9 ≥ 0.10.
- NO: lo demás. **Bloque** (serie + réplica): si coinciden vale ése; si no, el menor; NO SE LEE manda.
- Descriptivo: `pasg` vs `termo` pareado ("pasg ≈ termo" si gana entre 6 y 14 de 20), mayorías, fundadores por linaje.

## 7. Regla de parada
- Réplica sólo si la serie no da NO. FUNCIONA ×2 → "la selección natural encuentra el termostato en la pista" (vocabulario: "evoluciona"
  sólo con la curva de g al lado; nada de "cruza el muro"). MODESTO → se registra y no se repite. NO → la línea g-por-pasajes se cierra.

## 8. Predicciones firmadas (antes del humo)
| # | predicción | rango | p |
|---|---|---|---|
| T1 | v143: mediana del R0 real (T 100k) | [0.50, 0.70] | 0.80 |
| T2 | ctl: mediana del R0 real | [0.20, 0.45] | 0.70 |
| T3 | pasg: mediana del R0 real | [0.75, 0.92] | 0.70 |
| T4 | PA: pasg > v143 ≥ 15/20 | dif mediana [+0.10, +0.35] | 0.75 |
| T5 | PA: pasg > ctl ≥ 15/20 | dif mediana [+0.30, +0.65] | 0.90 |
| T6 | PB: cadenas con g p9 en banda | 15–20/20 (mediana de g p9 en [0.13, 0.28]) | 0.75 |
| T7 | PC: ctl con g p9 en banda | 0–3/20 | 0.90 |
| T8 | pasg vs termo | gana 5–14/20 | 0.65 |
| T9 | O1 ancla (V4) y V3 pasan | | 0.85 |
| T10 | fundadores por linaje (media) de pasg ≥ los de v143 × 0.3 y NO bajan contra ctl (descriptivo: el muro no se mueve) | | 0.70 |
| V | veredicto de la SERIE: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.55 / 0.20 / 0.07 / 0.18 |

## 9. Las cuatro trampas
- Canal simétrico: no hay canal ni pizarra nueva; la transferencia es entre pasajes del MISMO brazo y se declara.
- Acierto sin balancear: la medida es el R0 real del juez y el g de los vivos, no un acierto.
- El mundo se come la comida: es parte del mecanismo (con g alto los establecidos comen mejor y los refundadores sufren: exploratorio).
  Fundadores por linaje se reportan (T10).
- Sitios fijos: semilla de pista nueva por pasaje y por prueba; posiciones de los rng de la pista.

## 10. Riesgos
- 4 cadenas exploratorias → varianza entre cadenas mal estimada (c1 llegó sólo a 0.126: PB justa).
- V3: v143 dio 0.413 en 39001–39010; si cae bajo 0.40 la serie es NO SE LEE.
- V4: O1 cuesta 406 s por prueba y ancla la pista; su 12/12 del exploratorio hace esperable que pase.

## 11. Arnés, humo y comandos
- Arnés `identidad_termostato.py` → `identidad_termostato_salida.txt`: **ARNES PASA, 27/27** (85 s; 21:59).
- Humo `--humo` (1 proceso, 6 corridas, T 5 000, práctica 596900–596901 y 596990; NO cuenta): `humo_termostato_salida.txt`.
```
python experimentos/organelos/reunion/opusB/identidad_termostato.py
python experimentos/organelos/reunion/opusB/corre_termostato.py --humo
python experimentos/organelos/reunion/opusB/corre_termostato.py --serie --pool 6 2>&1 | tee experimentos/organelos/reunion/opusB/serie_termostato_pool6.log
python experimentos/organelos/reunion/opusB/corre_termostato.py --replica --pool 6 2>&1 | tee experimentos/organelos/reunion/opusB/replica_termostato_pool6.log   # solo si la serie no da NO
python experimentos/organelos/reunion/opusB/corre_termostato.py --bloque <datos_termostato/termostato_serie_*/resumen.json>,<datos_termostato/termostato_replica_*/resumen.json>
```

### 11 bis. Resultado del humo (22:01; NO cuenta; nada de aquí cambia §6–§8)
`humo_termostato_salida.txt`, resumen `datos_termostato/termostato_humo_20260928_220015/resumen.json` (sha 107dad8d9d8581be); runner
`corre_termostato.py` sha 27d091dd179ad95c; 6 corridas, 0 abortos, 56 s.
- V2 (p0 pasg == ctl) True; V5 (la siembra actúa) True: en p1 de `pasg` 25/25 fundadores de la siembra, en `ctl` 0/38; la física difiere.
- Coincidencia declarada: el g medio de la siembra de p1 es −0.0160 en `pasg` y en `ctl` (redondeo a 4 decimales). Verificado a mano que las
  distribuciones son distintas (pasg desde −0.13; ctl desde −0.09): es azar de T 5 000, no un error; con T 5 000 no hay tiempo de selección.
- La letra dice NO SE LEE, como corresponde a un humo incompleto (sin termo, ctl ni o1 en la prueba; T corto).
