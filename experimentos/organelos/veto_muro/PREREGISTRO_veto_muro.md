# PREREGISTRO — veto_muro: CONFIRMATORIO de "TERMO + PATAS + VETO POR RESERVAS" contra el muro de la carrera

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas).

Escrito el 29-sep-2026 por el creador de `experimentos/organelos/veto_muro/`, **antes de ver un solo número de las semillas
53701–53740** y antes del humo (semilla 53793). Vale sólo si se commitea antes de la serie (ERR-154). El runner lo impone: `--serie` y
`--replica` abortan si este archivo, `corre_veto_muro.py`, `construye_veto_muro.py` o `carros/TVPISO.py` no están commiteados o difieren de
HEAD. **La serie se lanza DESPUÉS de que termine `patas_muro` (52601–52640), con `--pool 2` como máximo.**

## 1. Pregunta, hipótesis y diagnóstico (números verificados por el creador)
Con TERMO + PATAS 3 (el `pc` de patas_muro), ¿quitarle a la boca de fábrica SÓLO las mordidas de lo sentido malo que el cuerpo no puede
pagar aumenta los linajes que cruzan el muro?

**Diagnóstico** (junta Fable, investigador 2; re-verificado aquí sobre los JSON crudos):

| fuente | brazo | hijos muertos | ≤ 200 pasos | vida mediana del hijo | muere de veneno+sal | hijo que pare | B+D por linaje |
|---|---|---|---|---|---|---|---|
| termo 39101–39140 | termo | 10 913 | **0.131** | **1318** | **0.475** | 0.49 | 62 |
| termo 39101–39140 | o1 | 5 303 | **0.006** | **3581** | 0.318 | 0.70 | 354 |
| termo 39101–39140 | v143 | 8 913 | 0.132 | 1345 | 0.472 | 0.50 | 90.5 |

- `dinamita/lee_dinamita.py`, 39201–39210 (exploratorio): termo 44/90 (h≤200 0.129, mundo A+C 3.30); **vu** (VETO 1, piso = rep_umbral
  SIEMPRE) **4/90**, h≤200 0.000, mundo A+C **2.19** (el mundo se tapa: nadie limpia); **pc** 55/90, h≤200 **0.197** (PATAS SUBE la muerte
  temprana del hijo), mundo A+C 2.50; o1 71/90, h≤200 0.006, mundo A+C **2.08**.
- La boca de fábrica muerde con logit `1.2·w + 2·hambre + 0.5`: con hambre muerde lo malo. El hijo nace a E = Ag = 0.6 (dote); un veneno
  (−0.4) lo deja a 0.2 y muere en ~200 pasos (costo 0.001/paso).
- O1 muerde lo malo sólo si puede pagarlo (`O1._costeable`: PISO 0.2 fuera de la ventana de parto, rep_umbral 1.0 dentro), y además sólo
  sobre la necesidad más llena y sin nada útil a la vista. **Nunca se probó el piso intermedio de O1 solo.**

- **H-VETO:** tpv (TERMO + PATAS 3 + VETO_PISO) tiene más linajes que cruzan (cruza_real, ENMIENDA 5) que termo, pareado por semilla, en
  semillas que nadie vio; y la ventaja depende de leer la necesidad que el golpe toca (tpv > vinv).
- **Origen:** NO hay exploratorio de esta pieza. Es un confirmatorio directo de un diagnóstico. No hay sesgo del ganador en la pieza
  (nunca se corrió a T largo), pero sí lo hay en PATAS 3 (máximo de 12 brazos en dinamita; lo confirma o no patas_muro).

## 2. Mecanismo mínimo; memoria nueva: CERO; una constante nueva DECLARADA
Carro `carros/TVPISO.py` (sha `7653cd267790500b`), construido POR ANCLAS con `construye_veto_muro.py` (sha `779c5cd8bea2db85`) desde
`dinamita/carros/TPATAS.py` (sha `1b6272ef4616af8b`, que a su vez es V143_TERMO `3db639cab75641fb` + PATAS por anclas). Seis anclas, cada
una exactamente una vez o aborta.

