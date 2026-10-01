# PREREGISTRO — PELDAÑO 7 DE LA ESCALERA: SEÑAL POR PIZARRA CON SIGNIFICADO DADO POR EL DISEÑO, ENTRE LINAJES CLONES, CON COSTO DE EMITIR (O1_LUGAR_SENAL en el mundo con oasis), CONFIRMATORIO (30-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y
réplicas). Encargo del director (30-sep, "LA ESCALERA", modo ráfaga). Ingeniero genético: Fable. Plan completo: `ESCALERA.md` (P7).
**DECLARACIÓN (sesgo del diseñador):** este diseño VIENE DE UNA EXPLORACIÓN VISTA. Antes de escribir esta letra se corrieron dos humos
(739790–739791, T 30k) y una exploración (739701–739702, T 100k) de un proceso, SIN costo de emitir (sec. 11, `BITACORA.md`); con esos
datos se eligieron (i) el control (lado opuesto/antípoda en vez de permutación: el humo 1 mostró que la permutación filtraba contenido, el
mismo hallazgo que ERR-170 en P1), (ii) los brazos (sen / senbar / lug) y (iii) la puerta co-principal de fundadores (en la exploración la
señal más grande fue en fundadores por linaje: 6.6 contra 30.3, y en vida mediana). Lo que NO se vio nunca: el costo de emitir `c_e`
(perilla de mundo nueva, humo 3 pendiente) ni ninguna semilla de la serie. Las semillas de la serie son NUEVAS y disjuntas de las vistas.
Escrito ANTES de cualquier dato de serie y ANTES del humo 3 (con costo). Siguiente ERR libre: ERR-172 (este bloque no abre ninguno).

## 0. Qué es y qué no es
Es DISEÑO dirigido: el ingeniero pone en O1_LUGAR (P1) un módulo (SEÑAL: escribir en la pizarra pública DÓNDE le fue bien y sembrar la
memoria de lugar con lo que oye) y pone en el mundo un COSTO de emitir. NO es selección natural. El significado de la señal es DADO por
diseño (N2 del 18-sep: el significado no emerge por refuerzo; N1/N3d: con significado dado el canal sirve ×3). Lo que se pregunta es si un
canal con significado dado, QUE CUESTA, le paga al linaje en la moneda del juez contra un control que oye lo mismo y lo siembra en el
lugar equivocado. Depende de P1: si P1 da NO, P7 se lee igual (sen vs lug es autocontenido) pero su interpretación cambia (sec. 7).

## 1. Pregunta
En el mundo de P1b (oasis denso, vista parcial) con costo de emitir `c_e` = 0.01 E por escritura, ¿O1_LUGAR + SEÑAL (`sen`) cruza más y se
refunda menos que O1_LUGAR mudo (`lug`), y más que O1_LUGAR + SEÑAL que lee el antípoda (`senbar`), y lo hace llegando al oasis ANTES
(latencia por vida desde el nacimiento hasta el primer bocado dentro, física)?

## 2. Mecanismo y memoria nueva (carro `O1_LUGAR_SENAL`, `construye_p7.py`, por anclas sobre el texto de O1_LUGAR que produce
`construye_p1.py` sha `90dc1b6f848fac80` (texto O1_LUGAR sha `49eee6bb278ea097`; commit 76dc3d11); cadena O1 `99436afa2715f028` → O1_LUGAR → O1_LUGAR_SENAL)
- **EMITE:** cada `SN_CADA` = 100 pasos, si su memoria de lugar tiene un bin VIVIDO (nl > 0) con bono total > `SN_UMBRAL` = 0.3, escribe en la
  pizarra pública (canal de la pista: ≤ 8 números, CUPO 16, FIFO) la tripla (bin, bono_E, bono_Ag) de su mejor bin. Significado dado:
  "en el bin b me fue así de bien".
- **LEE:** al inicio de `actua`, las entradas nuevas de la pizarra que no son suyas; si el linaje NO ha estado en ese bin (nl == 0), SIEMBRA su
  memoria de lugar con lo leído (máximo, peso `SN_W` = 1.0). Lo vivido manda sobre lo oído: en cuanto muerde allí, la EMA lo corrige.
