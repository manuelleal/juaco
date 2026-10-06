# PREREGISTRO — F2 "UN GEN POR PARTO" (o1_libre_f2, 1-oct-2026) — EXPLORATORIO con letra fija

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y
réplicas). Origen: ficha F2 de `investigacion_20261001/ENTREGA_1_reactor.md` y `AUDITORIA_F0.md`. Rama `o1-libre` (HEAD `23a6c83d`),
carpeta `experimentos/organelos/o1_libre_f2/`. El bloque `o1_libre` (cerrado: NO) **no se toca**: se importa y se construye por anclas.
No apunta al tronco. Numeración de esta rama: ERR-161 a 169 (no se usa ninguno si no cambian criterios tras ver datos).

## 1. Hipótesis
En o1_libre la selección sostuvo a O1 frente a la deriva pero no lo superó (lib cruza 55 y 39 contra 66 y 69 de O1; conquista 4/10 ×2).
**F2: lo que tapa la subida es la carga de mutar los 14 genes en cada parto, no la selección.**

## 2. Mecanismo mínimo y memoria nueva
**Único cambio:** cada evento de mutación muta UN gen elegido al azar uniforme entre los 14, con la misma σ_j (0.03 × max(1, |fábrica_j|))
y el mismo recorte. Los otros 13 pasan iguales. "Evento" = cada parto y cada fundador o refundador (`_ps_muta` es la única puerta de
mutación del carro; en o1_libre los fundadores también mutaban los 14). **Memoria nueva heredable: cero.** Estado nuevo: una rng propia
por cuerpo (`[PS_SEMILLA, índice, instancia, 7724]`).
- Carro `carros/O1_LIB_F2.py` = `o1_libre/carros/O1_LIB.py` (sha `ff30214f59ed36d8`) + 11 líneas por 4 anclas (`construye_o1_lib_f2.py`),
  con la perilla `PS_UNGEN` (0 = O1_LIB bit a bit; 1 = un gen). Con `PS_UNGEN` 1 la rng vieja (`_psrng`) sólo elige la entrada de siembra o
  colonia, igual que antes; la mutación usa la rng nueva.
- **Todo lo demás es o1_libre, importado sin tocar** (`corre_o1_libre.py` `98d3a103a1fdde3b`): mundo `pista_libre` (estación, parche,
  quieto), 9 linajes, siembra de 90 partos con t ≥ 50k, colonia de 50, cadenas `lib` (PS_LEE 1) y `neu` (PS_LEE 0), 3 pasajes de 100k,
  pruebas de 100k `lib`, `neu`, `o1`, `mix`, `mixn`, 10 índices, casillas alternas, σ 0.03.
- **Consecuencia declarada del recorte:** un evento que cae en un poder que está en 0 con paso negativo no cambia nada (≈ 4/14 × 1/2 = 14 %
  de los eventos al inicio; el arnés U6 mide 615 de 4200). Es la misma regla de recorte de o1_libre.
- **Semillas nuevas** (grep 1-oct: `744xxx` no aparece en `.py/.md/.txt/.log` de `PROYECTOS/JUACO`; o1_libre usó `734xxx`): serie pasajes
  `744000 + 10 i + p`, pruebas `744201 + i`; réplica `744300 + 10 i + p` y `744501 + i`; práctica `744900–744999`.

## 3. Control que puede ganar y predicción rival
- **Control histórico declarado (no se re-corre):** el montaje de 14 genes por parto, medido ×2 en o1_libre (serie `i734201–210` y réplica
  `i734501–510`, letra `efcccd35`): R0 mediano del neutro 0.795 y 0.620; cruces lib/o1/neu 55/66/30 y 39/69/32; PC 4/10 ×2. **Reserva:** es
  un control de otras semillas y otro día, no pareado; por eso las puertas de F2 se leen contra `o1` y `neu` de la MISMA serie, y el histórico
  sólo fija el nulo de PF1.