**Pieza VETO_PISO (una, en la BOCA; sólo QUITA mordidas, nunca fuerza; sin rng):** sobre una letra k cuyo dS SENTIDO por el linaje
(`s = _adS`, la misma lectura de TERMO) tiene alguna componente negativa:
- `piso = rep_umbral (1.0)` si `min(E, Ag) ≥ rep_umbral` (la ventana de parto corre); `piso = PISO_V = 0.2` si no.
- **VETOP 1 (PISO):** no muerde si existe j con `s_j < 0` y `nivel_j + s_j < piso`.
- **VETOP 2 (PISOINV, CONTROL):** la misma regla leyendo la necesidad que el golpe NO toca: `nivel_{1−j} + s_j < piso`.
- Va DESPUÉS de FILTRO, APR (opción) y TERMO. La opción APR aprende sobre SU decisión, no sobre la ejecutada (igual que VETO de dinamita;
  declarado).
- **Constante nueva:** `PISO_V = 0.2 = dote/3` (dote 0.6) = el PISO de O1. Todo lo demás es de TERMO.
- **Frontera declarada:** el hijo recién nacido (E = 0.6 exacto) sobre un veneno sentido −0.4 da `0.6 − 0.4 = 0.19999999999999996 < 0.2`
  → se veta (igual que en `O1._costeable`). Tras un paso E = 0.599 y el caso ya no es frontera.
- **Parecido con O1, DECLARADO:** es la cláusula de piso de `O1._costeable`, sola. NO lleva "el golpe cae en la necesidad más llena", ni
  "nada útil a la vista", ni fuerza limpiezas.
- **Diferencia con VETO 1 de dinamita (vu):** vu usaba piso = rep_umbral siempre (sólo muerde veneno con E ≥ 1.4). VETO_PISO deja limpiar
  a quien tiene E ≥ 0.6 fuera de la ventana: el adulto sigue limpiando el mundo; el hijo hambriento no.
- **Con VETOP = 0 es TPATAS bit a bit; con VETOP = PATAS = 0 es V143_TERMO bit a bit** (arnés (a), salida ENTERA).
- **Efecto heredado del tronco (auditoría H-5), DECLARADO:** un mordisco vetado es un "no muerde", y la línea que sigue en `actua()` hace
  `_rech[pos] = t + MEMORIA_RECHAZO`: esa casilla deja de ser objetivo del ojo de v14.3 (`_see`) durante MEMORIA_RECHAZO pasos, o hasta que
  la letra se olvide o alguien la muerda. **En esta pista MEMORIA_RECHAZO = 20** (`pista.cfg_fabrica()['kw']['memoria_rechazo']`; lo
  confirma la salida del carro en una corrida de tpv, s 53791). La pieza no toca esa línea: es el mismo tratamiento que ya reciben los
  rechazos de la boca de fábrica, de FILTRO y de TERMO. Consecuencia: el cuerpo vetado tiende a alejarse de lo malo que no puede pagar
  durante 20 pasos (con PATAS 3, el ojo de v14.3 sólo manda cuando no hay blanco útil).

## 3. Montaje
- **Pista:** la vieja (`pista.py` 9f47c65e438e0ff4), con el juez (`juez.py` 6a68f640a7832f12).
- **Condiciones:** monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, pizarra 1, rep_acum 0, escala 1, **fundador limpio 1**.
- **Letra de cruce:** ENMIENDA 5 (cruza_real).
- **Entrada (regla 14):** `corre_v143.tarea` importada sin tocar; arnés (c) campo a campo contra `corre_v143.tarea` y contra
  `corre_patas_muro.tarea('pc')`.

| brazo | carro | perillas | papel |
|---|---|---|---|
| `tpv` | TVPISO | PATAS 3, VETOP 1 | **CANDIDATO** |
| `tv` | TVPISO | PATAS 0, VETOP 1 | ABLACIÓN sin patas (TERMO + VETO_PISO); no decide |
| `vinv` | TVPISO | PATAS 3, VETOP 2 | **CONTROL desfasado** del mismo canal (trampa 1) |
| `pc` | TPATAS | PATAS 3 | ABLACIÓN sin veto (= pc de patas_muro, mismo sha); no decide |
| `termo` | V143_TERMO | TERMO 1 | **BASE** |
| `o1` | O1 (carrera) | — | ANCLA / techo |
| `v143` | V143 (tronco v14.3) | — | ANCLA / el bicho real |

