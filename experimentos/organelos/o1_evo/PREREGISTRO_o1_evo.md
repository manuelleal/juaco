# PREREGISTRO — O1 CON PERILLAS HEREDABLES: ¿la selección hace a O1 mejor que su diseñador? (o1_evo, parte A, 30-sep-2026; escrito ANTES del humo; con los cambios por auditoría ANTES de datos, sec. 12)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Encargo del director (30-sep): "O1 con perillas heredables". CONFIRMATORIO. Siguiente ERR libre: ERR-157 (este bloque no abre ninguno).

## 0. Qué NO es
No es un intento de "cruzar el muro": O1 ya cruza (136–139/180, mayoría 18–19/20). La pregunta es si la selección por pasajes (la que ya
afinó el termostato ×2) **mejora** a un organismo que ya vive. No inventa piezas: sólo mueve 4 perillas continuas de O1.

## 1. Pregunta y de dónde sale
¿Diez pasajes de T 25 000 (lo vivo al final de un pasaje siembra a los fundadores del siguiente, sin juez) mueven las 4 perillas de O1 hacia
valores con los que el linaje **cruza más** que O1 de fábrica y que el mismo carro sin transferencia?
- Origen: ESTADO 29-sep ("la selección afina perillas continuas pero no inventa combinaciones"; "O1 funciona como conjunto"). Termostato
  en la pista FUNCIONA ×2 (`reunion/opusB/PREREGISTRO_termostato_pista.md`): mismo esquema de pasajes, aquí aplicado a O1 entero.
- No hay exploratorio previo de O1_PAS: no hay sesgo de diseño por datos vistos (el diseño copia a `pasg`).

## 2. Mecanismo y memoria nueva
- Carro `O1_PAS` (`construye_o1_pas.py` sha `8013e4a99a004bda`; carro `c5377ada6b28bee0`; `O1_PAS0` `940a70aeacb8581c`), **por anclas** desde
  `carrera_escuderias/carros/O1.py` (`99436afa2715f028`, sólo se lee). **13 anclas**, cada una exactamente una vez; un chequeo `ast` garantiza que
  las 4 constantes ya no se leen como globales en ningún método.
- **Genes (4 floats por cuerpo; es toda la memoria nueva):**

| gen | fábrica | qué decide | clip |
|---|---|---|---|
| MARGEN | 0.25 | muerde lo bueno si la necesidad que sube está bajo rep_umbral (1.0) + MARGEN; y dispara la limpieza | [−0.5, 0.5] |
| PRUEBA | 0.50 | prueba una letra desconocida sólo si E y Ag > PRUEBA | [0, 1.5] |
| PEN_OTRO | 0.35 | factor al blanco si otro cuerpo está más cerca | [0, 1.5] |
| PISO | 0.20 | la limpieza no baja la necesidad golpeada de aquí (fuera de la ventana de parto) | [0, 1] |

  **Por qué estas 4:** son las 4 constantes de O1 que deciden *cuándo comer, cuándo probar y cuándo limpiar* — el muro es "decidir cuándo
  limpiar y cuándo comer" (ESTADO 28-sep). D0 (suavizado de distancia) queda fijo: no es una decisión comer/limpiar. Los pesos de urgencia
  (4/2/1) quedan fijos: son una tabla, no un umbral.
- **Herencia:** fundador (el primero y cada refundación de la ENMIENDA 5) = una entrada de SIEMBRA al azar (o FÁBRICA si no hay siembra) +
  N(0, σ) por gen; hijo = genes del padre + N(0, σ) (viajan en la memoria del parto, `'_gen'`). **σ = 0.03** (el σ de `pasg`; fijado a priori).
  rng propio `[PS_SEMILLA, índice, instancia, 7702]`: no toca el rng del mundo, del cuerpo ni del hijo. `salida()` no cambia.
- **Perilla `PS_LEE`** (la fija el runner): con 0 los genes se heredan, mutan, se muestrean y se transfieren IGUAL, pero el cuerpo NO los lee
  (decide con las constantes de fábrica). Es la cadena del brazo neutro `o1neu` (sec. 3). Con `PS_LEE` 0 el carro es O1 bit a bit con cualquier σ (arnés (n)).
