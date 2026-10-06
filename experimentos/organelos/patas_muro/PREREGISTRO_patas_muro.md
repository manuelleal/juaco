# PREREGISTRO — patas_muro: CONFIRMATORIO de "TERMO + PATAS" contra el muro de la carrera

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas).

Escrito el 29-sep-2026 por el creador de `experimentos/organelos/patas_muro/`, **antes de ver un solo número de las semillas
52601–52640**. Vale sólo si se commitea antes de la serie (ERR-154). El runner lo impone: `--serie` y `--replica` abortan si este
archivo o `corre_patas_muro.py` no están commiteados o difieren de HEAD.

## 1. Pregunta e hipótesis
Con TERMO (v14.3 + termostato de boca), ¿cambiar SÓLO a dónde va el cuerpo aumenta los linajes que cruzan el muro de la carrera?
"A dónde va" significa ir derecho al objeto más cercano que la boca de TERMO mordería ahora, cediendo el que otro cuerpo tiene más cerca
(PATAS 3, UTIL+CEDE, brazo `pc`).

- **H-PATAS:** pc tiene más linajes que cruzan (cruza_real, ENMIENDA 5) que termo, pareado por semilla, en semillas que nadie vio.
- **Origen EXPLORATORIO** (dinamita, ola 3, 39201–39210): pc 55/90 contra termo 44/90 (+7 −2 =1), pi 34/90, o1 71/90.
- **Sesgo del ganador:** pc es el máximo de 12 brazos probados en las mismas 10 semillas, así que su ventaja está inflada.
- **La ola 4 (39211–39230, 8/80) NO se leyó ni se usa.** Esas semillas quedan excluidas.

## 2. Mecanismo mínimo; memoria nueva: CERO
El carro es `dinamita/carros/TPATAS.py` (sha `1b6272ef4616af8b`), construido por anclas desde `termo/carros/V143_TERMO.py`
(sha `3db639cab75641fb`) con `dinamita/construye_patas.py` (sha `85a8c136aa09491d`). **Se REUSA tal cual; aquí no se construye nada.**

- La pieza reemplaza SÓLO el paso que sale del motor de v14.3. El motor corre y consume su rng igual.
- **Qué lee:** lo sentido por el linaje (`_adS` de TERMO), E y Ag, los objetos a la vista y la foto de los cuerpos. Todo eso ya está en `obs`.
- **Cero memoria nueva y cero constantes nuevas:** usa `rep_umbral` y el ½ de TERMO.
- **Con PATAS = 0 es V143_TERMO bit a bit** (arnés, (a)).
- **Parecido con O1, DECLARADO:** O1 también va derecho a un blanco bueno que le sirve y penaliza el que otro tiene más cerca.

## 3. Montaje
- **Pista:** la vieja (`pista.py` 9f47c65e438e0ff4), con el juez (`juez.py` 6a68f640a7832f12).
- **Condiciones:** monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, pizarra 1, rep_acum 0, escala 1, **fundador limpio 1**.
- **Letra de cruce:** ENMIENDA 5 (cruza_real).
- **Entrada (regla 14):** `corre_v143.tarea` importada sin tocar.

| brazo | carro | papel |
|---|---|---|
| `pc` | TPATAS, PATAS 3 (UTIL+CEDE) | **CANDIDATO** |
| `pu` | TPATAS, PATAS 2 (UTIL) | secundario (no decide) |
| `pd` | TPATAS, PATAS 1 (DIRECTO: sólo paso derecho al objetivo de v14.3) | **secundario y descriptivo** (auditoría H-2; no entra en FUNCIONA) |
| `termo` | V143_TERMO | **BASE** (la comparación principal) |
| `pi` | TPATAS, PATAS 4 (INÚTIL: va a lo bueno que la boca NO mordería) | **CONTROL desfasado** del mismo canal |
| `o1` | O1 (carrera) | ANCLA / techo |
| `v143` | V143 (tronco v14.3) | ANCLA / el bicho real |

