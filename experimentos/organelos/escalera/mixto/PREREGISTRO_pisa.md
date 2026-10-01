# PREREGISTRO — PISA: la señal leída puede pisar memoria de lugar caducada, en el mundo con oasis que se muda

1-oct-2026 · creador (ráfaga `escalera/mixto/`) · MISIÓN: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin
retropropagación, peldaños preregistrados con controles y réplicas).
Runner: `corre_pisa_serie.py` · carros: `construye_pisa.py` · nulo: `nulo_pisa.py` · arnés: `corre_pisa_serie.py --identidad`.

**Vocabulario.** Es DISEÑO, no selección: la regla la escribió el creador. Todo vale "en el mundo con oasis que se muda" (`mundo_tramo_c`:
oasis + mueve 20000 + c_e 0.01). No se dice "comunicación" ni "lenguaje" a secas: es una señal con significado DADO (bin y bono) por la
pizarra pública. **No reemplaza al carro de P7** (`O1_LUGAR_SENAL` queda como está; P7 FUNCIONA ×2 con él).

## 0. Sesgo declarado
La letra, los brazos y los umbrales se fijaron DESPUÉS de dos humos de ráfaga: humo 1 (s738611–12: mix / mixbar / sen9 con lectores
ORIGINALES) y humo 2 (s738621–22: pmix / pmixbar / sen9 / pmudo), más una sonda (s738611) y una corrida de P7 (s738623). Ninguna de esas
semillas entra en la serie ni en la réplica. El brazo `mix` (el que aísla la variante) NUNCA se corrió en las semillas del humo 2: la
comparación pmix vs mix de la serie es la primera pareada.

**Predicción refutada en el humo (no es puerta):** la ficha 4 predecía latencia de lectores ≤ 700 pasos. Humo 1 (lectores originales):
1547.5 y 1093.5. Humo 2 (lectores PISA): 989.5 y 768. No se alcanzó; no se usa como umbral.

## 1. Hipótesis
En `juntos` la señal no sumó sobre explorar. Causa medida (sonda de sólo lectura, s738611): tras cada mudanza, 99.8 % (mix) y 98.8 % (sen9)
de las lecturas que apuntaban al oasis NUEVO se rechazan porque `nl[b] != 0` (el linaje ya estuvo en ese bin y `nl` no se borra con la
mudanza); unas 10 000 de esas lecturas por corrida llegan a un linaje cuya memoria propia de ese bin ya no vale. Hipótesis: si lo oído puede
pisar lo vivido que ya no vale, los lectores llegan antes al oasis nuevo cuando hay UN explorador que habla.

## 2. Mecanismo mínimo y memoria nueva
`O1_SEN_PISA` = `O1_TODO_SEN` + UNA línea de conducta en `_sn_lee` (perilla `SN_PISA`; con 0 es `O1_TODO_SEN` bit a bit):

    if SN_PISA and self.nl[b] > 0 and self.lugar[b].sum() <= LG_MIN: self.nl[b] = 0; self.st['sn_pisa'] += 1

Luego actúa la regla ORIGINAL de P7 (siembra si `nl[b] == 0`). Como `nl[b]` queda en 0, el linaje no re-emite ese bin hasta vivirlo de nuevo.
**Memoria nueva: 0 floats** (reutiliza `nl`); 1 contador de telemetría. Regla local (sólo estado propio y la pizarra que ya lee).
El explorador es el `O1_TODO` ORIGINAL (no pisa).

## 3. Instrumento y anclas
Cada corrida ES `corre_juntos.tarea` (sha db75135c8c2f3e0d; a su vez `corre_v143.tarea`, regla 14) con la lista de carros sustituida por
una mixta; mundo `mundo_tramo_c` (sha 4a1044a4e0e1d5c9). Carros por anclas desde `construye_juntos` (sha d469c8f3bf194d64):
`O1_SEN_PISA` bca8f97bcb6cb353 · `O1_SEN_PISA_BAR` 95cda0103eb80b40 · `O1_SEN_PISA0` 362a150ded4ff12d. Originales: `O1_TODO`
b7519a4a481a0cf5 · `O1_TODO_SEN` dff5e762bd23612e · `O1_TODO_PREG` 382dafcf822b36a1.
Sondas de sólo lectura (ganchos en memoria sobre `_sn_lee` y `_lg_hereda` de los carros PISA): el arnés exige corrida con ganchos == sin ganchos.

## 4. Brazos (n = 20, semillas pareadas, T 100 000, mueve 20 000, c_e 0.01, 9 linajes, fundador limpio)
El explorador va en el índice **e = i mod 9** (i = índice de la semilla, 0–19): ROTADO, el mismo en los 4 brazos de cada semilla.

| brazo | explorador (1) | lectores (8) | papel |
|---|---|---|---|
| **pmix** | O1_TODO | O1_SEN_PISA | candidato |
| **mix** | O1_TODO | O1_TODO_SEN (originales) | aísla la variante, mismas semillas |
| **pmixbar** | O1_TODO | O1_SEN_PISA_BAR (leen al antípoda, b + 15 mod 30; también pisan) | control de contenido (puede ganar) |
| **pmudo** | O1_TODO_PREG (explora; ni emite ni lee) | O1_SEN_PISA | control: explorador mudo (puede ganar) |
| sen9 | — | 9 × O1_TODO_SEN | descriptivo, sólo serie, semillas 0–9 |
| pisa9 | — | 9 × O1_SEN_PISA | descriptivo, sólo serie, semillas 0–9 (la variante sin explorador) |

