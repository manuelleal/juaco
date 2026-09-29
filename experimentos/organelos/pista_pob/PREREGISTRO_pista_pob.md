# PREREGISTRO (EXPLORATORIO con puerta hacia serie) — PISTA_POB: población de pistas con depósito de los que parieron (29-sep-2026, creador)

Misión: llegar a la AGI por este camino. Principio del director: que la selección construya el órgano, no nosotros.
Aprobado por el director en su **versión barata**. Escrito con el arnés corriendo y ANTES de lanzar el humo y de ver cualquier número de pista_pob.

## 0. Por qué
BLOQUES_PISTA (28-sep, NO ×2 rondas): con 9 cuerpos y 100k la selección no tiene material (deriva; 1–3 linajes por semilla se refundan cientos de
veces con fundador ingenuo). `pista.N_MAX = 9` y un cuerpo vivo por linaje: más población sin tocar la pista **no existe dentro de una corrida**.
PISTA_POB la construye por fuera: **K = 8 copias de la pista vieja en paso fijo**, unidas sólo por un depósito de las memorias de los que parieron.

## 1. Hipótesis
Si el refundador de un linaje sale del depósito de los que PARIERON en 8 pistas (72 cuerpos a la vez) en vez de ser ingenuo o salir del banco de su
propio linaje, la selección entre pistas arma listas de reglas (V143_BQ2) que, sembradas en la pista vieja, hacen **cruzar más linajes** que el mismo
transporte sin selección (neutro) y que los pasajes de bloques_pista (bloq_pas).

## 2. Mecanismo y memoria nueva
- `experimentos/carrera_escuderias/pista_pob.py` (archivo NUEVO; pista.py y juez.py sin tocar, shas fijados 9f47c65e438e0ff4 / 6a68f640a7832f12).
  `run_gen` = `pista.run` transformado por **5 anclas** (cada una exactamente una vez; fuente transformada 7b05c9615ee40483): generador que cede cada
  paso + ganchos inicio / parto / fundador. Se ejecuta con los globales de pista (Linaje, _diag, _estado, cfg_fabrica… importados, no copiados).
- Copia c: semilla `seed` (c = 0) o `10**8 + 1000*seed + c`; sus corrientes rng son las de `pista.run` con esa semilla. Cada copia carga su PROPIO
  módulo del carro (canal oculto `_BQ_BANCO` cerrado; arnés I2 lo prueba con un control que debe fallar).
- Depósito `pool[i]` (por índice de linaje): deepcopy de la memoria de `al_parir` marcada con la copia, FIFO tope 50·K = 400; los partos del paso t
  se publican al terminar t en las K copias (simétrico).
- Fundación (sólo con fundador limpio, ENMIENDA 5): la pista ya hizo `crea(ctx)`; si `pool[i]` tiene entradas de OTRA copia → migrante:
  `nace(memoria=…)` con el `rng_hijo` normal de la pista y el sorteo con rng NUEVA `[semilla_c, i, 16, k]` (pista usa 11–15). Si no → fundador
  limpio como en la vieja. El migrante **cuenta como fundador** (no suma nacimientos reales).
- **Memoria nueva: cero en el carro** (V143_BQ2 sin cambios, sha 183fb81cf6ad520c, tasas BQ_C de la ronda 2 = corre_bp.CFG0). La cámara guarda ≤ 400
  listas por índice.

## 3. Brazos (índice j = 1..5)
| brazo | cámara (K 8, T_evo 50 000, semilla 59800+j) | papel |
|---|---|---|
| pob_sel | migrante = entrada al azar de pool[i] con marca ≠ c (sólo entra quien parió; ya trae la mutación de `al_parir`) | CANDIDATO |
| pob_neutro | migrante = reglas del cuerpo VIVO del linaje i en otra copia al azar (haya parido o no; foto del final del paso anterior) + UNA pasada del mismo operador de mutación del carro. **Misma tasa**: migra si y sólo si pool[i] tiene entradas de otra copia (el depósito se lleva igual) | CONTROL que puede fallar (NO puro: ver sec. 11) |
| v143 | V143 en la pista vieja, 59201–59205, T 100k (nuevo) | validez |
| termo, bloq2, bloq2aza, bloq_pas, o1 | JSON guardados de bloques_pista/datos/explora_T100000 (mismos shas; arnés I4 reproduce bloq2 y bloq_pas s59201 bit a bit) | referencias pareadas |