- **Semillas FRESCAS:** serie **53701–53720**, réplica **53721–53740**, arnés 53791–53792, humo 53793.
  - Colisiones: se buscó en json/py/md/txt/log/csv de todos los árboles de `PROYECTOS/JUACO` con contexto de semilla (`"seed": 537xx`,
    `s537xx`, rangos `537xx–`, `range(537xx`): **0**. Las únicas apariciones de `537xx` como número suelto son un sello de hora
    (`_053711`) y valores de un CSV de capacidad del 15-sep; ninguna es semilla. No se usan 526xx (patas_muro) ni 592xx (moneda).
- **Corridas:** 7 brazos × 20 = 140 por serie.
- **Estado por worker:** cada brazo es una instancia de módulo PROPIA; `trabajo()` fija PATAS y VETOP en el proceso que corre, los escribe
  en el JSON (`estado`) y `lee()` los verifica (V4). Arnés (d): se estropean a mano y `trabajo()` los re-fija.

## 4. Medida principal
`c_b(s)` = linajes que cruzan (0–9) del brazo b en la semilla s. La medida es la **suma sobre 20 semillas × 9 = 180 linajes**, pareada por
semilla. La mayoría por semilla (≥ 5/9, la letra del muro) es una **puerta aparte**.

## 5. LA LETRA (está en `lee()` del runner; manda el código si hubiera discrepancia de redacción)
**Validez.** Si falla cualquiera: NO SE LEE.
- **V1:** 20 semillas × 7 brazos completas, 0 abortos, contabilidad coherente y t_fund reconstruible en todos los linajes.
- **V2:** O1 con mayoría que cruza en **≥ 17/20** semillas.
- **V3:** V143, mediana del R0 real en **[0.40, 0.80]** (histórico 0.536–0.634).
- **V4:** cada JSON trae el carro, el sha y las perillas esperadas (TVPISO 7653cd267790500b con (PATAS, VETOP) = (3,1), (0,1), (3,2);
  TPATAS 1b6272ef4616af8b con PATAS 3; V143_TERMO 3db639cab75641fb; TERMO = 1). Además, antes de correr: shas fijados, TVPISO ==
  construye_veto_muro, e identidad corta con VETOP = 0 == TPATAS/TERMO y con VETOP = PATAS = 0 == V143_TERMO.
- **V5:** las piezas actúan en todas las semillas: vetos (`vpiso.a_no`) > 0 en tpv, tv y vinv; cambios de paso (`patas.cambia`) > 0 en tpv,
  vinv y pc.
- **V6:** termo, Σ de linajes que cruzan en **[70, 120]** de 180 (histórico 96 y 95).

**Puertas.**
- **PA:** tpv tiene MÁS linajes que cruzan que termo en **≥ 13/20** semillas. Los empates cuentan EN CONTRA.
- **PB:** Σ c_tpv ≥ Σ c_termo **+ 15** (de 180).
- **PD (control, trampa 1):** tpv le gana a vinv con la misma forma: ≥ 13/20 semillas y Σ c_tpv ≥ Σ c_vinv + 15.
- **PC (letra del muro):** tpv con mayoría que cruza (≥ 5/9) en **≥ 15/20** semillas.

**Veredicto de una serie:**
- **FUNCIONA** = PA ∧ PB ∧ PD ∧ PC.
- **HAY ALGO MODESTO** = PA ∧ PB ∧ PD ∧ ¬PC.
- **NO** en cualquier otro caso. Si PA ∧ PB pasan y PD cae: **"NO (inespecífico)"**.
- **En el umbral:** FUNCIONA o MODESTO con PA = 13 exacto, PB entre +15 y +17, **PD con gana = 13 exacto o dif entre +15 y +17, o (en
  FUNCIONA) PC = 15 exacto** (auditoría C3) se marca `en_umbral` (el runner dice qué puertas) y no sostiene ★ sin la réplica.

**Ajustes sobre la letra sugerida por el coordinador, con su justificación:**
1. **"A+C del mundo: falla si < 2.5" pasa de umbral absoluto a descriptivo relativo.** En dinamita ola 3, O1 (que cruza 71/90) tiene mundo
   A+C 2.08 y pc 2.50: un corte absoluto en 2.5 marcaría como "tapado" al techo y a la ablación. Se marca **"mundo tapado"** si tpv pela el
   mundo más que pc en ≥ 13/20 semillas **y** cruza menos que pc (Σ). No decide; ata el vocabulario.