- **Transferencia** (`corre_o1_evo.siembra`): genes de los cuerpos VIVOS muestreados cada 1 000 pasos en los últimos 5 000 pasos del pasaje,
  9 linajes (~45 entradas). No ve R0, ni hijos, ni cruza. **La moneda de la siembra es sobrevivir al muestreo (estar vivo en t = 20k…24k),
  no el establecimiento** que mide el juez (0 fundadores tras 10k y R0 real ≥ 0.9). Cada linaje aporta sus 5 muestras aunque sea un
  refundador reciente: **los refundadores diluyen la siembra** con genes recién sacados de la siembra anterior (como en `pasg`: la selección
  entre linajes es débil; la de dentro del linaje es por quién pare).

## 3. Brazos (monocultivo de 9 carros iguales, pista vieja, L 360, 36 objetos, fundador limpio 1, pizarra 1)
| brazo | qué es |
|---|---|
| `o1pas` | CANDIDATO: cadena de 10 pasajes con transferencia; en la prueba T 100k, fundadores de la siembra FIJA del último pasaje de SU cadena (σ 0.03 sigue actuando) |
| `o1neu` | CONTROL NEUTRO (por auditoría): LA MISMA cadena que `o1pas` (mismas semillas de pasaje, herencia, mutación, muestreo y transferencia) con `PS_LEE` 0: los genes derivan pero ningún cuerpo los lee, así que la selección no los ve; en la prueba T 100k, `PS_LEE` 1 con la siembra final de SU cadena |
| `o1ctl` | CONTROL: el mismo carro y σ, SIN transferencia (fundadores de FÁBRICA + mutación); misma semilla de prueba |
| `o1` | O1 de fábrica (sin mutación): la BASE |
| `termo` | V143_TERMO (ancla descriptiva) |
| `v143` | V143 (ancla de validez) |

- **Diferencia con `pasg` (declarada):** la cadena de `o1ctl` NO se corre. Sin transferencia sus pasajes no tocan su prueba (la prueba de
  `o1ctl` es O1_PAS con siembra None, idéntica en distribución al pasaje 0 de cualquier cadena). El pasaje 0 de cada cadena `o1pas` ES un pasaje
  sin selección entre pasajes (siembra None) y da el "movimiento de genes dentro de un pasaje". Ahorra ~20 % de CPU. Por eso no hay "V2 p0 pasg == ctl":
  lo sustituye el arnés (b) (o1ctl con σ 0 == o1 por el juez) y V4 (la siembra actúa en o1pas y no en o1ctl).
- `o1ctl` contra `o1` mide el costo de la mutación (descriptivo). **`o1pas` contra `o1ctl` (PC) mide la TRANSFERENCIA: selección + deriva
  acumulada** en 250 000 pasos previos. **`o1pas` contra `o1neu` (PN) separa la selección de la deriva acumulada**: mismo proceso de
  mutación, herencia y transferencia, y la única diferencia es si los genes se leyeron (y por tanto si la selección pudo verlos) en la cadena.
- Por qué genes que no se leen y no "un vivo al azar": todo vivo muestreado es un sobreviviente, así que tomar uno al azar sigue arrastrando
  selección; con `PS_LEE` 0 los genes viajan por la misma genealogía (de O1 de fábrica) sin afectarla: es deriva pura con el mismo número de
  mutaciones por linaje. Números aleatorios comunes: `o1neu` y `o1pas` comparten semillas de pasaje y corrientes de mutación; con T corto sus
  siembras pueden coincidir exactamente (visto en el arnés (h), T 2 000) y se separan cuando las genealogías divergen.

## 4. Instrumento, semillas, T, costo
- Runner `corre_o1_evo.py` (`--humo`, `--serie`, `--replica`, `--lee`, `--bloque`, `--reanuda`, `--pool N ≤ 4`); cada corrida ES
  `corre_v143.tarea` (regla 14, arnés (a)); JSON por trabajo y por pasaje (ERR-54), `--reanuda` salta lo hecho y reintenta los abortos; candados
  (se niega si ya hay veredicto; réplica sólo por la regla de parada; `git_limpio` del preregistro, runner, constructor y carro; sha del runner
  igual en serie y réplica); `fija()` carga y verifica el carro en CADA worker y escribe su estado en el JSON (V5). Shas en `SHAS`.