- **Semillas FRESCAS:** serie **52601–52620**, réplica **52621–52640**, arnés 52691–52692, humo 52693–52694.
  - Se buscaron colisiones en los JSON, py, md, txt, log y csv de todos los árboles de `PROYECTOS/JUACO` (bundle, organelos, carrera,
    nube, convive, anclado, aprende, criterio, escuela, exploracion, fanin, ml_continuo, sandbox): **0 archivos** usan 52600–52699.
- **Corridas:** 7 brazos × 20 = 140 por serie.
- **Estado por worker:** cada brazo TPATAS es una instancia de módulo PROPIA. `trabajo()` fija PATAS en el proceso que corre y lo escribe
  en el JSON (`estado`); `lee()` lo verifica (V4).
- **Runner:** `corre_patas_muro.py`. Su sha se fija con este commit.
- **Arnés:** `identidad_patas_muro.py`, PASA; salidas enteras en `identidad_patas_muro_salida.txt` y `identidad_patas_muro_salida_largo.txt`.
  El (e) reproduce bit a bit el JSON de la ola 3 de pc en 39201 con el runner confirmatorio.

## 4. Medida principal (hallazgo 3 del auditor)
`c_b(s)` = linajes que cruzan (0–9) del brazo b en la semilla s. La medida es la **suma sobre 20 semillas × 9 = 180 linajes**, pareada
por semilla. La mayoría por semilla (≥ 5/9, la letra del muro) se reporta como una **puerta aparte**.

## 5. LA LETRA (está en `lee()` del runner; manda el código si hubiera discrepancia de redacción)
**Validez.** Si falla cualquiera: NO SE LEE.
- **V1:** 20 semillas × 7 brazos completas, 0 abortos, contabilidad coherente y t_fund reconstruible en todos los linajes.
- **V2:** O1 con mayoría que cruza en **≥ 17/20** semillas (histórico: 20, 19, 19, 19; ola 3: 10/10).
- **V3:** V143, mediana del R0 real en **[0.40, 0.80]** (histórico: 0.536–0.634).
- **V4:** cada JSON trae el carro, el sha y la perilla esperados (TPATAS 1b6272ef4616af8b con PATAS 3/2/1/4; V143_TERMO 3db639cab75641fb;
  TERMO = 1). Además, antes de correr: shas fijados, TPATAS == construye_patas, e identidad corta con PATAS = 0 == V143_TERMO.
- **V5:** la pieza actúa (`cambia` > 0) en pc, pu, pd y pi, en todas las semillas.
- **V6 (auditoría H-3):** termo, Σ de linajes que cruzan en **[70, 120]** de 180 (histórico 96 y 95; ola 3 44/90 ≈ 88). Si cae, la base
  está fuera de lo conocido y NO SE LEE.

**Puertas.**
- **PA:** pc tiene MÁS linajes que cruzan que termo en **≥ 13/20** semillas. Los empates cuentan EN CONTRA.
- **PB:** Σ c_pc ≥ Σ c_termo **+ 15** (de 180).
- **PD (control, trampa 1):** pc le gana a pi con la misma forma: ≥ 13/20 semillas y Σ c_pc ≥ Σ c_pi + 15.
  - Si falla, la ventaja no es del CONTENIDO (ir a lo útil), sino de caminar derecho a cualquier cosa buena.
- **PC (letra del muro):** pc con mayoría que cruza (≥ 5/9) en **≥ 15/20** semillas (como O1; `gana_e5` de corre_v143).

**Veredicto de una serie:**
- **FUNCIONA** = PA ∧ PB ∧ PD ∧ PC.
- **HAY ALGO MODESTO** = PA ∧ PB ∧ PD ∧ ¬PC.
- **NO** en cualquier otro caso. Si PA ∧ PB pasan y PD cae, se escribe "NO (inespecífico)".