2. **V5 exige que actúen LAS DOS piezas** (el veto en tpv/tv/vinv y las patas en tpv/vinv/pc).
3. **Ablaciones con la forma PA+PB** (tpv vs pc, tpv vs tv, tv vs termo, pc vs termo): no deciden, atan el vocabulario (§11).
4. Lo demás, como lo sugirió el coordinador (13/20, +15, vinv con la misma forma, mayoría ≥ 15/20, validez).

**Por qué 13/20 y +15** (igual que patas_muro): con DT ≈ 1.7 por semilla en la diferencia pareada, bajo nulo P(Σ ≥ +15) ≈ 0.03 y
P(≥ 13/20 con empates en contra) ≈ 0.02.

## 6. Descriptivos, ablaciones y secundarias (NO deciden; se reportan siempre)
- **Hijos, por brazo** (cuerpos de origen 1 ya muertos, agregados): muertos en ≤ 200 pasos (**h≤200**); muertos de hambre o sed con vida
  ≤ 620 (**h600**: el hijo que no se muerde el veneno pero tampoco come — la muerte desplazada de vu); vida mediana; fracción que muere de
  veneno+sal; fracción que pare. Pareado por semilla tpv vs termo, tpv vs pc, tpv vs vinv, tv vs termo, pc vs termo, o1 vs termo.
- **Mundo:** A+C del mundo (mediana por semilla), mordidas A+C y B+D por linaje, fracción buena, fundadores, establecidos.
- **Ablaciones (qué aporta cada pieza):**

| par | pregunta |
|---|---|
| tpv vs pc | ¿el veto aporta sobre TERMO + PATAS? |
| tpv vs tv | ¿las patas aportan sobre TERMO + VETO? |
| tv vs termo | ¿el veto solo, sobre TERMO? |
| pc vs termo | réplica de patas_muro en semillas nuevas (descriptiva) |
| vinv vs termo | si Σ c_vinv ≤ Σ c_termo − 15: "el contenido equivocado daña" |

## 7. Réplica, regla de parada y bloque
- La réplica (53721–53740, mismos brazos y letra) **sólo se corre si la serie da FUNCIONA o HAY ALGO MODESTO**. El runner lo impone.
- Si la serie da NO, se para y el bloque es **NO**. Si da NO SE LEE, se diagnostica y se re-corre con `--reanuda` (sin tocar la letra).
- **Candados:** `--serie`/`--replica` se niegan si ya hay un `resumen.json` (no humo) con veredicto; con carpeta previa cortada o NO SE LEE,
  sólo `--reanuda`; la réplica exige el mismo `sha_runner` que la serie, y `--bloque` lo exige a los dos.
- **Bloque = el menor de los dos veredictos.** Para ★ hace falta FUNCIONA ×2.

## 8. Predicciones (probabilidades honestas; escritas antes de cualquier número de la pieza, incluido el humo)
| # | predicción (serie 53701–53720) | p |
|---|---|---|
| Q1 | V6: Σ c_termo en [70, 120] · y en [80, 105] | 0.92 · 0.75 |
| Q2 | h≤200 de tpv < 0.05 (termo ≈ 0.13, pc ≈ 0.20) | 0.80 |
| Q3 | h≤200 de tv < 0.05 · h≤200 de vinv < h≤200 de termo (vinv también veta al recién nacido: E = Ag) | 0.80 · 0.70 |
| Q4 | h≤200 de pc en [0.14, 0.26] | 0.75 |
| Q5 | vida mediana del hijo: tpv > termo en ≥ 13/20 semillas | 0.70 |
| Q6 | muerte desplazada: h600 de tpv > h600 de termo en ≥ 13/20 semillas | 0.65 |
| Q7 | mundo A+C mediano de tpv en [2.0, 2.8] · bandera "mundo tapado" | 0.70 · 0.30 |
| Q8 | Σ c_tpv en [80, 125] | 0.70 |
| Q9 | Σ c_tpv − Σ c_termo en [−15, +25] · PB pasa (≥ +15) | 0.75 · 0.35 |
| Q10 | PA pasa (≥ 13/20) | 0.35 |
| Q11 | PD pasa (tpv sobre vinv con la forma) | 0.35 |
| Q12 | PC pasa (mayoría ≥ 15/20) | 0.35 |
| Q13 | tv vs termo: \|dif\| < 15 · tv ≤ termo − 15 · tv ≥ termo + 15 | 0.55 · 0.25 · 0.20 |
| Q14 | "el veto aporta": tpv > pc con la forma PA+PB | 0.25 |
| Q15 | o1: Σ en [125, 150] y mayoría ≥ 18/20 · v143: R0 real mediano en [0.50, 0.68] | 0.80 · 0.80 |
| Q16 | Veredicto de la serie: FUNCIONA 0.12 · HAY ALGO MODESTO 0.12 · NO 0.71 · NO SE LEE 0.05 | — |
| Q17 | Bloque FUNCIONA ×2 | 0.06 |