- **Rival PURGA** (organelos: "mutación ÷10 = PURGA"): con menos carga la selección borra variación antes de sumar. Predice: sin conquista,
  y el reloj mutacional de `lib` queda en ≤ la mitad del de `neu` (`firma_purga`, descriptiva). Si aparece, se dice.
- **Rival "trivial"** (el creador la cree la más probable, §8): con un gen por parto casi nada muta en 3 pasajes; `lib` y `neu` son casi O1
  de fábrica, el déficit desaparece por eso y no hay conquista. **PF1 + PF2 solas no distinguen esto de la hipótesis** (§5).

## 4. PUERTA DE VALIDEZ NUEVA: los dos relojes (se miden y se reportan por separado; no se habla de "generaciones")
**(a) Reloj mutacional por gen** (`reloj()`): en la `siembra_final`, n = media sobre los 10 genes de O1 de E[((g − fábrica)/σ_j)²]. En
o1_libre el neutro dio 11.87 (serie) y 11.65 (réplica) (el arnés R1 reproduce la auditoría de F0). Ahí n = eventos de mutación en la
ascendencia, porque cada evento tocaba los 14 genes. **Con un gen por evento se espera n por gen ≈ 12/14 ≈ 0.86** (el neutro decide como O1
en los dos montajes: la demografía del neutro no cambia). Se reportan n por gen y "eventos equivalentes" 14·n, en `neu` y en `lib`.
- **V8 (validez):** mediana de n por gen del neutro ≤ 3.0. Si sale ~12, la perilla no actuó: NO SE LEE.
- **Qué implica para la potencia (honesto):** el reloj por gen cae 14 veces. En o1_libre, con ~14 eventos por gen, lib movió PISO +0.10
  (3.3 σ) y MEM +0.06. Con ~0.9 eventos por gen el desplazamiento posible por gen es del orden de 1 σ (0.03). Un poder dado recibe al
  menos un evento en el 59 % de las ascendencias (1 − (13/14)¹²) y ≥ 3 eventos en ~5 %. **PP (dif. ≥ 0.05) queda prácticamente fuera de
  alcance en 3 pasajes; PC por adaptación nueva, también.** En 3 pasajes F2 **sí** puede informar de: si la carga explica la degradación del
  neutro (PF1) y el déficit de lib frente a O1 (PF2). **No** puede informar de si "sin carga los poderes suben": un NO de PC/PP aquí no
  dice nada de los poderes.
- **Lo que haría falta para igualar el reloj por gen de o1_libre:** 14 × 3 = 42 pasajes por cadena (≈ 84 M de pasos sólo de cadenas por
  serie, > 25 h con pool 2): no cabe. Intermedio posible: 6 pasajes (n por gen ≈ 1.7), ≈ 6.2 h por serie con pool 2. **No se hace en este
  bloque; se propone sólo si la serie da MODESTO por carga, como bloque aparte con su preregistro.**

**(b) Reloj de recambio** (por pasaje y brazo, medianas de cadenas): `fund_colonia`, `fund_de_siembra`, `Ne_linajes` y `padres_distintos`
de cada siembra, partos y eventos de mutación. Referencia o1_libre: colonia serie lib 215.5 / neu 132, réplica lib 273 / neu 175;
Ne_linajes 8.1–8.3 (máximo 9; no es Ne genético); padres distintos 23.5–24. El reloj de selección entre linajes sigue sin medirse
(AUDITORIA_F0 H-2): se declara.
- **V7 (validez):** en cada pasaje y cada prueba con O1_LIB, la telemetría del carro `ungen` (sólo existe con `PS_UNGEN` 1) tiene eventos
  > 0, `cambia_1 + cambia_0 == eventos`, `cambia_1 > 0`; el estado anota `ungen` 1 y el sha del carro F2.

## 5. LA LETRA (por código: `corre_o1_libre_f2.lee_serie`, n = 10 índices)
**Validez (todas o NO SE LEE):** V1–V6 de o1_libre tal cual (completa sin abortos; O1 vive, R0 ≥ 0.50; el mundo actúa; la siembra actúa;
perillas; el neutro no activa poderes) + V7 + V8. Extinción de cadena = dato (ERR-160 v).