**Recorte declarado:** `sen9` y `pisa9` van con n = 10 y sólo en la serie (no en la réplica), al final de la cola, porque el PC se apaga a
las 14:00 y serie + réplica deben caber con pool 2. No entran en la letra ni en la validez de completitud.

Semillas NUEVAS (grep 1-oct: `7386[4-9]x` no aparece en .py/.md fuera de esta carpeta): **serie 738641–738660 · réplica 738671–738690** ·
humo de main 738695–738698 · arnés 738632.

## 5. Medida principal
Por semilla y brazo: **mediana de la latencia de los 8 lectores** (pasos desde cada mudanza hasta el primer bocado A+C del linaje dentro
del oasis nuevo; 4 mudanzas × 8 lectores = 32 latencias; "nunca" cuenta T). Física de sólo lectura del mundo (`latencias` de `OasisC`).

## 6. La letra (por código: `lee_serie`)
Pareado por semilla, MENOR gana, **empate en contra**. Umbral de pares 14/20.
- **G_var_pares**: pmix < mix en ≥ 14/20. **G_var_magnitud**: mediana (sobre semillas) de pmix/mix ≤ 0.85.
- **G_contenido**: pmix < pmixbar en ≥ 14/20. **G_mudo**: pmix < pmudo en ≥ 14/20.
- **NO SE LEE**: falla cualquier validez (sec. 7). Va antes que todo.
- **FUNCIONA**: las cuatro puertas.
- **HAY ALGO MODESTO**: G_contenido Y G_var_pares (falla la magnitud o el mudo).
- **NO**: lo demás.
- **En el umbral**: alguno de los tres conteos de pares a ±1 de 14.

**Ajuste respecto de la letra propuesta por el coordinador** ("MODESTO si pasa contenido y una de las otras"), por el nulo simulado
(`nulo_pisa.py`, 200 000 series por escenario, sd del log entre semillas 0.25; medida 0.227 y 0.238 en el brazo `sen` de las dos series de
juntos): si la variante NO hace nada (pmix = mix) pero el antípoda y el mudo son peores —lo que ya se ve en el humo—, esa letra da MODESTO o
más el **85–94 %** de las veces. Por eso MODESTO exige G_var_pares. La letra del coordinador se imprime como descriptivo ("no decide").

| escenario (razones verdaderas) | P(FUNCIONA) | P(MODESTO) | P(NO) |
|---|---|---|---|
| nulo total (4 brazos iguales) | 0.001–0.002 | 0.009 | 0.990 |
| nulo de la variante (pmix = mix; antípoda ×1.3, mudo ×1.8) | 0.012–0.021 | 0.035–0.046 | 0.943 |
| nulo de contenido (pmix = pmixbar; mix ×1.3, mudo ×1.8) | 0.054–0.057 | 0.001 | 0.943 |
| efecto en el borde (pmix/mix 0.85) | 0.39–0.43 | 0.13–0.21 | 0.36–0.48 |
| efecto del humo (pmix/mix 0.77) | 0.77–0.86 | 0.07 | 0.07–0.16 |
| efecto grande (pmix/mix 0.65) | 0.99 | 0.00 | 0.01 |

(Rango = sin pareo y con correlación 0.3 entre brazos.) **Falso positivo máximo declarado: 5.7 % para FUNCIONA** (lo gobierna una sola
puerta de 14/20 bajo el nulo de contenido) y ≤ 5.8 % para "MODESTO o más" bajo el nulo de la variante. Potencia 0.77–0.86 si el efecto es el
del humo; 0.39–0.43 si está en el borde. El modelo del nulo es lognormal i.i.d. entre semillas: no usa datos de los brazos mixtos (no existían
a n 20); es una aproximación, no una permutación de datos reales.

**Correcciones de la auditoría previa (antes del commit y de cualquier dato de serie; no cambian ningún cálculo ni la letra):**
- H-1: la fila "efecto del humo (pmix/mix 0.77)" está mal etiquetada, aquí y en `nulo_pisa.py`. `mix` NUNCA se corrió en las semillas del
  humo; el 0.77 es **pmix/sen9** (989.5/1261 y 768/1014), y sen9 son 9 lectores sin explorador. La razón pmix/mix no está medida a T 100k; la
  única pareja pmix/mix que existe (humo de main, T 20k) fue en contra (1.65). La "potencia 0.77–0.86" es por tanto para un efecto supuesto.
- H-2: las valideces V1, V5, V6 y V7 del runner miran también los brazos descriptivos sen9 y pisa9 (n 10). Una corrida descriptiva incoherente
  daría NO SE LEE: es más estricto que lo escrito en el §4 y se acepta así. La completitud sólo mira los cuatro brazos de la letra.