- **Semillas NUEVAS (617xxx).** Grep 30-sep en todo `PROYECTOS/JUACO`: en .py/.md no aparece; en .txt/.out/.json sólo como dígitos decimales o
  conteos (p. ej. `alpha 4.617547`), no como semillas.
  - serie: pasaje p de la cadena i → 617000 + 10 i + p (617000–617199); prueba T 100k de i → 617201 + i (617201–617220);
  - réplica: 617300 + 10 i + p (617300–617499); prueba 617501 + i (617501–617520);
  - práctica: 617900–617999 (arnés 617950–617989; humo 617990–617998).
  - la cadena `o1neu` usa LAS MISMAS semillas de pasaje que la de `o1pas` (pareada, números aleatorios comunes).
- T pasaje 25 000; 10 pasajes; T prueba 100 000; 20 índices. Pool 4 (máx.). Costo: ver §11 bis (medido en el humo).

## 5. Medidas
- **Principal:** linajes que cruzan (`cruza_real` del juez: R0 real ≥ 0.90 y 0 fundadores tras t = 10 000), por índice (0–9) y suma (de 180).
- Co-principal DESCRIPTIVA (no decide): fundadores por linaje (establecimiento), pareada o1pas vs o1.
- Descriptivos: trayectoria de cada gen por pasaje en `o1pas` y en `o1neu` (mediana de cadenas de la media de la siembra), desplazamiento en
  p9 contra fábrica (mediana, mediana del valor absoluto, cuántas cadenas suben/bajan), genes de los vivos al final de la prueba, **genes por
  linaje (media de sus vivos y último vivo) cruzados con `fund_post10k`** (establecidos contra no establecidos), R0 real, mayorías, mundo A+C,
  cruzan por pasaje de la cadena.

## 6. LA LETRA (`corre_o1_evo.lee_serie`; el arnés la prueba en 24 casos sintéticos: (f) 15 y (L) 9)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (20 cadenas, 100 pruebas), 0 abortos, contabilidad física coherente.
- V2: `o1` con mayoría de linajes que cruzan (≥ 5/9) en **≥ 16/20**. Binomial: histórico 18, 19, 20/20 (57/60 ≈ 0.95); con p = 0.90 (conservador)
  P(X ≤ 15) = 0.043; con p = 0.95, 0.003. Fijado ANTES de mirar corridas de esta familia (regla de ERR-156).
- V3: `v143`, mediana de índices del R0 real mediano, en [0.40, 0.80].
- V4: la siembra actúa: en `o1pas` y en `o1neu` todos los fundadores de la prueba salen de la siembra (20/20 índices); en `o1ctl`, ninguno.
- V5: estado escrito por cada worker: carro correcto en todos los brazos; σ 0.03 y `PS_LEE` 1 en las pruebas de o1pas, o1neu y o1ctl;
  `PS_LEE` 1 en cada pasaje de la cadena `o1pas` y 0 en cada pasaje de la cadena `o1neu` (si el neutro no fue neutro: NO SE LEE).
**Puertas (empates EN CONTRA):**
- PA: `o1pas` > `o1` en linajes que cruzan en **≥ 13/20** índices.
- PB: suma(`o1pas`) ≥ suma(`o1`) **+ 10**.
- PC-par: `o1pas` > `o1ctl` en ≥ 13/20. PC-suma: suma(`o1pas`) ≥ suma(`o1ctl`) + 10.
- PN-par: `o1pas` > `o1neu` en ≥ 13/20. PN-suma: suma(`o1pas`) ≥ suma(`o1neu`) + 10.
**Veredictos:**
- FUNCIONA: V1–V5 y PA, PB, PC-par, PC-suma, PN-par, PN-suma.
- HAY ALGO MODESTO: no FUNCIONA, y (PA o PB) y (PC-par o PC-suma): "sólo la suma o sólo lo pareado". Con matiz:
  **"MODESTO (transferencia, no selección)"** si PN no pasa entero (en particular: PA, PB y PC pasan pero PN no); "MODESTO (selección
  parcial)" si PN pasa entero pero PA/PB/PC sólo en parte.