## 4. Medida OFICIAL (fuera de la cámara)
Al final de la cámara, por linaje: fotos del depósito + los 8 vivos cada 1000 pasos en los últimos 5000 (5 fotos); 50 listas al azar sin reposición
(rng `[seed, i, 17, 0]`), sin listas vacías → siembra (≤ 450). Se carga con `corre_bp.prepara(siembra=…)` a través de `corre_bp.tarea(59200+j, 'bloq2',
100 000, siembra)` (la MISMA función que hizo bloq_pas): la pista vieja, el juez, fundador limpio, letra ENMIENDA 5. **Medida principal: linajes que
cruzan (`cruza_real`) de 9 por índice**; R0 real mediano al lado.

## 5. Predicciones (firmadas antes del humo)
| # | predicción | p |
|---|---|---|
| Q1 | suma de cruzan (5 índices × 9) pob_sel en [18, 28] | 0.65 |
| Q2 | suma de cruzan pob_neutro en [16, 26] | 0.65 |
| Q3 | pob_sel > pob_neutro en ≥ 4/5 índices | 0.15 |
| Q4 | pob_sel ≥ bloq2 (4, 3, 3, 6, 5; BQ2 sin depósito) en ≥ 4/5 (antes: ≥ bloq_pas, p 0.35; cambiado por auditoría H-2) | 0.30 |
| Q5 | (PROXY) en la cámara, migrantes / (migrantes + limpios) ≥ 0.90 en los dos brazos y todos los índices (la letra original, 'fundadores tras t = 5000', no es calculable con lo guardado) | 0.80 |
| Q6 | v143 R0 real mediano en [0.40, 0.80] | 0.80 |
| Q7 | fundadores por linaje (mediana de 9) en la prueba pob_sel < pob_neutro en ≥ 3/5 | 0.35 |
Veredicto que espero: **NO** (p 0.70), MODESTO (0.20), FUNCIONA (0.10). O1 mayoría 5/5 ya se conoce (JSON guardados): es condición, no predicción.

## 6. Puerta (calculada por código: `corre_pista_pob.lee`)
- **FUNCIONA (pasa a serie)** = pob_sel > pob_neutro en cruzan en ≥ 4/5 índices **Y** pob_sel ≥ bloq2 (misma BQ2, sin depósito) en ≥ 4/5. bloq_pas se imprime al lado y NO decide.
- **HAY ALGO MODESTO** = pob_sel > pob_neutro en ≥ 3/5, **o** suma de cruzan pob_sel ≥ pob_neutro + 5.
- **NO** = cualquier otra cosa.
- **Validez (si falla: NO APLICA)**: 0 abortos; los 10 trabajos completos; v143 R0 real mediano (mediana por semilla) en [0.40, 0.80]; O1 mayoría que
  cruza ≥ 4/5; arnés pasado (la salida dice PASA y cita el sha actual de pista_pob.py).

## 7. Qué lo refuta
pob_sel ≤ pob_neutro en ≥ 3/5 y suma de cruzan pob_sel < pob_neutro + 5: el depósito de los que parieron no selecciona nada que la pista vieja premie.
Si pob_sel ≈ pob_neutro y ambos > bloq2: es el TRANSPORTE (la población), no la selección.

## 8. Cuatro trampas
1. **Canal simétrico**: los dos brazos tienen el mismo depósito, la misma tasa de migración (misma condición) y la misma medida; lo único que cambia
   es de dónde sale el migrante. Los partos se publican al final del paso para las K copias; la foto del vivo (neutro) es del paso anterior para todas.
   El canal oculto de módulo está cerrado (un módulo por copia; I2 con control que debe fallar).
2. **Acierto sin balancear**: la medida es un conteo pareado por semilla de prueba contra un control con la misma maquinaria; las tasas base se conocen
   (cruzan 45 linajes: termo 20, bloq2 21, bloq2aza 16, bloq_pas 19, o1 37). Nada se lee en absoluto.