| puerta | código | umbral | nulo declarado (regla 15) |
|---|---|---|---|
| **PF1** el neutro no se degrada | mediana por índice del R0 real mediano de la prueba `neu` | ≥ 0.90 | montaje de 14 genes: 0.795 y 0.620 (×2, 0/2 pasan); margen ≥ 0.10. O1 de fábrica: 0.981 ×2 |
| **PF2** lib no queda bajo O1 (no inferioridad con margen; auditoría H-1) | suma de linajes que cruzan (de 90): `lib` − `o1` | ≥ −5 (`MARGEN_PF2` = 5) | **Nulos como SUPUESTO, con sd ≈ 4 de la diferencia (calibración débil: sale de dos datos, o1 = 66 y 69):** bajo "el déficit persiste" (−11) pasa ~0.07; bajo "lib ≡ O1" pasa ~0.89. PF2 NO es una puerta de superioridad |
| **PC** conquista | `mix`: nacimientos reales medios lado lib − lado O1 > 0 | ≥ 8/10 | 0.055 si lib equivale a O1; o1_libre 4/10 ×2 |
| **PN** no es sólo deriva | conquista `mix` > conquista `mixn` | ≥ 8/10 | 0.055; cuenta para "en el umbral" sólo si PC ≥ 7 (ERR-160 i) |
| **PP** un poder se prende | gen en la siembra final: lib > neu en ≥ 8/10 cadenas y dif. de medianas ≥ 0.05 | | ~0.18 por multiplicidad; **sin potencia en F2 (§4)**: se calcula, no se exige |

- **FUNCIONA** = válido y PF1 y PF2 y PC y PN. (Quitada la carga, la selección le gana a O1 en el mismo mundo y no es deriva.)
- **HAY ALGO MODESTO** = válido y (PF1 y PF2) o PC o PP. Matices por código:
  - PF1 y PF2 sin PC ni PP: matiz **"SOLO CARGA, NO SUBIDA"** y clave `solo_carga: True` en el resumen (auditoría H-2; el veredicto
    sigue siendo MODESTO para el orden de `--bloque`). **Esto NO apoya "la selección sube sin carga": es compatible con la rival trivial
    (bajo "lib ≡ O1" PF2 pasa ~0.89). No se cita sin réplica y nunca como subida.**
  - PF1 y PF2 con PP y sin PC: "un poder se prende sin conquista; el déficit de lib frente a O1 no aparece".
  - PF1, PF2 y PC sin PN: "conquista, pero la deriva sola hace lo mismo".
  - PC sin (PF1 y PF2); o sólo PP: matiz propio.
- **NO** = válido y nada de lo anterior. Matiz: si PF1 pasa y PF2 no, "la carga se quitó y lib sigue bajo O1: la carga no era lo que
  tapaba" (refuta F2); si PF1 no pasa, "un gen por parto no quita la degradación del neutro" (refuta el mecanismo).
- **En el umbral:** las reglas de o1_libre (PC ±1 de 8; PN ±1 sólo si PC ≥ 7; PP) o |R0 del neutro − 0.90| ≤ 0.03 o |(lib − o1) − (−5)| ≤ 4 cruces (a ±4 del umbral de PF2).
- **Descriptivos fijados antes de datos:** `lib_supera_o1_con_margen` (lib − o1 ≥ +7 cruces; nulo ~0.05), `firma_purga`, los dos relojes,
  la letra vieja de o1_libre sobre estos datos, y todo el descriptivo de o1_libre.

## 6. Regla de parada, réplica y bloque
Réplica (semillas `7443xx`/`7445xx`) sólo si la serie da FUNCIONA, MODESTO o NO en el umbral; mismo sha de runner. Bloque = el menor de los
dos veredictos. Un NO fuera del umbral cierra el bloque sin réplica. NO SE LEE por abortos: `--reanuda` reintenta sólo los abortos; NO SE
LEE por V2–V8: se cierra como NO SE LEE, no se arregla tras ver datos sin ERR.