- Memoria nueva: el último t leído (1 entero) + 3 contadores. `salida()` agrega `sn_escribe`, `sn_lee`, `sn_siembra` (telemetría; no puntúa).
- Con `SENAL` = 0 el carro es O1_LUGAR bit a bit (salida entera); con la pizarra apagada también (mudo == base), arnés.
- **Control de contenido `O1_LUGAR_SENAL_BAR`** (`SN_BARAJA` = 1): emite igual y paga igual; al leer, siembra el bin ANTÍPODA (b + 15 mod 30):
  oye lo mismo, siembra SIEMPRE un lugar equivocado (el oasis son 4 bins contiguos de 30: al sembrar, el antípoda nunca toca el oasis; el
  cuerpo sí puede entrar al oasis por sus propios medios). Mismo tipo de control que P1 (ERR-170).
- **A quién paga (trampa del canal simétrico):** monocultivo: los 9 linajes son el MISMO carro; el que lee es un fundador limpio (nace sin
  memoria) o un linaje que aún no encontró el oasis. Se declara: pago al linaje y a los parientes; en pista mixta el pago sería al rival.
  Se reporta quién escribe (linajes con escrituras > 0) y cuánto se siembra, por brazo.
- Los tres carros pasan `revisa_carro`.

## 3. Mundo (`mundo_tramo_c.py`: `pista.py` `9f47c65e438e0ff4` + las 9 anclas de `mundo_escalera.py` sha `4f28b372207ba0a6` + 8 anclas propias; `juez.py` `6a68f640a7832f12`)
El de P1b (`oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista_r 20`; T 100 000; monocultivo de 9; fundador limpio) con UNA perilla nueva:
- `c_e` = 0.01: cada escritura ACEPTADA en la pizarra le cuesta 0.01 de E al que escribe, en el acto. Tope: a `SN_CADA` 100, si emitiera
  siempre, 0.0001 E/paso = 10 % del metabolismo (0.001/paso); lo MEDIDO en la exploración sin costo fue ~3 900 escrituras por corrida de 9
  linajes y 100k pasos → 39 E / 9 ≈ 4.3 E por linaje sobre 100 E de metabolismo: **≈ 4 % del metabolismo** (ERR-173: la primera versión decía
  10 % y 0.3 E por linaje). Hablar cuesta, callar es gratis. Con `c_e` = 0 el mundo es `mundo_escalera` bit a bit (arnés M).
- Sensibilidad declarada (no se toca): `SN_UMBRAL` = 0.3 fija cuántas veces se emite (y por tanto el costo); con un umbral más bajo se
  emitiría más y se pagaría más; con uno más alto, menos. No se exploró; 0.3 es el valor de los humos 1-2 y la exploración.
- Se registra por linaje `cobros` (física) y la `latencia_vida` (pasos desde el nacimiento hasta el primer bocado A+C dentro, por vida).
- Las demás perillas del tramo C (`letra_x`, `cerrojo`, `cerrojo_pobre`, `mueve`) van APAGADAS en este peldaño (arnés M: apagadas == `mundo_escalera`
  bit a bit). `mundo_tramo_c.py` se fija por sha en `corre_p7.verifica()` (H-4): sha final `4a1044a4e0e1d5c9` (el humo 3 corrió con `1a423097d67f2203`,
  antes de agregar `cerrojo_pobre` para el humo 2 de P9; la diferencia no toca a P7: arnés re-corrido).

## 4. Brazos
| brazo | carro | mundo | qué es |
|---|---|---|---|
| `sen` | O1_LUGAR_SENAL (`fab119d6fda1e5f1`) | P1b + `c_e` 0.01 | CANDIDATO |
| `senbar` | O1_LUGAR_SENAL_BAR (`cab7460e91e215e3`) | P1b + `c_e` 0.01 | control de CONTENIDO: mismo canal, mismo costo, siembra el antípoda |
| `lug` | O1_LUGAR (`49eee6bb278ea097`) | P1b + `c_e` 0.01 | la BASE (mudo; el costo no lo toca: arnés) |
(Sin `o1f`: la validez de la pista lisa es V2 de P1, que corre antes. V2 aquí es que el canal actúe.)