**Ajustes sobre la letra sugerida por el coordinador, con su justificación:**
1. Se añade PD a FUNCIONA y a MODESTO. Sin PD, la trampa del canal simétrico queda abierta.
2. pi-vs-termo va como secundaria. pi se hundió en la ola 3 (−10/90), así que "pc > pi" sola sería una puerta fácil; la comparación
   que decide es contra termo (PA, PB).

**Por qué 13/20 y +15.** En la ola 3, la diferencia pc−termo por semilla tuvo desviación típica 1.7. Sobre 20 semillas, la suma tiene
DT ≈ 7.7.
- Bajo nulo, P(Σ ≥ +15) ≈ 0.03.
- Bajo nulo, con p(gana) ≈ 0.4 (hay empates), P(≥ 13/20) ≈ 0.02.
- Ninguna de las dos depende de una sola semilla en el umbral de 5/9.

## 6. Secundarias y descriptivas (NO deciden; se reportan siempre)
- **pu vs termo**, con la forma PA+PB. También pc vs pu, o1 vs pc, o1 vs termo y termo vs v143.
- **pd (auditoría H-2):** `pc_vs_pd` y `pd_vs_termo`, con la forma PA+PB (≥ 13/20 y ≥ +15). Sólo ata el vocabulario (§11).
- **pi vs termo (hallazgo 4):** se reporta el pareado entero.
  - Si Σ c_pi ≤ Σ c_termo − 15, se escribe **"el contenido equivocado daña"**: el canal lleva información en los dos sentidos.
  - Si Σ c_pi ≥ Σ c_termo + 15, se escribe **"caminar derecho ayuda por sí solo"**, y FUNCIONA/MODESTO se lee con esa reserva.
- **R0 real:** pareado por la mediana de cada semilla (`corre_v143.pareado`).
- **¿Come más o decide mejor? (hallazgo 5).** Cada medida es la mediana de los 9 linajes de la semilla; la lectura se da sólo si
  pc > termo en ≥ 13/20 semillas.

| medida | se lee como |
|---|---|
| mordidas A+C por linaje | **"come más"** |
| fracción buena (A+C)/(A+B+C+D) | **"decide mejor"** |
| nacimientos reales por 100 mordidas A+C | **"rinde mejor"** |
| A+C del mundo (pc < termo) | **"mundo más pelado"** |
| mordidas B+D por linaje | se reporta |
| fundadores | se reporta |
| linajes establecidos (0 fundadores tras 10k) | se reporta |

Vocabulario ligado: si pc cruza más pero "no decide mejor", se dice "**cruza comiendo/limpiando más**", no "decide cuándo limpiar".

## 7. Réplica, regla de parada y bloque
- La réplica (52621–52640, mismos brazos y misma letra) **sólo se corre si la serie da FUNCIONA o HAY ALGO MODESTO**. El runner lo impone.
- Si la serie da NO, se para y el bloque es **NO**.
- Si da NO SE LEE, se diagnostica y se re-corre la serie con `--reanuda` (sin tocar la letra).
- **Candados del runner (auditoría H-5):**
  - `--serie` y `--replica` se niegan si ya existe un `resumen.json` (no humo) con veredicto FUNCIONA, MODESTO o NO.
  - Si hay una carpeta previa cortada o NO SE LEE, sólo se admite `--reanuda`.
  - La réplica exige que el `sha_runner` de la serie sea igual al del runner actual, y `--bloque` lo exige a los dos resúmenes.
- **Bloque = el menor de los dos veredictos** (`--bloque`). Para ★ hace falta FUNCIONA ×2.