## 7. Qué refuta
- F2 queda **refutada** si PF1 pasa y PF2 no (lib − o1 < −5: la carga se quitó y el déficit sigue), o si PF1 no pasa.
- F2 queda **sin apoyo** (no refutada) si PF1 y PF2 pasan sin PC ("SOLO CARGA, NO SUBIDA"): el déficit no aparece; no hay subida.
- **Refutada / sin apoyo = relativo al control histórico no pareado; no se escribe "la carga explica" sin `PS_UNGEN` 0 pareado**
  (auditoría H-3). Los nulos de PF2 son un SUPUESTO con sd ≈ 4 (dos datos): −11 pasa ~0.07; lib ≡ O1 pasa ~0.89.
- F2 queda **apoyada** sólo con FUNCIONA ×2.
- Prohibido: "la selección sube/inventa sin carga" sin PC ×2; "los poderes no suben ni sin carga" (PP sin potencia); comparar "generaciones".

## 8. Predicciones firmadas (creador, ANTES del humo; ya vistos: el arnés con T ≤ 6000 y los datos de o1_libre)
| # | predicción | rango | p |
|---|---|---|---|
| Q1 | V1–V8 pasan | | 0.85 |
| Q2 | PF1 (R0 mediano del neutro ≥ 0.90) | [0.93, 0.985] | 0.85 |
| Q3 | reloj por gen del neutro (mediana) | [0.5, 1.5] | 0.80 |
| Q4 | PF2 (lib ≥ o1 en cruces) | lib − o1 en [−8, +6]: 0.75 | 0.45 |
| Q5 | PC (conquista ≥ 8/10) · PN | | 0.07 · 0.07 |
| Q6 | PP | | 0.03 |
| Q7 | `firma_purga` | | 0.15 |
| Q8 | lib supera a o1 con margen (+7) | | 0.05 |
| Q9 | suma de cruces de `o1` | [60, 75] | 0.75 |
| Q10 | suma de cruces de `neu` ≥ 55 (o1_libre: 30 y 32) | | 0.75 |
| Q11 | `fund_colonia` mediana por pasaje: neu en [100, 190]; lib en [100, 220] | | 0.65 |
| V | FUNCIONA / MODESTO / NO / NO SE LEE | | 0.04 / 0.42 / 0.42 / 0.12 |

La ficha firmaba 0.3 de conquista y 0.7 de que el neutro deje de degradarse. **Firmo 0.07 y 0.85**: la caída ×14 del reloj por gen (§4)
hace casi mecánico lo segundo e improbable lo primero.

## 9. Costo y tamaño (declarado ANTES de datos; no debilita la letra)
- **`mixA` NO se corre** (era descriptiva y fuera de la letra en o1_libre; separa poderes de perillas, y aquí los poderes casi no se mueven).
  Por índice: 6 pasajes + 5 pruebas = 11 corridas de 100k (o1_libre: 12). N_IND = 10, NPAS = 3, T y umbrales: los de o1_libre.
- o1_libre midió 16 223 s por serie con pool 2 (120 corridas, PC cargada) → ≈ 135 s por corrida. **F2: 110 corridas ≈ 4.1 h con pool 2**
  (más con la PC cargada: a las 07:30 había 7 procesos python). Réplica: igual.
- **El PC se apaga a las 14:00.** Si no cabe entera, la serie es **parcial y retomable**: JSON por pasaje y por trabajo (escritura atómica),
  `--serie --pool 2 --reanuda` salta lo hecho. Orden de la cola: 60 pasajes y las 10 pruebas `o1` primero, luego las 40 pruebas. **Entre el
  corte y la reanudación no se corre `--lee` ni se abre ningún JSON de prueba; la letra no cambia.** Un pasaje cortado a medias se repite
  entero (misma semilla: mismo resultado).