- NO: lo demás (incluye ganar a `o1` sin ganar a `o1ctl`: la mutación sola, sin selección entre pasajes, no es lo que se pregunta).
- **EN EL UMBRAL** (regla 12): si cualquier conteo pareado (PA, PC, PN) queda a ±1 de 13 (12–14) o cualquier diferencia de suma a ±1 de 10 (9–11).
- **Bloque** (serie + réplica): si coinciden vale ése; si no, el menor; NO SE LEE manda.

## 7. Regla de parada
- Réplica (semillas 617300–617520) sólo si la serie da FUNCIONA, MODESTO, o NO **en el umbral**. El runner lo exige.
- PC mide **transferencia (selección + deriva acumulada)**; sólo PN separa la selección. **"Afina" o "mejora" se dicen sólo con PN y con
  una trayectoria direccional** (el desplazamiento de al menos un gen en `o1pas` con el mismo signo en ≥ 15/20 cadenas y mayor en valor
  absoluto que en `o1neu`). FUNCIONA ×2 → "la selección por pasajes afina las perillas de O1 y mejora su establecimiento en la pista"
  (prohibido "O1 evoluciona un órgano", "la evolución supera al diseñador" sin la palabra "perillas"). MODESTO (transferencia, no
  selección) → "transferir genes de la cadena ayuda, pero la deriva sola hace lo mismo": no se dice "selección". MODESTO → se registra, no se repite.
- **NO SE LEE no tiene salida por esta letra:** no se relee, no se reinterpreta ni se re-corre con las mismas semillas; se registra la causa
  (con número de ERR si es del instrumento) y cualquier intento nuevo lleva semillas nuevas y preregistro commiteado.
- **V2/V3 en el borde** (O1 exactamente 16/20; v143 en [0.40, 0.42] o [0.78, 0.80]): la validez vale tal como está escrita, sin redondeos ni
  márgenes; se reporta "validez en el borde". Con V2 o V3 fuera por uno, NO SE LEE igual.
  NO → "O1 está cerca de un óptimo local de sus perillas para esta pista, o la selección por viabilidad no lo ve" (no se distingue sin otro bloque).

## 8. Predicciones firmadas (antes del humo)
| # | predicción | rango | p |
|---|---|---|---|
| Q1 | `o1`: suma de linajes que cruzan | [125, 150] | 0.80 |
| Q2 | V2 (o1 ≥ 16/20) y V3 (v143 en banda) pasan | | 0.85 |
| Q3 | `o1ctl`: suma | [110, 145]; ≤ o1 | 0.65 |
| Q4 | `o1pas`: suma | [115, 155] | 0.70 |
| Q5 | PA (o1pas > o1 en ≥ 13/20) | | 0.15 |
| Q6 | PB (+10 sobre o1) | | 0.30 |
| Q7 | los genes se mueven: al menos un gen con desplazamiento mediano en p9 ≥ 0.05 contra fábrica | | 0.75 |
| Q8 | MARGEN sube (p9 > 0.25) en ≥ 12/20 cadenas (comer más paga en viabilidad) | mediana p9 en [0.28, 0.45] | 0.50 |
| Q9 | PRUEBA, PEN_OTRO y PISO: desplazamiento mediano en p9 < 0.10 en valor absoluto (casi deriva) | | 0.50 |
| Q10 | fundadores por linaje (media) de o1pas ≤ los de o1 en ≥ 10/20 índices | | 0.50 |
| Q11 | (por auditoría, antes de datos) PN (o1pas > o1neu en ≥ 13/20 y +10) | | 0.12 |
| Q12 | o1neu suma dentro de ±10 de o1ctl (la deriva acumulada sola casi no cambia el cruce) | | 0.60 |
| V | veredicto de la SERIE: FUNCIONA / MODESTO / NO / NO SE LEE (con PN ya en la letra) | | 0.06 / 0.17 / 0.64 / 0.13 |

(La fila V original, escrita antes del humo sin `o1neu`, era 0.10 / 0.15 / 0.62 / 0.13; se conserva aquí como registro.)