**Por qué soy más pesimista que el investigador (FUNCIONA 0.25, MODESTO 0.35, NO 0.40):**
1. PD es dura: vinv comparte el veto del recién nacido (al nacer E = Ag, las dos lecturas coinciden) y sólo difiere cuando E ≠ Ag.
2. vu mostró que salvar al hijo de los 200 pasos lo mata a los 600 si el mundo no tiene comida cerca. PISO_V deja limpiar a los adultos,
   pero PATAS 3 ya pela el mundo (2.50).
3. Lectura global que espero: el hijo deja de morir joven (Q2 casi segura), la vida del hijo sube, parte de esa muerte se desplaza a los 600,
   y la suma de linajes que cruzan sube poco, sin llegar a +15.

## 9. Las cuatro trampas
1. **Canal simétrico.** vinv usa la misma maquinaria (misma lectura `_adS`, mismo piso, mismo lugar en la boca, mismas patas), con la
   necesidad invertida: es PD. Si PA ∧ PB pasan y PD cae, se escribe "NO (inespecífico)": el beneficio sería "no morder lo malo con
   reservas bajas", sin leer qué necesidad golpea. **Alcance del cierre (auditoría C2):** en ese caso sólo queda CERRADO el veto como
   pieza que lee QUÉ necesidad golpea el mordisco. **"Proteger al recién nacido"** (no morder lo malo con reservas bajas, sea cual sea la
   necesidad) queda como **hipótesis distinta, NO refutada**: vinv también la cumple al nacer (E = Ag) y este diseño no la separa.
2. **Acierto sin balancear.** No hay clases. La medida son linajes (9 por semilla, pareados), así que ningún brazo gana por tener más
   linajes. R0 real = nacimientos reales. La mayoría depende del umbral 5/9; por eso decide la suma, con la mayoría como puerta aparte.
3. **Mundo que se come la comida.** Aquí es el riesgo inverso (el mundo que se TAPA porque nadie limpia, como vu). Se reporta el mundo A+C
   por brazo y la bandera "mundo tapado" (§5, ajuste 1). Las reglas de la pista no cambian; en monocultivo el costo lo pagan los mismos 9.
4. **Sitios fijos.** La pieza no tiene memoria de lugares: lee sólo la letra bajo el cuerpo y los niveles propios. La única memoria de
   casillas es la heredada del tronco (`_rech`, 20 pasos, §2) y la tienen igual todos los brazos TERMO. Las semillas son frescas y el
   mundo se genera por semilla.

## 10. Qué lo refuta
- **PA o PB caen:** salvar al hijo de la muerte temprana no mueve el muro sobre TERMO. VETO_PISO sobre TERMO + PATAS queda CERRADO.
- **PA y PB pasan, pero PD cae:** "NO (inespecífico)" (§9.1). Sólo se cierra el veto como pieza que lee qué necesidad golpea;
  "proteger al recién nacido" queda como hipótesis distinta, no refutada (auditoría C2).
- **PA, PB y PD pasan, pero PC cae:** MODESTO. Ayuda, pero no cruza la letra del muro.
- **h≤200 de tpv NO baja de 0.05:** el diagnóstico estaba mal (el hijo no moría por morder lo sentido malo). Se reporta aunque el veredicto sea otro.
- **La réplica no repite:** el bloque baja al menor.

## 11. Vocabulario
- **Permitido** (sólo con el veredicto correspondiente): "con VETO_PISO, TERMO + PATAS tiene más linajes que cruzan"; "cruza la letra del
  muro" (sólo con FUNCIONA ×2).
- **"El veto aporta"** sólo si tpv > pc con la forma PA+PB; si no: "sin separar el veto de las patas".
- **"Las patas aportan"** sólo si tpv > tv con la forma PA+PB; si no: "sin separar las patas del veto".
- **"Mundo tapado"** si la bandera (§5) se enciende. El runner imprime qué frase toca.
- **Prohibido:** "decide cuándo limpiar", "aprende", "supera a O1", "como O1" (la pieza es UNA cláusula de O1, no O1).