## 10. Las cuatro trampas
- **Canal simétrico:** igual que o1_libre (pizarra pública; colonia = canal de genes declarado, con la misma asimetría en las mixtas: un
  O1_LIB extinto se refunda desde la colonia, un O1 desde fábrica). F2 no añade canal.
- **Acierto sin balancear:** medidas físicas del juez (R0 real, `cruza_real`, nacimientos reales). Ninguna tasa de acierto.
- **Mundo que se come la comida:** `mundo_AC` y fracción en el parche por brazo, como en o1_libre.
- **Sitios fijos:** parche sorteado por semilla y móvil; semilla nueva por pasaje y prueba; casillas alternas por índice.
- **Trampa propia de F2:** "lib ≥ o1" puede pasar porque no mutó nada. Se mide (reloj, V8) y se declara en la letra (PF2 no es superioridad).

## 11. Instrumento, arnés, humo
```
python experimentos/organelos/o1_libre_f2/construye_o1_lib_f2.py --verifica
python experimentos/organelos/o1_libre_f2/identidad_o1_libre_f2.py
python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --humo
python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --humo --reanuda
python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --serie --pool 2 2>&1 | tee experimentos/organelos/o1_libre_f2/serie_pool2.log
python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --serie --pool 2 --reanuda 2>&1 | tee -a experimentos/organelos/o1_libre_f2/serie_pool2.log
python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --replica --pool 2     # sólo por §6
python experimentos/organelos/o1_libre_f2/corre_o1_libre_f2.py --bloque <resumen serie>,<resumen réplica>
```
- Runner: importa `corre_o1_libre` y lo redirige en memoria al carro F2 (ningún archivo de o1_libre cambia). Candados: `git_limpio` de este
  preregistro, runner, constructor y carro F2, y de los 5 archivos de o1_libre que se importan; shas fijados; `identidad_corta` en cada
  corrida real (incluye O1_LIB_F2 con `PS_UNGEN` 0 == O1_LIB, salida entera y telemetría, T 3000); se niega si ya hay veredicto.
- Arnés y humo: resultados en §12 (escrita después; nada de §1–§10 cambia).

## 12. Arnés y humo (ESCRITA DESPUÉS del arnés y del humo, 1-oct 07:38–07:50; NO cuentan; nada de §1–§11 cambia)
La versión de este preregistro que registran las cabeceras de los dos logs del humo es sha `56ae42fc5d1f48f5` (§1–§11 como arriba).
- **Arnés `identidad_o1_libre_f2.py` → `identidad_o1_libre_f2_salida.txt`: ARNES PASA, 69/69 (198.5 s), a la primera.** Identidad bit a bit
  con `PS_UNGEN` 0 contra el O1_LIB de o1_libre: salida ENTERA de la pista y telemetría en el mundo del bloque (T 6000, 61 partos, 24
  refundaciones por colonia), neutro con siembra (T 3000), pista vieja (T 2000) y 200 partos sin pista; control: con `PS_UNGEN` 1 cambia. Un
  gen: 300 fundadores y 4200 partos cambian exactamente 1 gen; elección uniforme (260–331 por gen, esperado 300); paso z con sd 1.007; desde
  fábrica 615/4200 eventos no cambian nada (poder clavado en 0). Reloj: `reloj()` da 11.87 y 11.65 en el neutro de o1_libre (los números de
  la auditoría de F0) y 0.866 en una simulación de 12 eventos de un gen (esperado 0.857). Letra: 30 casos sintéticos. Ruta Pool con Pool
  falso, candado y regla de parada. **No probado: un Pool real** (prohibido al creador); se simuló el import de un hijo `spawn`
  (`run_name='__mp_main__'`): el hijo queda redirigido al carro F2. Si no lo quedara, V7 daría NO SE LEE.