## 8. Predicciones (probabilidades honestas; escritas antes de los datos, con el sesgo del ganador en mente)
| # | predicción (serie 52601–52620) | p |
|---|---|---|
| Q1 | Σ c_termo entre 80 y 105 (de 180; histórico 96 y 95) | 0.75 |
| Q2 | Σ c_pc entre 90 y 120 | 0.70 |
| Q3 | Σ c_pc − Σ c_termo entre +3 y +22 | 0.65 |
| Q4 | PB pasa (≥ +15) | 0.35 |
| Q5 | PA pasa (≥ 13/20 semillas) | 0.35 |
| Q6 | PD pasa (pc sobre pi) | 0.85 |
| Q7 | pc: mayoría que cruza entre 11 y 17 de 20 · PC (≥ 15) pasa | 0.75 · 0.35 |
| Q8 | Σ c_pi ≤ Σ c_termo − 15 ("el contenido equivocado daña") | 0.55 |
| Q9 | o1: Σ entre 125 y 150 y mayoría ≥ 18/20 | 0.80 |
| Q10 | v143: R0 real mediano entre 0.50 y 0.68 | 0.80 |
| Q11 | pu pasa la forma PA+PB contra termo | 0.25 |
| Q12 | pc "come más" (A+C) sí 0.60 · "decide mejor" NO 0.85 · "mundo más pelado" sí 0.80 · muerde más B+D que termo en ≥ 13/20 0.85 | — |
| Q13 | pc: fundadores medianos < termo en ≥ 13/20 | 0.45 |
| Q14 | Veredicto de la serie: FUNCIONA 0.15 · HAY ALGO MODESTO 0.20 · NO 0.60 · NO SE LEE 0.05 | — |
| Q15 | Bloque FUNCIONA ×2 | 0.08 |
| Q16 | pd ≈ termo: Σ c_pd − Σ c_termo entre −12 y +12 (ola 3: 47 contra 44 de 90) | 0.70 |
| Q17 | pd pasa la forma PA+PB contra termo | 0.10 |
| Q18 | pc pasa la forma PA+PB contra pd ("a dónde va lo útil") | 0.25 |
| Q19 | V6: Σ c_termo en [70, 120] | 0.92 |

Lectura global que el creador espera: la ventaja existe pero es menor que en la ola 3 (sesgo del ganador), y lo más probable es que no
llegue a +15. Si llega, será comiendo y limpiando más, no decidiendo mejor.

## 9. Las cuatro trampas
1. **Canal simétrico.** pi usa la misma maquinaria (misma lectura, paso derecho, mismo carro) con el blanco invertido: es PD.
   - Además va pd (DIRECTO: paso derecho al objetivo de v14.3, sin elegir lo útil), como secundario. Separa "ir a lo útil" de "caminar
     derecho" y ata el vocabulario (§11). En la ola 3 dio 47/90 ≈ termo.
2. **Acierto sin balancear.** No hay clases. La medida son linajes (9 por semilla, pareados), así que ningún brazo gana por tener más
   linajes. R0 real = nacimientos reales. La mayoría por semilla depende del umbral 5/9, por eso decide la suma.
3. **Mundo que se come la comida.** En la ola 3, pc bajó el A+C del mundo (2.5 contra 3.3). Se reporta siempre (§6) y ata el
   vocabulario. Las reglas de la pista no cambian; en monocultivo el costo del mundo pelado lo pagan los mismos 9 carros.
4. **Sitios fijos.** PATAS no tiene memoria: lee sólo los objetos presentes en `obs`, así que no puede explotar sitios. Las semillas son
   frescas y el mundo se genera por semilla.

## 10. Qué lo refuta
- **PA o PB caen:** la ventaja de la ola 3 era sesgo del ganador. PATAS sobre TERMO queda CERRADO contra el muro.
- **PA y PB pasan, pero PD cae:** es inespecífico (caminar derecho), no "a dónde va lo útil".
- **PA, PB y PD pasan, pero PC cae:** MODESTO. Ayuda, pero no cruza la letra del muro.
- **La réplica no repite:** el bloque baja al menor.
- **En el umbral (auditoría H-4):** un FUNCIONA con PA = 13 exacto, o con PB entre +15 y +17, se reporta **"en el umbral"** y no
  sostiene ★ sin la réplica. El runner lo marca (`en_umbral`). Vale igual para MODESTO.