## 12. Comandos y tiempo (estimado con pool 2)
- **Humo (un proceso, T 20 000, s 53793; con patas_muro corriendo al lado):** tpv 22.0 s, tv 19.1 s, vinv 25.5 s, pc 24.0 s, termo 20.4 s,
  o1 38.3 s, v143 ≈ 20 s. Suman ≈ 169 s por semilla, ≈ 845 s con T 100 000. Salidas enteras en `humo_salida.txt` y `humo_reanuda_salida.txt`.
- **Con pool 2** (140 corridas): serie ≈ **2.4 h** (entre 2.2 h y 4 h según la contención); réplica otro tanto.
- **El humo se miró DESPUÉS de firmar la sec. 8** y no la cambia. No cuenta (una semilla, T 20 000); se anota para que el lector
  compare: tpv h≤200 0.00 (pc 0.30), vida del hijo 1512 (pc 600), pero h600 0.24 (pc 0.07) y mundo A+C 2.16 (pc 3.15): el patrón de vu
  (muerte desplazada y mundo tapado) aparece ya en el humo.
- **El humo son dos procesos** (máximo 6 corridas por proceso): `--humo` corre 6 brazos y da NO SE LEE por incompleta; `--humo --reanuda`
  corre la 7.ª (v143) y lee. Aun completo da NO SE LEE **por diseño** (T 20 000 y una semilla: O1, V143 y la banda de termo no llegan).
- `datos/humo/` queda fuera de git (`.gitignore` local).

```
python experimentos/organelos/veto_muro/construye_veto_muro.py --verifica
python experimentos/organelos/veto_muro/identidad_veto_muro.py            # arnés corto (~80 s); --largo (~+150 s)
python experimentos/organelos/veto_muro/corre_veto_muro.py --humo
python experimentos/organelos/veto_muro/corre_veto_muro.py --humo --reanuda
python experimentos/organelos/veto_muro/corre_veto_muro.py --serie --pool 2           # DESPUÉS de patas_muro
python experimentos/organelos/veto_muro/corre_veto_muro.py --serie --pool 2 --reanuda # sólo si se cortó o dio NO SE LEE
python experimentos/organelos/veto_muro/corre_veto_muro.py --replica --pool 2
python experimentos/organelos/veto_muro/corre_veto_muro.py --bloque <serie>/resumen.json,<replica>/resumen.json
```

## 13. Cambios por auditoría antes de datos (29-sep)
El auditor dejó el diseño LISTO CON CAMBIOS. Todo se aplicó antes de cualquier dato de 53701–53740. **La sec. 8 (predicciones) no se tocó
en ningún momento después de firmarse.**

- **Entre el sha del humo (`a58aeee6b38c89be`) y `3e7e34544e2682b3` (C1):** un solo cambio, en la sec. 12 y sólo en ella. Se reemplazó
  la línea del humo ("ver humo_salida.txt… tiempos medidos allí") por los tiempos medidos por brazo (tpv 22.0 s … o1 38.3 s; ≈ 169 s por
  semilla, ≈ 845 s a T 100 000), se re-estimó la serie con pool 2 (≈ 2.4 h, entre 2.2 h y 4 h) y se añadió la nota de que el humo se miró
  DESPUÉS de firmar la sec. 8, no la cambia, y ya muestra el patrón de vu (h≤200 0.00, vida del hijo 1512, h600 0.24, mundo A+C 2.16).
- **C2:** secs. 9.1 y 10. Si PA y PB pasan y PD cae, sólo se cierra el veto como pieza que lee qué necesidad golpea; "proteger al recién
  nacido" queda como hipótesis distinta, no refutada.
- **C3:** "en el umbral" se extiende a PD (gana = 13 exacto o dif entre +15 y +17) y a PC (= 15 exacto, en FUNCIONA); el runner guarda
  `umbral` por puerta y dice cuáles (sec. 5; `corre_veto_muro.py`, `lee()`). Arnés (normal y largo) y humo re-corridos con el sha nuevo.
- **H-5:** sec. 2 (y 9.4). Un mordisco vetado escribe `_rech[pos] = t + MEMORIA_RECHAZO` (heredado del tronco); en esta pista
  MEMORIA_RECHAZO = 20.
- La letra (PA, PB, PD, PC, V1–V6), los brazos, las semillas y el carro (TVPISO 7653cd267790500b) no cambian.