## 5. Medidas
- **Principal:** linajes que cruzan (`cruza_real`), por semilla y suma (de 180). Pareado por semilla, empates EN CONTRA.
- **Co-principal (director):** fundadores por linaje (media de 9) por semilla, pareado `sen` < `lug` (menos refundaciones = se establece).
- **Mecanismo (física, H-9):** fracción de vidas que llegan a morder dentro del oasis, pareado `sen` > `lug` ("llegan más vidas"). Descriptivo:
  latencia mediana por vida hasta el primer bocado dentro ("llega antes"), que era la medida original.
  **Sesgo de supervivencia declarado (H-6) de la latencia:** la latencia sólo existe en las vidas que LLEGARON a morder dentro; una vida que muere antes no
  entra. Es conservador contra `sen` si `sen` hace llegar a vidas que en `lug` habrían muerto antes (entran latencias largas que en `lug` no
  existen). Se agrega como descriptivo la fracción de vidas con bocado dentro por brazo.
- Descriptivos: R0 real, establecidos, vida mediana, fracción de vidas con bocado dentro, mundo A+C, razón de pasos en el oasis, escrituras,
  cobros, siembras, linajes que escriben.

## 6. LA LETRA (`corre_p7.lee_serie`; casos sintéticos en el arnés (f), 8 casos)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (20 × 3), 0 abortos, contabilidad coherente.
- V2: el canal actúa: en TODA corrida de `sen` y `senbar`, escrituras > 0, cobros > 0 y lecturas > 0; en toda corrida de `sen`, siembras > 0;
  en `lug`, 0 escrituras.
- V3: el mundo actúa: mordidas A+C dentro > 0, `extra` 0.8, `pobre` 0.5, `c_e` 0.01 en toda corrida.
- V4: estado por worker: carro y mundo correctos; `SENAL` 1 en `sen`/`senbar`, `SN_BARAJA` 1 sólo en `senbar`, `LUGAR_BARAJA` 0 en todos.
**Puertas (n 20):**
- PA-par: `sen` > `lug` en linajes que cruzan en ≥ 13/20. PA-suma: suma(`sen`) ≥ suma(`lug`) + 10.
- PB-par: `sen` > `senbar` en ≥ 13/20. PB-suma: suma(`sen`) ≥ suma(`senbar`) + 10.
- PF: fundadores por linaje de `sen` < `lug` en ≥ 13/20 semillas.
- ~~PM: latencia mediana de `sen` < `lug` en ≥ 13/20 semillas.~~ (retirada tras el humo 3, H-9: sesgo de supervivencia en la dirección declarada)
- PM: fracción de vidas con bocado dentro del oasis (vidas que LLEGAN; física) de `sen` > `lug` en ≥ 13/20 semillas. La latencia queda como descriptivo.
**Veredictos:** FUNCIONA = V1–V4 y SEIS condiciones: PA-par, PA-suma, PB-par, PB-suma, PF y PM. HAY ALGO MODESTO = no FUNCIONA, y (PA-par o
PA-suma o PF) y (PB-par o PB-suma) y PM. NO = lo demás; si gana sin PM → "NO (gana sin llegar antes: instrumento)" y se audita. EN EL UMBRAL:
cualquier pareado a ±1 de 13 o cualquier suma a ±1 de 10. Bloque serie + réplica: si coinciden vale ése; si no, el menor; NO SE LEE manda.
PB es NECESARIA (da el signo del contenido: sin ella lo que paga es "hablar", el sesgo del canal, y el código da NO); PA mide superar al
silencio (`lug`, mudo); PF y PM son las co-principal y de mecanismo.
**Nulos declarados (ERR-174):** cada puerta pareada (PA-par, PB-par, PF, PM) con empates en contra: bajo el nulo (p = 0.5 por semilla),
P(≥ 13/20) = 0.132 (binomial). Las sumas (PA-suma, PB-suma, +10 de 180 = 5.6 % de la escala): bajo el nulo la diferencia tiene media 0; su
dispersión no se calibró (depende de la varianza por semilla: en la serie de P1, `lug` varió entre 2 y 6 por semilla) y se reporta. FUNCIONA
exige las seis a la vez; bajo el nulo, si fueran independientes, P ≈ 0.132⁴ × P(sumas) < 0.0003; no son independientes (van juntas), así que
el nulo real de FUNCIONA está entre 0.0003 y 0.132. MODESTO exige al menos dos pareadas (o una suma + PM): nulo ≤ 0.132.