- H-4: "nunca llega" cuenta como latencia T (100 000), igual en todos los brazos.

## 7. Validez (cualquiera falla → NO SE LEE)
- V1 completa: 0 abortos, los 4 brazos de la letra con n filas, `coherente` del juez.
- V2 mundo: 4 mudanzas, mueve 20 000 y c_e 0.01 en la salida del mundo.
- V3 estado: la lista de carros de cada corrida == la del brazo con el explorador en i mod 9; shas de carros; sondas activas.
- V4 **el explorador llega antes**: latencia mediana del explorador < la de sus lectores en ≥ 90 % de las corridas de cada brazo de la letra.
- V5 pisadas: > 0 en cada corrida de los brazos PISA (sonda ≥ telemetría); 0 y sin contador en `mix` / `sen9`.
- V6 señal viva: lecturas > 0, siembras > 0 y escrituras > 0 en cada corrida.
- V7 sólo uno pregunta: `pg_exc` > 0 en el explorador y nulo en los lectores.
- Antes de correr (no crea carpeta si falla): shas, carros == constructor, e identidad corta (variante apagada == `O1_TODO_SEN`; mixto de 9
  iguales == `corre_juntos.tarea`; sondas no perturban; pmix != mix).

## 8. Trampas que se reportan SIEMPRE junto al veredicto (no entran en la letra)
1. **Mundo que se come la comida**: `mundo_AC` por brazo (en P7 sin mudanza, 1 semilla, la variante lo subió de 8.7 a 11.9).
2. **Cruce y fundadores de los lectores** por brazo (acierto sin balancear: llegar antes no vale si el linaje cruza menos).
3. **Rumor**: fracción de pisadas (periodos tras mudanza) que apuntaban al oasis VIEJO.
4. **Efecto lateral de `_lg_hereda`** (adopta la memoria heredada si `nl.sum() == 0`): número de adopciones en carros que ya habían
   aprendido (`lg_apr > 0`), imposibles en el original. En el humo de main y en el arnés: 0.
5. Sitios fijos: el explorador rota (i mod 9). Canal simétrico: el control antípoda oye lo mismo y siembra en el lado opuesto.
6. Descriptivos `sen9` y `pisa9` (n 10).

## 9. Candados y regla de parada
`--serie/--replica`: T, n, brazos, mueve y semillas fijos; pool ≤ 2; todo commiteado y sin cambios vs HEAD (preregistro, runner, constructor,
carros, `corre_pisa.py`, `corre_mixto.py` y lo que éste fija); no se re-corre una carpeta con veredicto; `--reanuda` salta las pruebas ya
escritas (JSON por corrida, escritura atómica; un JSON truncado se re-corre). **Réplica sólo si la serie da FUNCIONA, HAY ALGO MODESTO, o NO
en el umbral (±1)**, con el mismo sha de runner. Hacen falta serie y réplica concordantes para declarar.

## 10. Predicciones firmadas (creador, antes de la serie)
- pmix < mix en **15/20** (rango 12–18); mediana de pmix/mix **0.80** (rango 0.65–0.95).
- pmix < pmixbar en 17/20 (rango 14–20); pmix < pmudo en 17/20 (rango 14–20).
- Latencia mediana de lectores: pmix 900 (750–1100) · mix 1200 (1000–1450) · pmixbar 1450 (1200–1900) · pmudo 1800 (1300–2600).
- Veredicto: FUNCIONA 0.45 · MODESTO 0.15 · NO 0.40. Riesgo principal: `mix` nunca se pareó con `pmix`; en el humo de main (T 20 000,
  mueve 5000, 1 semilla, otro mundo: no cuenta) pmix quedó PEOR que mix (2225 vs 1344.5).
- Trampas: mundo_AC de pmix mayor que el de mix por 0.3–1.5; fracción de pisadas al oasis viejo 0.10–0.35; `_lg_hereda` tras vivir: 0;
  cruce de lectores de pmix no menor que el de mix en más de 8 (de 160).
- La ficha (≤ 700): seguirá sin alcanzarse.

## 11. Qué lo refuta
NO en la serie (fuera del umbral) cierra el peldaño sin réplica. FUNCIONA o MODESTO en la serie que no se repite en la réplica: no se declara.
Si G_var pasa pero G_contenido falla: la variante acelera por algo que no es el contenido de la señal (p. ej. borrar memoria vieja) y la
lectura es NO para este peldaño.

## 12. Comandos y costo
    python experimentos/organelos/escalera/mixto/corre_pisa_serie.py --serie --pool 2      [--reanuda]
    python experimentos/organelos/escalera/mixto/corre_pisa_serie.py --replica --pool 2    [--reanuda]
    python experimentos/organelos/escalera/mixto/corre_pisa_serie.py --lee <carpeta>

Costo medido en un proceso: 92–112 s por corrida de T 100 000 (16 corridas de los humos y la sonda). Serie: 80 + 20 = 100 corridas ≈ 85 min
con pool 2; réplica: 80 corridas ≈ 67 min. Total ≈ 2 h 30 min. El runner no escribe en `BITACORA.md`: la fila la registra el coordinador.