- **Humo** (práctica 744990–744998; `humo_salida.txt` 6 corridas / 88 000 pasos; `humo_reanuda_salida.txt` 3 corridas / 60 000 pasos;
  carpeta `datos/humo/humo_20261001_074322/`; runner `bb40e2a3feeffb37`): 0 abortos, V1–V8 True. A T 20k: o1 6/9 (R0 0.90), lib 6/9
  (0.909), **neu 7/9 (0.917)** (en el humo de o1_libre el neutro daba 1/9 y R0 0.44); conquista mix +0.65, mixn −0.15; poderes ≤ 0.006 en
  lib y en neu. Reloj por gen tras 2 × 12k: lib 0.22, neu 0.20 (≈ 3 eventos equivalentes). Con 1 índice la letra escalada dice "FUNCIONA
  en el umbral": **no cuenta** (umbral escalado a 1/1; T corto).
- **Costo medido (un proceso, PC con otros 7 procesos python):** pasaje ≈ 2.15 ms/paso (100k ≈ 215 s); prueba ≈ 2.1–2.9 ms/paso (100k ≈
  210–290 s). Por índice 6 × 215 + 5 × 240 ≈ 2 490 s de CPU; serie ≈ 24 900 s → **≈ 3.5 h con pool 2 sin contención; ≈ 4.1 h al ritmo que
  midió o1_libre con la PC cargada**, más ~35 s de identidad corta por arranque.
- Shas al cierre del creador: en el informe (el del preregistro es el que quede commiteado).

## 13. Cambios por auditoría (LISTO CON CAMBIOS), ANTES de datos (1-oct, ~08:00–08:30). Sólo existían el arnés y el humo (no cuentan)
- **H-1 (toca la letra):** PF2 pasa de "lib − o1 ≥ 0" a **"lib − o1 ≥ −5"** (`MARGEN_PF2` = 5); "en el umbral" de PF2 pasa a ±4 alrededor
  de −5. Nulos escritos como SUPUESTO (§5, §7). `lib_supera_o1_con_margen` (+7) sigue descriptivo. Contrafáctico en el humo (1 índice, no
  cuenta): lib 6 vs o1 6, PF2 pasa con las dos reglas; veredicto del humo igual. Arnés: 4 casos de frontera (−5 pasa, −6 no; −1 y −9 dentro
  del umbral). **Es un cambio de letra después del humo y antes de datos: por el precedente de ERR-160 le corresponde ERR-161; lo asigna y
  registra el coordinador.**
- **H-2:** rama PF1 y PF2 sin PC ni PP: veredicto intacto (MODESTO), matiz "SOLO CARGA, NO SUBIDA", clave `solo_carga` en la letra y en
  el resumen.
- **H-3:** frase de §7 sobre el control histórico no pareado.
- **H-5:** `trabajo()` llama a `comprueba_f2()` antes de cada trabajo (y `main` antes de crear la carpeta): sha del carro cargado ==
  `SHA_F2` y `PS_UNGEN` queda en 1 tras `_pon_lib`; si no, `RuntimeError` inmediato que corta la serie (no es un "aborto" de trabajo).
- **H-7:** el bucle del Pool vigila los pids de los hijos; si cambian (un hijo murió y el Pool lo reemplazó, su trabajo no vuelve), corta
  con rc 2, sin resumen ni veredicto, y pide `--reanuda`. **Probado sólo con un Pool falso (arnés P7), no con un Pool real.**
- **Predicciones re-firmadas por el cambio de PF2 (antes de datos; el humo ya visto):** Q4 PF2 (lib − o1 ≥ −5): **0.80** (antes 0.45 con
  ≥ 0; el rango de lib − o1 no cambia). V: FUNCIONA 0.04 / MODESTO 0.68 / NO 0.16 / NO SE LEE 0.12 (antes 0.04 / 0.42 / 0.42 / 0.12). Las
  demás no se mueven.
- Arnés y humo repetidos tras los cambios: números en el informe del creador y en las salidas `identidad_o1_libre_f2_salida.txt`,
  `humo_salida.txt`, `humo_reanuda_salida.txt` (las anteriores quedan como `*_v1.txt`).