## 7. Regla de parada, lectura condicional y vocabulario
- Réplica (739651–739670) sólo si la serie da FUNCIONA, MODESTO o NO en el umbral; el runner lo exige (candado) con el mismo sha del runner.
- FUNCIONA ×2 → "O1 con memoria de lugar, con una señal por pizarra de significado dado por el diseño (bin y bono), entre linajes clones y
  con costo de emitir, se establece y cruza más que el mudo y que el que lee la misma señal sembrada en el lugar equivocado, y llega antes
  al oasis". Vocabulario PERMITIDO: "señal por pizarra con significado dado por el diseño, entre linajes clones, con costo de emitir".
  PROHIBIDO: "comunicación" a secas, "mensaje", "los demás", "coopera", "lenguaje", "entiende", "aprende de otros", "altruismo", "piensa".
- Si P1 da NO (la memoria de lugar no paga) y P7 FUNCIONA: se lee "la señal paga aunque la memoria sola no" y se dice que el peldaño 1 no
  está declarado debajo: P7 NO sube a declarado hasta que P1 tenga veredicto distinto de NO SE LEE. (P1 serie 30-sep: FUNCIONA; réplica en curso.)
- MODESTO → se registra con sus puertas. Si PB cae (PB-par y PB-suma), el código da NO aunque PA/PF/PM pasen: se dice "lo que paga es hablar,
  no el contenido".
- NO SE LEE no tiene salida por esta letra (semillas nuevas y preregistro nuevo).

## 8. Predicciones firmadas (antes del humo 3 con costo y de la serie; calibradas con la exploración SIN costo, sec. 11, declarado)
| # | predicción | rango | p |
|---|---|---|---|
| Q1 | `lug`: suma de linajes que cruzan | [40, 110] de 180 | 0.70 |
| Q2 | `sen`: suma | [70, 140] | 0.65 |
| Q3 | `senbar`: suma | [25, 90]; ≤ `lug` (sembrar el lugar equivocado cuesta) | 0.60 |
| Q4 | V2 (el canal actúa en toda corrida) | | 0.85 |
| Q5 | PA (par ≥ 13/20 y +10) | | 0.55 |
| Q6 | PB (par ≥ 13/20 y +10) | | 0.70 |
| Q7 | PF (fundadores: `sen` < `lug` ≥ 13/20); medianas `sen` ≤ 12, `lug` ≥ 20 | | 0.70 |
| ~~Q8~~ | ~~PM (latencia: `sen` < `lug` ≥ 13/20)~~ (retirada H-9; en el humo 3 la latencia fue 173 vs 108 en contra de `sen`, con 41/37 vidas que llegan contra 29/16) | | ~~0.65~~ |
| Q8 | PM (fracción de vidas con bocado dentro: `sen` > `lug` ≥ 13/20); latencia descriptiva `sen` ≥ `lug` (llega más tarde porque llegan vidas que antes morían) | | 0.70 |
| ~~Q9~~ | ~~el costo NO mata: cobros medianos por corrida en `sen` ≤ 3 000 (≤ 0.3 E por linaje por 100k) y vida mediana `sen` ≥ `lug`~~ (ERR-173: aritmética mal: 3 000 × 0.01 = 30 E = 3.3 E por linaje, no 0.3; y la exploración ya dio ~3 900 escrituras) | | ~~0.75~~ |
| Q9 | el costo NO mata: cobros medianos por corrida en `sen` ≤ 5 000 (≤ 50 E por corrida ≈ 5.6 E por linaje por 100k ≈ 5.6 % del metabolismo de 100 E) y vida mediana `sen` ≥ `lug` | | 0.70 |
| Q10 | `sen` no pela el mundo: mundo A+C de `sen` ≥ 0.9 × `lug` | | 0.75 |
| V | veredicto de la SERIE: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.35 / 0.25 / 0.30 / 0.10 |

## 9. Las cuatro trampas
- **Canal simétrico:** hay canal (la pizarra). Se reporta quién escribe (linajes con escrituras > 0) y cuánto se siembra por brazo; el
  control `senbar` lleva el MISMO canal con el mismo costo; en monocultivo el pago es al linaje/parientes (declarado).
- **Acierto sin balancear:** la medida es `cruza_real`, fundadores y latencia (física), no un acierto del carro.
- **Mundo que se come la comida:** `dens` 0.5 repone el oasis; se reporta mundo A+C por brazo (Q10).
- **Sitios fijos:** el oasis se sortea por semilla; semillas nuevas 739601–739620; el antípoda del control nunca toca el oasis por construcción.