3. **Mundo que se come la comida**: la cámara no comparte mundo entre copias (cada una su anillo, su comida, su olvido); la prueba es la pista vieja sin cambios.
4. **Sitios fijos**: el anillo se sortea por semilla; las semillas de la cámara (598xx y 10^8+…) NO son las de prueba (592xx): la siembra no se
   entrena en el mundo donde se mide.

## 9. Semillas (grep 29-sep: 598xx libre en py/md/txt)
Cámara 59801–59805 (copias c ≥ 1: 10^8 + 1000·s + c) · prueba 59201–59205 (pareadas) · humo 59891 (cámara y prueba) · arnés 59892, 59893.

## 10. Declarado
- **bloq_pas es V143_BQ (v1, sentidos 0–6), no BQ2.** Por eso, tras la auditoría (sec. 11), la puerta usa bloq2 (BQ2 sin depósito) y bloq_pas sólo se imprime.
- El migrante neutro lleva UNA mutación (la del operador del carro con la rng de la migración) para igualar a la entrada del pool, que ya trae la de `al_parir`.
- La cámara lee `_bqR` del vivo (neutro y la muestra final) desde FUERA del carro: no es un carro, revisa_carro no aplica; V143_BQ2 nunca muta `_bqR`
  en su lugar (sólo lo reemplaza), así que la referencia del final del paso vale.
- Costo medido en el humo (ver informe): la cámara K 8 × 50k ≈ 4 corridas viejas de 100k.
- Añadido 09:28 (tras el humo, SIN cambiar umbrales): Q5 se lee con el proxy migrantes / (migrantes + limpios) de toda la cámara por brazo e índice
  (`evo_*.json` → `camara`); el runner no guarda el instante de los fundadores limpios. Arnés: PASA (`identidad_pista_pob_salida.txt`, 618 s).
  Humo (59891, K 8, T_evo 3000, prueba T 10 000): 0 abortos; cámara 27.9 s / 28.8 s (≈ 1.2 ms por paso de copia).

## 11. Cambios por auditoría antes de datos (29-sep)
El auditor dejó pista_pob LISTO CON CAMBIOS. Aplicados ANTES de cualquier dato del explora (sólo existían arnés y humo a T 10k, semilla 59891):
- **H-1 (bloqueante, bug)**: `trabajo()` con `--reanuda` y un `evo_*.json` ya escrito llegaba a `prueba()` con `corre_bp.CFG0 = None` (TypeError en
  un proceso nuevo o worker de Pool), se guardaba como aborto y `--reanuda` no lo reintentaba. Ahora `trabajo()` llama `cfg()` al empezar; un JSON final o
  una cámara con aborto SE REINTENTAN con `--reanuda` (queda `reintento_de` en el JSON). Nuevo `--humo --reanuda --carpeta datos/humo_*` para probarlo.
- **H-2 (bloqueante, puerta)**: la segunda condición de FUNCIONA pasa a **pob_sel ≥ bloq2 en ≥ 4/5** (el mismo carro BQ2 sin depósito: aísla lo que
  agrega la población). bloq_pas (V143_BQ v1) se imprime al lado, no decide. Q4 reescrita igual (p 0.30).
- MODESTO: letra "≥ 3/5" (el código ya era `>=`).
- **pob_neutro NO es un control puro** (declarado): (a) el vivo también sobrevivió hasta ese momento (hay selección por viabilidad, sólo falta la de
  parir); (b) la antigüedad difiere (el pool guarda partos de hasta 400 entradas atrás; el vivo es del paso anterior); (c) la copia donante se sortea
  uniforme entre las otras K − 1, no ponderada por cuántos partos aportó cada una como en el pool. Una diferencia sel − neutro mide "haber parido +
  antigüedad + ponderación por copia", no sólo "haber parido".
- Q5 rotulada PROXY (arriba). `lee()` imprime Q1–Q7 con lo medido. `arnes_pasado()` exige que la salida del arnés cite el sha actual de
  `pista_pob.py` **y** el de `corre_pista_pob.py` (el arnés se volvió a correr con el runner nuevo).