Predicción honesta: O1 cruza en ~7/9 linajes por índice y el techo es 9; con empates en contra, ganar 13/20 exige +1 casi siempre. Lo más
probable es NO (p 0.62): O1 está cerca de su techo en esta pista, y la selección por viabilidad (vivos al final) no mira la letra del juez.

## 9. Las cuatro trampas
- **Canal simétrico:** no hay canal nuevo; O1 no lee ni escribe la pizarra. La transferencia es entre pasajes del MISMO brazo y se declara.
- **Acierto sin balancear:** la medida es `cruza_real` del juez (física), no un acierto del carro.
- **Mundo que se come la comida:** un MARGEN más alto come más y puede pelar el mundo (monocultivo: se lo come a sí mismo). Se reporta
  mundo A+C por brazo y fundadores por linaje; si o1pas gana comiendo más y pelando el mundo, se dice.
- **Sitios fijos:** semilla nueva por pasaje y por prueba; posiciones y orden de turno del rng de la pista.

## 10. Riesgos
- Carga de mutación: σ 0.03 durante la prueba puede bajar a `o1pas` y a `o1ctl` bajo `o1` (por eso `o1ctl` existe y `o1` no muta).
- Deriva: con muchas generaciones por pasaje la deriva puede dominar a la selección (genes que se mueven sin mejorar: Q7 sí, PA no). `o1neu` la mide.
- La moneda de la siembra (sobrevivir al muestreo) no es la de la letra (establecimiento): la selección puede empujar hacia cuerpos que viven
  mucho y paren poco. Los refundadores diluyen la siembra con genes de la siembra anterior (débil entre linajes).
- V2: O1 de fábrica es la base y el ancla a la vez; si cae bajo 16/20 la serie es NO SE LEE.

## 11. Arnés, humo y comandos
- Arnés `identidad_o1_evo.py` → `identidad_o1_evo_salida.txt`: **ARNES PASA, 64/64** (179.6 s; con los shas finales de sec. 12).
  Historia: el primer intento dio 43/44 (el caso sintético "MODESTO sólo lo pareado" del ARNÉS estaba mal construido, +10 y no +5; se corrigió
  el caso, no la letra); luego 48/48 con (h); ahora 64/64 con (n), (L) y las comprobaciones de `o1neu` en (e) y (h).
  Salida ENTERA: O1_PAS0 == O1; O1_PAS σ 0 (sin siembra y con siembra de fábrica) == O1; O1_PAS σ 0 con genes X == O1 con las 4 constantes
  escritas a mano en X (cableado); **O1_PAS con `PS_LEE` 0, σ 0.03 y siembra X == O1** (el neutro no actúa) aunque sus genes se mueven.
- Humo `--humo` (1 proceso: 2 cadenas × 2 pasajes de T 5 000 + o1ctl y o1 de T 20 000 = 6 corridas, 60 000 pasos; práctica 617990–617998;
  NO cuenta) y `--humo --reanuda` (2.º proceso: termo, v143, o1pas, o1neu = 4 corridas, 80 000 pasos; y lee).
```
python experimentos/organelos/o1_evo/construye_o1_pas.py --verifica
python experimentos/organelos/o1_evo/identidad_o1_evo.py
python experimentos/organelos/o1_evo/corre_o1_evo.py --humo
python experimentos/organelos/o1_evo/corre_o1_evo.py --humo --reanuda
python experimentos/organelos/o1_evo/corre_o1_evo.py --serie --pool 4 2>&1 | tee experimentos/organelos/o1_evo/serie_pool4.log
python experimentos/organelos/o1_evo/corre_o1_evo.py --replica --pool 4 2>&1 | tee experimentos/organelos/o1_evo/replica_pool4.log   # sólo por §7
python experimentos/organelos/o1_evo/corre_o1_evo.py --bloque <datos/serie_*/resumen.json>,<datos/replica_*/resumen.json>
```