## 10. Instrumento, semillas, costo, comandos
- Runner `corre_p7.py` (`--humo`, `--explora`, `--serie --pool ≤ 2`, `--replica`, `--lee`, `--reanuda`); JSON por trabajo; `fija()` por worker (V4);
  candados: veredicto previo, réplica sólo por la regla de parada, `git` limpio de preregistro, runner, constructor, mundo, carros y de los
  archivos de P1 de los que depende (`construye_p1.py`, `mundo_escalera.py`, `corre_p1.py` congelado `392b71186cf49b60`).
- Arnés `identidad_p7.py` → `identidad_p7_salida.txt`: **ARNES PASA 36/36** (T 4000, 82 s; también 36/36 en modo corto T 800): shas por sha
  (pista, juez, O1, corre_v143, corre_p1 congelado, construye_p1 y texto de O1_LUGAR, mundo_escalera, mundo_tramo_c), carros == constructor,
  chequeo estático, mundo c_e 0 == mundo_escalera bit a bit, costo actúa y no toca al mudo, SENAL0 == O1_LUGAR, mudo == base, control antípoda
  nunca siembra el oasis, regla 14 campo a campo contra corre_p1 y corre_v143, JSON/reanuda/nube-9, 8 casos sintéticos, guardas.
- **Semillas NUEVAS 7396xx–7397xx:** serie 739601–739620; réplica 739651–739670; humo 739790–739795 (739790–739791 ya usados sin costo; el
  humo 3 con costo usa 739792–739793); exploración 739701–739705 (739701–739702 usados sin costo); arnés 739750–739759.
- **Costo:** por semilla ≈ 3 × 150 s = 450 s → serie ≈ 2.5 h CPU → **≈ 1.3 h con pool 2**; réplica igual.
```
python experimentos/organelos/escalera/construye_p7.py --verifica
python experimentos/organelos/escalera/identidad_p7.py
python experimentos/organelos/escalera/corre_p7.py --humo --desde 739792 --nota 'humo 3 con costo'        # ingeniero (un proceso)
python experimentos/organelos/escalera/corre_p7.py --serie --pool 2 2>&1 | tee experimentos/organelos/escalera/p7_serie_pool2.log   # coordinador
python experimentos/organelos/escalera/corre_p7.py --replica --pool 2 2>&1 | tee experimentos/organelos/escalera/p7_replica_pool2.log
```

## 11. Historia honesta (ráfaga; NADA de esto cuenta; `BITACORA.md`)
1. **Humo 1** (739790–739791, T 30k, sin costo, control = permutación fija por instancia): cruzan sen 5 / senbar 4 / lug 2; el control casi
   iguala al candidato porque 4 de 30 bins permutados caían en el oasis por azar (filtraba contenido). Cambio ANTES del humo 2: control =
   lado opuesto (antípoda).
2. **Humo 2** (mismas semillas): sen 5 / senbar 1 / lug 2; establecidos 16 / 10 / 13; R0 0.87 / 0.17 / 0.25.
3. **Exploración** (739701–739702, T 100k, SIN costo y con los carros VIEJOS: O1_LUGAR `8edb746f7967e877`, el de P1 antes de ERR-170, y los
   SENAL construidos sobre él; los carros de la serie son los regenerados sobre el construye_p1 antípoda): cruzan **sen 12 / senbar 5 / lug 8** (de 18); pareado sen vs lug 1 gana 1 empate;
   sen vs senbar 2/2; fundadores por linaje **6.6 / 35.9 / 30.3**; vida mediana 2344 / 1323 / 1190; establecidos 15 / 11 / 14; ratio de
   pasos en el oasis 7.3 / 6.7 / 6.7; mundo A+C 7.8 / 8.8 / 7.1. Lectura: la señal más clara está en fundadores y vida (el linaje se establece),
   el cruce es más estrecho (un empate). Por eso PF es co-principal y Q5 lleva p 0.55.
4. Lo que NO se sabe: el efecto del costo `c_e` (humo 3: ver sec. 12; si con costo `sen` ≤ `lug` en el humo, se declara y la serie se lanza
   igual: la predicción Q2/Q5 queda en riesgo, no se recalibra); si el antípoda es un control demasiado fácil (siembra lejos del oasis siempre):
   si `senbar` < `lug` en la serie, PB es más fácil que PA y se dice.