## 11. Vocabulario
- **Permitido** (sólo con el veredicto correspondiente): "con PATAS, TERMO tiene más linajes que cruzan"; "cruza la letra del muro" (sólo con
  FUNCIONA ×2).
- **"A dónde va lo útil"** (auditoría H-2) sólo si pc > pd con la forma PA+PB. Si no, se dice **"PATAS ayuda, sin separarlo de caminar
  derecho"**. El runner imprime cuál de las dos toca.
- **Prohibido:** "decide cuándo limpiar" (salvo que "decide mejor" se cumpla), "aprende", "supera a O1".

## 12. Comandos y tiempo (estimado con pool 2)
- **Costo por corrida** (medido con pool 6 en termo y dinamita): termo y v143 ~150 s; pc, pu, pd y pi ~188 s; o1 ~300 s.
- **Humo (un proceso, T 20 000):** pc 21.7 s, pu 21.1 s, pd 18.1 s, termo 17.7 s, pi 22.0 s, o1 34.5 s, v143 17.3 s. Suman 152 s por
  semilla, ≈ 760 s con T 100 000.
- **Con pool 2** (140 corridas): serie ≈ **2.4 h** (entre 2.1 h sin contención y 3.8 h con la contención de pool 6); réplica otro tanto.
- **El humo son dos procesos**, porque el máximo es 6 corridas por proceso:
  - `--humo` corre 6 brazos y da NO SE LEE por incompleta.
  - `--humo --reanuda` corre la 7.ª (v143), salta lo escrito y lee.
  - Aun completo da NO SE LEE **por diseño**: con T 20 000 y una semilla, O1, V143 y la banda de termo no llegan (V2, V3, V6). Sirve
    para ejercitar el camino entero, no para leer.
- `datos/humo/` queda fuera de git (`.gitignore` local). La salida entera del humo va en `humo_salida.txt` y `humo_reanuda_salida.txt`.

```
python experimentos/organelos/patas_muro/identidad_patas_muro.py            # arnés corto (~55 s); --largo (~160 s)
python experimentos/organelos/patas_muro/corre_patas_muro.py --humo         # humo, 1.er proceso (6 corridas, T 20 000)
python experimentos/organelos/patas_muro/corre_patas_muro.py --humo --reanuda   # humo, 2.º proceso (v143) y lectura
python experimentos/organelos/patas_muro/corre_patas_muro.py --serie --pool 2
python experimentos/organelos/patas_muro/corre_patas_muro.py --serie --pool 2 --reanuda      # sólo si se cortó o dio NO SE LEE
python experimentos/organelos/patas_muro/corre_patas_muro.py --replica --pool 2
python experimentos/organelos/patas_muro/corre_patas_muro.py --bloque <serie>/resumen.json,<replica>/resumen.json
```

## 13. Cambios por auditoría antes de datos (29-sep)
El auditor dejó el diseño LISTO CON CAMBIOS. Todos se aplicaron antes de cualquier dato de 52601–52640.

- **H-3:** V6 de validez. Σ c_termo en [70, 120] de 180; si cae, NO SE LEE (§5).
- **H-2** (decisión del coordinador): se añade el brazo `pd` (TPATAS, PATAS 1, mismo sha).
  - Es SECUNDARIO y descriptivo; no entra en FUNCIONA.
  - Queda cubierto por V4 y V5 y aparece en los pares `pc_vs_pd` y `pd_vs_termo`, con la forma PA+PB.
  - Añade una regla de vocabulario (§11) y va en el arnés (PATAS = 0 == TERMO).
  - Predicciones Q16–Q18.
  - La serie pasa de 120 a 140 corridas.
- **H-5:** candados del runner (§7). Se niega a re-correr lo que ya tiene veredicto y verifica el `sha_runner` en la réplica y el bloque.
- **H-4:** regla "en el umbral" (§10).
- Arnés (normal y largo) y humo re-corridos con el sha final del runner.
- Las predicciones Q1–Q15 no se tocaron. Se añaden Q16–Q19.