### 11 bis. Resultado del humo con el sha final (29-sep 19:28–19:33; NO cuenta; nada de aquí cambia §6–§8)
`humo_salida.txt` y `humo_reanuda_salida.txt`; carpeta `datos/humo/humo_20260929_192822/` (resumen sha `17ce2240d722f9cb`); runner
`corre_o1_evo.py` sha `95622a2f93bb38b0`; preregistro en ese momento `610f894f1b202255`; 10 corridas en dos procesos (6 + 4), 140 000 pasos, 0 abortos.
- V1, V3, V4, V5 True: prueba o1pas 108/108 fundadores de la siembra; o1neu 65/65; o1ctl 0/171. Las cadenas o1pas y o1neu (mismas semillas)
  dan siembras distintas ya a T 5 000 (MARGEN p1 0.2491 contra 0.2542): el neutro no es una copia.
- A T 20 000 nadie cruza (0/9 en los 6 brazos; T corto): V2 falla y la letra da NO SE LEE, como corresponde a un humo.
- Humo anterior (antes de la auditoría, sin o1neu): `datos/humo/humo_20260929_190758/`, runner `49e1554c842cf74e`, 7 corridas, 0 abortos. Queda como historia.
- **Tiempos medidos (un proceso):** pasaje de O1_PAS a T 5 000 ≈ 9 s (≈ 45 s por 25k); pruebas de 20 000: o1 36 s, o1ctl 40 s, o1pas 51 s,
  o1neu 52 s, termo 18.5 s, v143 24.6 s. Por índice ≈ 2 cadenas × 10 × 45–55 s (≈ 1 000 s) + o1pas 255 + o1neu 260 + o1ctl 200 + o1 180 +
  termo 93 + v143 123 ≈ **2 100 s de CPU** → serie ≈ 42 000 s → **≈ 2.9 h con Pool 4 sin contención (estimo 3.2–3.6 h reales)**. Réplica
  igual. Es más que el objetivo de 2 h: el brazo neutro cuesta ~+80 %. Declarado; decide el coordinador.

## 12. Cambios por auditoría antes de datos (30-sep)
Auditor: LISTO CON CAMBIOS. Coordinador: además agregar el brazo neutro. Todo esto se escribió y probó ANTES de cualquier dato de serie (sólo
había humos, que no cuentan). No lleva número de ERR: no se cambió un criterio después de ver datos de la familia.
1. **Brazo `o1neu`** (sec. 3): cadena idéntica a la de `o1pas` con `PS_LEE` 0 (genes que no se leen); prueba con `PS_LEE` 1. Elegido sobre
   "un vivo al azar" porque todo vivo muestreado ya es un sobreviviente (arrastra selección); con genes no leídos la deriva acumulada es la misma
   y la selección no los ve. Nueva perilla `PS_LEE` en el constructor (shas nuevos, sec. 2).
2. **Letra:** PN-par y PN-suma (o1pas contra o1neu, misma forma que PC); FUNCIONA exige PN; si PA, PB y PC pasan pero PN no:
   "MODESTO (transferencia, no selección)"; "en el umbral" incluye PN; V4 y V5 cubren o1neu. Casos sintéticos nuevos en (L).
3. **Descriptivo:** genes por linaje en cada fila (media y último vivo) cruzados con `fund_post10k`.
4. **Texto:** §3 y §7: PC mide transferencia (selección + deriva acumulada); "afina"/"mejora" sólo con PN y trayectoria direccional.
   §2 y §10: la moneda de la siembra es sobrevivir al muestreo, no el establecimiento; los refundadores diluyen. §2: 13 anclas (antes decía 12,
   mal contado). §7: NO SE LEE sin salida; V2/V3 en el borde.
5. **Predicciones:** se agregan Q11 (PN, p 0.12) y Q12 y una fila V nueva con PN en la letra (0.06 / 0.17 / 0.64 / 0.13); la fila V original
   se conserva escrita.
6. **Shas finales:** `construye_o1_pas.py` `8013e4a99a004bda` · `carros/O1_PAS.py` `c5377ada6b28bee0` · `carros/O1_PAS0.py` `940a70aeacb8581c` ·
   `corre_o1_evo.py` `95622a2f93bb38b0` · `identidad_o1_evo.py` (ver informe) · este preregistro: el que quede commiteado (el runner lo registra en el log).