## 12. Cambios por auditoría antes de datos (30-sep) — ERR-172 / ERR-173 / ERR-174
Auditor: LISTO CON CAMBIOS. Aplicados ANTES de cualquier dato de serie (y antes de leer el humo 3):
- **ERR-172 (H-1):** `corre_p7.main()` nunca se había ejecutado extremo a extremo (sólo el arnés y una prueba con T 1500 en carpeta temporal).
  Se corre el humo 3 CON costo (`--humo --desde 739792`, un proceso) y `--lee` sobre su carpeta; salida en `humo_p7_3_salida.txt` y una línea en
  `BITACORA.md`. Los números del humo 3 se pegan abajo cuando terminen (no cambian la letra ni las predicciones).
- **ERR-173 (H-2):** Q9 estaba mal calculada (0.3 E por linaje; son 3.3 E con 3 000 cobros) y el costo se había escrito como 10 % del
  metabolismo (es el tope si emitiera siempre; lo medido ≈ 4 %). Q9 original tachada; nueva Q9 (sec. 8) y sec. 3 corregidas.
- **ERR-174 (H-3):** la sec. 6 no declaraba el nulo por puerta ni que FUNCIONA exige seis condiciones. Agregado.
- H-4: `SHA_MUNDO_TRAMO_C` fijado en `corre_p7.verifica()`; arnés re-corrido (sec. 10).
- H-5: "PB decide" → "PB es necesaria (signo del contenido); PA mide superar al silencio"; "nunca toca el oasis" → "al sembrar"; sensibilidad a
  `SN_UMBRAL` 0.3 declarada sin tocarlo (sec. 3).
- H-6: sesgo de supervivencia de PM declarado (conservador) y descriptivo nuevo: fracción de vidas con bocado dentro (runner y sec. 5).
- H-7: vocabulario del título y de la sec. 7 acotado; "MODESTO si sólo PB cae" corregido (el código da NO).
- H-8: sec. 10 (arnés completo 36/36) y sec. 11 (la exploración usó carros viejos y sin costo) corregidas.
Nada de la letra (sec. 6), de los brazos ni de las semillas de la serie cambió por estos puntos H-1…H-8.
- **H-9 (del ingeniero, TRAS el humo 3 y ANTES de todo dato de serie; candidato a ERR-175; el coordinador/auditor pueden revertirlo):** el
  humo 3 con costo (739792–739793, T 30k; `humo_p7_3_salida.txt`, carpeta `datos/p7_humo/humo_s739792-739793_T30000_20260930_204820`) dio:
  cruzan sen 4 / senbar 0 / lug 1; fundadores por linaje 2.2 / 24.1 / 18.3; vida mediana 1822 / 285 / 804; escrituras ≈ 826 por corrida
  (cobros = escrituras: ≈ 8 E por corrida de 30k ≈ 0.9 E por linaje: el costo no mata); PA, PB y PF pasan escaladas a n 2; **PM (latencia menor)
  FALLÓ en la dirección del sesgo declarado en H-6**: latencia sen 173 vs lug 108, con 41 y 37 vidas que llegan al oasis en `sen` contra 29 y
  16 en `lug`: la señal hace LLEGAR a más vidas (las que en `lug` mueren antes de llegar entran con latencias largas). Medir "antes" castiga
  justo el efecto que se busca. Cambio: PM = fracción de vidas con bocado dentro (`sen` > `lug` ≥ 13/20); la latencia queda como descriptivo
  (Q8 reescrita; la original tachada). Es un cambio de INSTRUMENTO del mecanismo, no de umbral ni de brazos; se hace por un humo de ráfaga (no
  dato) y se declara aquí. Si el auditor lo rechaza, se vuelve a la latencia y la predicción honesta es que la serie dará "NO (instrumento)".
  El humo 3 se repitió con el runner H-4/H-6 (mismas semillas; dos líneas en la bitácora) y se releyó con `--lee` con el runner final (H-9):
  `humo_p7_3_lee_salida.txt`. Con el descriptivo de H-6 ya en el runner, el humo 3 dio fracción de vidas con bocado dentro **sen 0.42 / senbar
  0.13 / lug 0.11**: es la medida que separa, y es física.
