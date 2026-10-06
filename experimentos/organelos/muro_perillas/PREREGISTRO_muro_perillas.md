# PREREGISTRO — PERILLAS DEL MURO. Paso 1: EL MAPA (genomas fijos, sin evolución) · Paso 2: los genes de O1 desde apagado bajo el montaje de perillas (1-oct-2026, ingeniero genético; MODO RÁFAGA: sondas, nada se declara)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).
Encargo del director: "qué muro tan duro, ¿dónde está nuestro gen perdido?". Carpeta nueva `experimentos/organelos/muro_perillas/`; nada existente se editó
(todo se importa por sha). ERR candidato: ERR-191 (no abierto; el 190 ya se usó). **La sección 4 (predicciones del mapa) se escribió ANTES de correr ninguna corrida del mapa.**

## 0. Primera línea
**O1 no se puede "apagar" hacia el tronco: son arquitecturas distintas** (tabla por letra del linaje y política escrita contra celdas Kenyon de v14.3/FABRICA).
La base del mapa es "O1 con cada mecanismo neutralizado". El único organismo de referencia YA EXISTENTE con un mecanismo apagado es
`carrera_escuderias/carros/CTRL_O1_SINLIMPIA.py` (`be029b0a1b8d6634`, O1 con `limpia = False`): el arnés prueba que el gen LIMPIA en 0 lo reproduce bit a bit.
Con los genes de fábrica el carro es O1 (`99436afa2715f028`) bit a bit (salida entera; arnés).

## 1. Qué ya está medido (no se repite; recalculado hoy con la letra del juez desde los crudos)
| genoma | serie | R0 real med | cruzan/180 | establecidos | fund med | mayorías |
|---|---|---|---|---|---|---|
| O1 fábrica, fundador limpio | r2o1mono 9101–9120 | 0.941 | 144 | 155 | 0 | 20/20 |
| O1 fábrica, fundador NO limpio | sellada_mono 5001–5020 | 0.941 | 117 | 141 | 0 | 18/20 |
| **O1 sin limpieza** (CTRL_O1_SINLIMPIA) | sellada_sinlimpia 5001–5020 | **0.216** | **0** | **0** | **53** | 0/20 (pareado 0/20 contra mono) |
| O1 fundador borra | sellada_fundborra 5021–5040 | 0.941 | 148 | 157 | 0 | 20/20 |
| o1_evo (4 constantes desde fábrica, selección) | serie 617201–617220 | 0.931 | 128 (o1 135, neutro 81) | — | — | la selección baja PRUEBA (19/20) y sube PISO (17/20) sin ganar cruce |
Del genetista (`investigacion_20261001/FABLE_gen_perdido.md`, verificado en `boca_buena/tabla_bb.txt` por él, no por mí): consigna de la boca EN U (MARGEN 0) = 0.000;
U+0.10 / U+0.40 = 0.92 / 0.95; "todo" (sin consigna) 0.895; PRUEBA plana; patas no se separan del ruido.

## 2. Instrumento (Paso 1)
- Carro `O1_MURO_GEN` (`construye_muro_perillas.py`, 15 anclas sobre el texto de O1.py, cada una exactamente una vez; chequeo `ast` de que las 4 constantes
  no se leen como globales). 6 genes CRUDOS por cuerpo: MARGEN, PRUEBA, PEN_OTRO, PISO (las constantes de O1, como `O1_PAS` de o1_evo) + LIMPIA y HUECO
  (las dos reglas: limpieza v2 y "sin blanco ir al hueco mayor"; activas si el gen > 0.5). Con genes fijos (σ 0, sin cámara) ES O1 con las constantes escritas a
  mano (arnés (C) cableado, gen por gen) — el mismo instrumento que propone el genetista (O1_PAS σ 0), más las dos reglas y la pista mixta.
- `PS_POR_LINAJE`: PISTA MIXTA = cada linaje con su genoma fijo (también al refundar); se reporta por linaje quién cruza y quién paga (B+D, limpiezas físicas).
- Cada corrida ES `corre_v143.tarea` (`24100621c450da22`, regla 14, arnés (R)): pista vieja `9f47c65e438e0ff4`, juez `6a68f640a7832f12`, monocultivo de 9, L 360,
  36 objetos, fundador limpio 1, T 100 000. Medidas por corrida: linajes que cruzan (`cruza_real`) de 9, R0 real mediano, fundadores por linaje, establecidos
  (0 fundadores tras 10k), vida, causas, B+D, A+C, mundo A+C, fracción de pasos sin nada bueno.
- Semillas NUEVAS 883001 (s1) y 883002 (s2) (grep 1-oct en .py/.md: 883xxx no aparece). Un proceso, ≤ 6 corridas por proceso, regla de CPU (tope 6) en el runner.

## 3. Rejilla (lotes de ≤ 6 corridas; prioridad A > B > C > M > D; s2 después)
| lote | genomas (sobre O1 de fábrica salvo `off+…`) | pregunta |
|---|---|---|
| A | MARGEN 0 · 0.03 · 0.06 · 0.10 · fab (0.25) · 0.5 ("todo") | ¿acantilado o rampa entre 0 y 0.10? ¿"todo" paga casi como fábrica? |
| B | PISO 0 · 0.4 · 0.6 · 1.0 · PEN_OTRO 1.0 · PRUEBA 0.0 | eje PISO (óptimo y techo); PEN_OTRO y PRUEBA un punto cada uno |
| C | LIMPIA 0 · HUECO 0 · MARGEN 0.1+PISO 0.6 · MARGEN 0.06+PISO 0.4 · MARGEN 0.1+PISO 1.0 · off (todo apagado: MARGEN 0, PEN 1, PISO 1, LIMPIA 0, HUECO 0) | las reglas; pares MARGEN×PISO; la base |
| M | mixta 8×PISO 0.2 + 1×PISO 0.6 · 8×0.6 + 1×0.2 · 8×fab + 1×LIMPIA 0 · 8×LIMPIA 0 + 1×fab | bien público: ¿el que limpia menos cruza más a costa de los vecinos? |
| D | desde `off`: +MARGEN 0.25 · +PISO 0.2 · +LIMPIA 1 · +MARGEN+PISO · +MARGEN+LIMPIA+PISO · +MARGEN+LIMPIA+PISO+PEN 0.35 | ¿hay camino de un paso desde el apagado del genetista? |

## 4. Predicciones firmadas del mapa (cruzan/9 en s1; antes de correr; p = mi confianza)
| # | predicción | rango | p |
|---|---|---|---|
| M1 | MARGEN 0 → 0/9 (consigna en U: extinción) | 0 | 0.80 |
| M2 | rampa, no acantilado: MARGEN 0.06 ≥ 3/9 y 0.03 ≥ 1/9 | | 0.45 |
| M3 | MARGEN 0.10 ≥ 5/9; fab 7–9/9; "todo" (0.5) 5–8/9 (el mecanismo de consigna vale ≤ 2 linajes) | | 0.65 |
| M4 | PISO 1.0 < 4/9 (casi sin limpieza hunde); PISO 0 y 0.4 dentro de ±2 de fab | | 0.65 |
| M5 | PEN_OTRO 1.0 y PRUEBA 0 dentro de ±2 de fab (planos) | | 0.70 |
| M6 | LIMPIA 0 → 0/9; `off` → 0/9 | | 0.90 / 0.95 |
| M7 | HUECO 0 dentro de ±2 de fab (quedarse quieto casi no cuesta: la vista es total) | | 0.55 |
| M8 | desde `off` NINGÚN gen solo pasa de 1/9 (valle de 2+ pasos desde el apagado del genetista); +MARGEN+LIMPIA+PISO ≥ 3/9 | | 0.60 |
| M9 | mixta 8×0.2+1×0.6: el linaje con PISO 0.6 muerde menos B+D que la mediana de sus vecinos y cruza (polizón) | | 0.55 |
| M10 | mixta 8×LIMPIA 0+1×fab: el único que limpia muere más (B+D ≥ 2× la mediana de los otros) y cruzan ≤ 2/9 | | 0.60 |
| V | veredicto de la primera línea: PENDIENTE / VALLE DE UN PASO / VALLE DE 2+ / NO SE PUEDE MEDIR | | 0.20 / 0.25 / 0.40 / 0.15 |
Lectura (fijada antes): PENDIENTE = existe un orden de prendido desde `off` en que cada paso suma ≥ 2 linajes; VALLE DE UN PASO = el primer paso no paga pero el
segundo sí; VALLE DE 2+ = hacen falta ≥ 3 genes a la vez para pasar de 1/9. Con una semilla nada se declara: s2 replica el eje que cargue.

## 5. Las cuatro trampas (Paso 1)
Canal simétrico: nadie lee ni escribe la pizarra; en la mixta los genomas son fijos, no viajan. Acierto sin balancear: la medida es `cruza_real` del juez. Mundo
que se come la comida: se reporta mundo A+C y la fracción de pasos sin nada bueno por genoma (un genoma que cruza pelando el mundo se dice). Sitios fijos:
posiciones y orden de turno del rng de la pista; semillas nuevas.

## 7. Diagnóstico del arnés (31/33) y de la contradicción LIMPIA=0 (1-oct, 12:20–12:40; el coordinador corrió la cadena: humo, lotes M, C, A, B, D)
- **(R) regla 14 FALLA → defecto del ARNÉS, no del instrumento.** Verificado a T 500: los únicos campos que difieren entre `corre_muro_perillas.tarea`
  (genes de fábrica) y `corre_v143.tarea('O1')` son `id` de cada linaje e `ids` de la pista (`O1_MURO_GEN#i` contra `O1#i`: la pista pone el nombre del carro;
  mismo tropiezo que anotó perillas, sec. 11.1). Con el nombre normalizado son idénticos campo a campo. Corregido en el arnés y en el humo (`sin_ids`); la
  prueba ahora exige que NINGÚN otro campo difiera. Las corridas del mapa siguen VÁLIDAS: la identidad corta (fábrica == O1 salida entera, LIMPIA 0 ==
  CTRL_O1_SINLIMPIA, neutro == O1, todo apagado != O1) pasó en cada lote y las 31 pruebas restantes del arnés pasaron.
- **(C) "genes se mueven" FALLA → defecto del ARNÉS.** A T 3000 con fundador limpio ningún linaje se extinguió (0 refundaciones), así que no hubo cámara que
  medir; la prueba exigía fundadores > 9. Corregido: el movimiento se mide en los VIVOS (hijos con `_gen` mutado, profundidad > 1, partos > 0) y la cámara
  sólo cuando hubo refundaciones. Nada de esto toca el carro ni los JSON escritos.
- **LIMPIA=0 clonal 5/9 contra 0/180 del registro → NO es el instrumento: es `fundador_limpio` (ENMIENDA 5).** `fila()` sobre el crudo viejo de
  sellada_sinlimpia reproduce el registro (0/180, R0 0.217, 52.5 fundadores, B+D 2). En el mapa, por linaje: los establecidos tienen B+D = 2 (una prueba de
  B y una de D por instancia) y los que se hunden tienen B+D ≈ fundadores + 2 (lin 1: 484 fund, 489 B+D; lin 7: 237, 243). **Cada refundador limpio nace con
  tabla vacía y PRUEBA B y D una vez antes de morir: los linajes que se hunden limpian el mundo con sus nacimientos** (~750 malos por 100k). Con fundador NO
  limpio (sellada 5001–5020) el refundador conservaba la tabla y nunca mordía B/D → 0/180. Comparación canónica (CTRL_O1_SINLIMPIA por `corre_v143.tarea`,
  s 883001, T 100k, campo a campo) en `compara_sinlimpia.py` → `compara_sinlimpia_salida.txt` (la lanza el vigía `espera_y_corre.py` al bajar la CPU, junto
  con el arnés corregido → `identidad_muro_perillas_salida2.txt`). Candidato a ERR-191 (candidato, no abierto; el 190 se usó el 1-oct para otra cosa): "con fundador limpio la pista regala limpieza por la prueba de los
  refundadores: un carro SIN limpieza cruza en monocultivo a costa de 2–4 linajes que no paran de nacer y morir".

## 5 bis. Estado al cierre (1-oct, 11:45): CONSTRUIDO, NO CORRIDO — regla de CPU
Durante toda la sesión hubo 7 `python.exe` de trabajo ajenos (o1_libre_f2 pool 2 desde 08:14 en i8/20 a las 11:30; perillas réplica pool 2 desde 11:02;
p8 serie pool 2 desde 11:29; regimen rejilla desde 11:30; 16 núcleos lógicos). Tope 6 → el runner se niega (`--forzar_cpu` sólo para el coordinador).
No se corrió ni el arnés de pista (es una simulación). Lo que sí se verificó sin CPU: `prearnes_unitario.py` (23/23: GEN0 == O1, fábrica == O1,
LIMPIA 0 == CTRL_O1_SINLIMPIA, neutro == O1, pista mixta, cada gen actúa, el parto con `_gen` no revienta, `fila()` sobre un crudo real, `lee_mapa()`,
6 casos sintéticos de la letra). **Pendiente al liberarse CPU (en este orden): `identidad_muro_perillas.py` → `--humo` → lotes A, B, C, M, D, A2, B2, C2, M2.**
Shas al cierre: `construye_muro_perillas.py` 4b7092184a16f4ca · `carros/O1_MURO_GEN.py` 2f88a0b447b48d32 · `carros/O1_MURO_GEN0.py` 36e00ceeb41b8ccb ·
`corre_muro_perillas.py` (ver informe) · `identidad_muro_perillas.py` (ver informe) · `prearnes_unitario.py` 2245abc9182b7c38.
Lectura gratis (0 CPU, JSON de o1_evo, "firma del polizón" de la ficha 4 del genetista; NO preregistrada, sólo orienta): dentro de semilla, Spearman PISO~cruza
> 0 en 11/20 (o1pas), 11/20 (o1ctl), 10/17 (o1neu); el linaje con PISO máximo cruza en 16/20, 17/20 y 12/17 contra 14.2, 14.9 y 9.0 esperados. Señal débil
y de poder bajo (la variación de PISO dentro de una semilla es ~σ): no apoya ni tumba el bien público; lo decide el lote M.

## 6. Paso 2 (construido, NO corrido; se activa sólo si el mapa muestra PENDIENTE o VALLE DE UN PASO)
Mismo carro con los genes heredables desde `BASE` (= APAGADO del constructor; se fija tras el mapa y se escribe aquí), montaje de perillas importado por diseño
(no por archivo: `corre_perillas.py` está atado a su carro y a su mundo; aquí la cadena, la siembra de establecidos, los dos relojes y la letra se reescribieron
genéricos en los genes, con las mismas constantes a priori: σ 0.03, δ 0.01, una mutación por parto en un gen, cámara continua, 5 pasajes de 100k, siembra de
linajes sin refundación en la segunda mitad, V7a profundidad neutra ≥ 30 y V7b refundaciones ≥ 3 000 en ≥ 16/20, PG margen 0.05 en ≥ 13/20, PC ≥ 13/20 y +10). [ANULADO el 5-oct: la letra vigente es la de la sec. 12: PG = (a) margen 0.03 ∧ (b) zona 0.06; V7 sobre neu y sel.]
Brazos: sel, neu (PS_LEE 0), fab (O1), off (BASE). Semillas: pasajes 883100 + 10 i + p, pruebas 883301 + i; réplica 883500 + 10 i + p y 883701 + i.
`GEN_LETRA` (el gen de PG) queda en None hasta que el mapa lo señale; el runner se niega a correr la serie sin él y sin shas fijados. Nulo de deriva: el de
`perillas/nulo_perillas.py` (misma regla de mutación: P(gen > 0.05) 0.22, > 0.10 0.07 con δ 0.01). Si el mapa muestra VALLE DE 2+ o dilema del bien público
(M9/M10), NO se corre tal cual: ver la propuesta en el informe (dos cámaras, clonal contra mixta; o genes ligados).
```
python experimentos/organelos/muro_perillas/construye_muro_perillas.py --verifica
python experimentos/organelos/muro_perillas/identidad_muro_perillas.py
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --humo
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --mapa --lote A      # luego B, C, M, D, A2, B2, C2, M2 (un proceso por lote)
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --lee
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --serie --pool 2 [--reanuda]   # SOLO el coordinador, Paso 2, tras fijar GEN_LETRA y shas
```

---
# PARTE II (5-oct-2026) — PASO A: el mapa sin la limpieza regalada · PASO B: PERILLAS DEL MURO (serie, CONFIRMATORIO)

## 8. Lo que dejó el mapa de dos semillas (1-oct; fundador limpio; `datos/mapa`, `mapa*.log`; nada declarado)
| genoma | cruzan/9 (s1, s2) | R0 real med | lectura |
|---|---|---|---|
| MARGEN 0 / 0.03 / 0.06 / 0.10 / fab 0.25 / "todo" 0.5 | 0,0 / 0,4 / 3,8 / 8,9 / 4,8 / 5,5 | 0.00 / 0.86 / 0.88 / 0.94 / 0.92 / 0.93 | **rampa** (M2 ✔): 0 letal (vida 200), 0.03 ya vive (8–9 establecidos), satura en 0.06–0.10 |
| LIMPIA 0 | 5, 6 (B+D 2) | 0.95 | artefacto: los refundadores limpios prueban B y D (sec. 7) |
| off (todo apagado) / off+MARGEN 0.25 / off+PISO / off+LIMPIA | 0,0 / 5,6 / 0,0 / 0,0 | — | "MARGEN solo cruza" = 11/18 con **B+D 2**: nadie limpia; es LIMPIA 0 con otro nombre |
| off+MARGEN+LIMPIA+PISO (+PEN) | 7,7 / 7,6 | 0.94 | el conjunto de O1 |
| PISO 0 / 0.4 / 0.6 / 1.0 · PEN_OTRO 1 · PRUEBA 0 · HUECO 0 | 15 / 10 / 16 / 11 · 12 · 12 · 13 (de 18) | 0.90–0.95 | planos dentro del ruido de dos semillas (fab 12) |
| mixtas PISO · 8×fab+1×LIMPIA0 · 8×LIMPIA0+1×fab | 15, 15 · 12 · 12 | — | el único limpiador entre 8 que no: R0 0.002, 487 fund (×2 semillas) |
Veredicto del mapa (exploratorio, 2 semillas): **PENDIENTE en MARGEN con el resto de O1 puesto; VALLE de 2+ desde el apagado del genetista** (nada suelto
pasa de 0 salvo MARGEN, y MARGEN suelto sólo cruza por la limpieza que regala el fundador limpio). Predicciones del 1-oct: M1 ✔, M2 ✔ (rampa), M3 ✘ (fab 4/9 en s1),
M4 ✘ (PISO 1.0 no hunde: 7, 4), M5 ✔, M6 ✘ en LIMPIA (artefacto) ✔ en off, M7 ✔, M8 ✔ (valle de 2+ desde off), M9 ✔ débil, M10 ✔.

## 9. PASO A — sonda con fundador NO limpio (`--fl 0`; sin tocar los JSON del 1-oct, que llevan sufijo nuevo `_fl0`)
Pregunta: ¿la rampa de MARGEN y "MARGEN solo cruza" se sostienen cuando los refundadores NO limpian (regla de la sellada 5001–5020)? Lotes A, A2, D, D2 (rampa y
desde apagado, dos semillas) y X, X2 (LIMPIA 0 y fab clonales). Regla de fundador de las series registradas del muro: **fundador limpio 1 (ENMIENDA 5)** en
r2o1mono 9101–9120 = "O1 18–20/20" (`carrera_escuderias/juez.py:536-537`), `tronco_v14_3/corre_v143.py:56` (`FL = 1`, :88), `o1_evo/corre_o1_evo.py:8,345`,
termostato (`reunion/opusB/corre_termostato.py:7`: corre por `corre_pas.tarea` = `corre_v143.tarea`); la sellada_mono 5001–5020 (18/20) y sellada_sinlimpia (0/20)
son con fundador NO limpio (`juez.py:536`, por defecto 0 fuera de r2). Predicciones firmadas antes de correr (cruzan/9 por semilla, fl 0):
| # | predicción | p |
|---|---|---|
| A1 | off+MARGEN 0.25 (nadie limpia) → 0/9 en las dos semillas; LIMPIA 0 clonal → 0/9 ×2 (como la sellada) | 0.85 |
| A2 | la rampa de MARGEN con el resto de O1 se sostiene: 0 → 0/9; 0.03 ≤ 0.06 ≤ 0.10 en suma de dos semillas; 0.10 ≥ 10/18 | 0.70 |
| A3 | fab (O1) con fl 0 ≥ 10/18 y mayoría en ≥ 1/2 semillas (sellada: 18/20) | 0.75 |
| A4 | off, off+PISO, off+LIMPIA → 0/9 ×2; off+MARGEN+LIMPIA+PISO ≥ 8/18 | 0.80 |
Arnés: caso nuevo (R) "tarea(fl=0, fábrica) == corre_v143.tarea('O1') con FL 0 (salvo ids), pista.fundador_limpio 0, FL restaurado". Costo estimado 28 × ~90 s ≈ 42 min.

## 10. PASO B — PERILLAS DEL MURO (serie): MARGEN como gen desde el arranque, el resto de O1 en fábrica
**Hipótesis (director):** en la pista vieja, con el montaje que prendió GV en perillas, la selección por persistencia sube el margen de la boca de O1 desde el
arranque y el genoma que deja cruza más que el que deja la deriva.
**Mecanismo y memoria nueva:** carro `O1_MURO_GEN` (sec. 2) con `BASE = (ARRANQUE_MARGEN, 0.5, 0.35, 0.2, 1, 1)`: sólo MARGEN parte del arranque; PRUEBA, PEN_OTRO,
PISO, LIMPIA y HUECO parten de fábrica y también mutan (la mutación cae en uno de los 6 genes al azar: MARGEN recibe 1/6 de los eventos; declarado). Memoria
nueva: 6 floats y un entero por cuerpo. Montaje de perillas tal cual: una mutación por nacimiento en un gen (σ 0.03, δ 0.01, recorte MARGEN [0, 0.6]), cámara
continua (cada refundación copia mutado el genoma del cuerpo actual de otro linaje), 5 pasajes de T 100 000, siembra = vivos de los últimos 5 000 pasos de los
linajes sin refundación en la segunda mitad (respaldo: menos refundaciones), neutro `PS_LEE 0` pareado (mismas semillas), prueba monomórfica T 100 000 con el
genoma MEDIANO de la siembra final (sel, neu) y los fijos fab = O1 (techo) y off = BASE (piso). n = 20 cadenas.
**Regla de fundador de la serie (`FL_SERIE`):** 1 = la canónica del muro (sec. 9). Si el PASO A muestra que con fl 0 la rampa de MARGEN se sostiene y "MARGEN
solo" cae a 0, las dos reglas son defendibles: la canónica decide (es la letra con la que O1 cruzó 18–20/20 y con la que se midió el mapa) y fl 0 queda como
SEGUNDA SERIE descriptiva (mismo runner, `FL_SERIE = 0`, semillas 884xxx), porque en fl 1 parte de la ventaja de un MARGEN alto puede venir de linajes vecinos
que se hunden y limpian (sec. 7). Decisión escrita antes de la serie en sec. 11.
**Arranque (`ARRANQUE_MARGEN`):** MARGEN 0 es letal (0/18, vida 200). `--humo_cadena` (1 pasaje sel de T 20 000 desde BASE) comprueba si la cadena muta antes
de "extinguirse" (en esta pista un linaje nunca se extingue del todo: cada refundación es una mutación; lo que puede pasar es que ninguna refundación suba MARGEN
y la cadena quede clavada en 0). Si el humo muestra MARGEN de la siembra ≤ 0.01 y 0 partos, el arranque pasa a **0.03** (primer escalón medido: R0 0.83–0.89,
8–9 establecidos) y se escribe en sec. 11 antes de la serie.
**Nulo de deriva de ESTE gen** (`nulo_margen.py` → `nulo_margen_salida.txt`; clip [0, 0.6], σ 0.03, δ 0.01, p 1/6 por evento): desde 0, mediana estacionaria
0.011, P(> 0.03) 0.35, P(> 0.05) 0.22, P(> 0.10) 0.07 por linaje; la MEDIANA de una siembra neutra de 45 muestras: 0.007 (P > 0.03 = 0.09, P > 0.05 = 0.012);
pareado, P(sel > neu + 0.03) por cadena bajo el nulo = 0.05 → P(≥ 13/20) ≈ 1e-11 (con arranque 0.03: 0.06 → 1e-11). Dosis-respuesta medida: 0.03 → 4/18,
0.06 → 11/18, 0.10 → 17/18 (fab 12/18). **Margen de PG = 0.03** (= `MARGEN_G`): es el nulo de este gen y el primer escalón de la rampa; **zona funcional
descriptiva 0.06** (`FUNC_MARGEN`): cuántas cadenas sel llegan.
**LA LETRA (`corre_muro_perillas.lee_serie`; 6 casos sintéticos en el arnés (F)).** Validez (una falla: NO SE LEE): V1 completa (40 cadenas, 80 pruebas, 0 abortos,
contabilidad coherente) · V2 el mundo paga el gen: fab > off en linajes que cruzan en ≥ 16/20 · V4 estado por worker (carro, PERILLAS 1, `fl` = FL_SERIE, σ/δ/cámara/
PS_LEE por brazo, pruebas con un solo genoma = el del brazo) · V5 desde el arranque (pasaje 0 con 9 fundadores de BASE; los demás de la siembra; toda refundación de
la cámara) · V7a profundidad mutacional neutra ≥ 30 y V7b refundaciones por cámara neutras ≥ 3 000, cada una en ≥ 16/20. Puertas (empates en contra): **PG**
MARGEN mediano de la siembra final de sel > neu + 0.03 en ≥ 13/20 · **PC** sel > neu en linajes que cruzan (pareado) en ≥ 13/20 **y** suma(sel) ≥ suma(neu) + 10.
FUNCIONA = válido, PG y PC · MODESTO = una de las dos (con matiz) · NO = ninguna · EN EL UMBRAL ±1 · bloque serie + réplica: si coinciden vale, si no el menor;
NO SE LEE manda. **Obligatorio en el informe:** sel vs fab (O1 de fábrica; fab ES O1), sel vs off, neu vs off; mundo (B+D, A+C, fracción sin nada bueno,
fundadores) por brazo; **mayorías (≥ 5/9 cruzan) por brazo**: la definición del muro; cadenas sel con MARGEN ≥ 0.06.
**Vocabulario:** FUNCIONA ×2 → frase máxima "en la pista vieja, la selección sube desde [arranque] el margen de la boca de O1 y el genoma que deja cruza más
que el de la deriva". NUNCA "la selección cruzó el muro" salvo que sel alcance mayoría en ≥ 16/20 pruebas como O1 (`sel_mayoria_como_O1`), y aun así "es O1 con
una perilla libre, no el tronco". MODESTO → se registra, no se repite. NO con V7 → "con reloj medido, la selección no subió el margen desde el arranque".
**Predicciones firmadas (antes de la serie):**
| # | predicción | rango | p |
|---|---|---|---|
| B1 | fab suma de linajes que cruzan; off | [100, 150]; [0, 10] (arranque 0) · [20, 60] (arranque 0.03) | 0.75 |
| B2 | V2 pasa (fab > off en ≥ 16/20) | | 0.90 |
| B3 | PG pasa (MARGEN sel > neu + 0.03 en ≥ 13/20) | esperado 14–18/20 | 0.60 |
| B4 | MARGEN mediano final: sel; neu | [0.04, 0.12]; ≤ 0.02 | 0.55 |
| B5 | cadenas sel con MARGEN ≥ 0.06 | ≥ 8/20 | 0.50 |
| B6 | suma de cruzan: sel; neu | [60, 120]; [0, 40] | 0.55 |
| B7 | PC pasa (par ≥ 13/20 y +10) | | 0.55 |
| B8 | sel NO alcanza mayoría como O1 (< 16/20 mayorías); fab sí (≥ 16/20) | | 0.80; 0.70 |
| B9 | los otros 5 genes de sel no se alejan de fábrica más de 0.05 en mediana (deriva con δ hacia abajo, salvo PISO) | | 0.60 |
| B10 | relojes neutros: profundidad mediana [40, 90]; refundaciones [3 500, 5 500] (vida corta en el arranque: más refundaciones que en perillas) | | 0.60 |
| B11 | V7a y V7b pasan | | 0.85; 0.90 |
| V | SERIE: FUNCIONA / MODESTO / NO / NO SE LEE | | 0.40 / 0.25 / 0.15 / 0.20 |
**Control que puede fallar:** neu (su MARGEN deriva hacia arriba → PG cae; o su genoma mediano cruza igual → PC cae). **Refuta:** NO con V7. **Debilita:** MODESTO
por PG sin PC (el gen sube pero el cruce no lo sigue: la rampa satura por encima de lo que la selección alcanza, o el cruce lo deciden los vecinos que se hunden).
**Trampas:** canal simétrico (la cámara es igual en sel y neu; nadie usa la pizarra; la prueba no tiene cámara) · acierto sin balancear (medida = cruza_real del
juez y el valor del gen; pareado) · mundo que se come la comida (se reporta A+C, B+D y sin-bueno por brazo; un MARGEN alto come más: si sel gana pelando el mundo,
se dice) · sitios fijos (semilla nueva por pasaje y prueba; posiciones y turno del rng de la pista).
**Semillas NUEVAS** (grep 5-oct en .py/.md fuera de esta carpeta: sólo 883001/883002 aparecen, ya en el registro del mapa): serie pasajes 883100 + 10 i + p
(883100–883294), pruebas 883301–883320; réplica 883500 + 10 i + p, pruebas 883701–883720; humo 883990–883998; segunda serie fl 0 (si se decide): pasajes
884100 + 10 i + p y pruebas 884001–884020.
**Instrumento:** `corre_muro_perillas.py --serie --pool 2 [--reanuda]` (tope pool 2; JSON por trabajo y por pasaje, ERR-54; `--reanuda` salta lo hecho, reintenta
abortos y rearma cadenas cortadas; candados: shas fijados en `SHAS_PROPIOS`, veredicto previo, regla de parada, git limpio del preregistro, runner, constructor y
carros). Humo de main de punta a punta (ERR-42): `--humo_serie` (1 proceso: 2 cadenas × 2 pasajes de 5k + pruebas sel y neu de 20k = 6 corridas) y
`--humo_serie --reanuda` (fab y off, y la letra). Costo: se mide en el humo (sec. 11); estimado por índice 14 corridas × 100–170 s ≈ 2 000 s; serie ≈ 40 000 s de
CPU → **≈ 5.5 h con pool 2**.
```
python experimentos/organelos/muro_perillas/construye_muro_perillas.py --verifica
python experimentos/organelos/muro_perillas/identidad_muro_perillas.py
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --humo_cadena
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --humo_serie && python experimentos/organelos/muro_perillas/corre_muro_perillas.py --humo_serie --reanuda
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --serie --pool 2 2>&1 | tee experimentos/organelos/muro_perillas/serie_pool2.log      # SOLO el coordinador
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --serie --pool 2 --reanuda 2>&1 | tee -a experimentos/organelos/muro_perillas/serie_pool2.log
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --replica --pool 2    # sólo por la regla de parada
python experimentos/organelos/muro_perillas/corre_muro_perillas.py --lee_serie <carpeta>
```

## 11. Resultados del PASO A (5-oct, 15:05–16:22 y 16:35–; `pasoA.log`, `pasoA2.log`, `datos/mapa/*_fl0.json`) y decisiones ANTES de la serie
**Arnés con la opción nueva:** `identidad_muro_perillas_salida4.txt` 33/34: pasa el caso nuevo (R) fundador NO limpio (`tarea(fl=0)` == `corre_v143.tarea('O1')`
con FL 0, pista.fundador_limpio 0, FL restaurado, difiere de fl 1); la única falla fue (K) porque BASE dejó de ser APAGADO ese mismo día (prueba actualizada:
BASE = arranque + fábrica; `off`/`off+` sobre APAGADO; `base+` sobre BASE). Re-corrida final → `identidad_muro_perillas_salida5.txt`.
**Error propio (5-oct 16:25, corregido antes de leer):** `genoma('off+…')` usaba BASE, que ese día pasó a ser el arranque de la serie: los 12 JSON fl 0 del
lote D de las 15:48–16:17 llevaban etiqueta falsa (`off+MARGEN=0.25 (fl 0)` era `fab`, bit a bit igual). Apartados en `datos/mapa/invalidos_etiqueta_fl0_D/`
con LEEME; el lote D fl 0 se repitió con la etiqueta corregida. Los JSON del 1-oct (fl 1) no se tocaron y son correctos (BASE era APAGADO; el genoma va escrito).
**Tabla (cruzan/9 en s883001, s883002; R0 real mediano; fundadores medianos; B+D):**
| genoma | fl 1 (1-oct) | **fl 0 (PASO A)** | predicción |
|---|---|---|---|
| MARGEN 0 | 0, 0 · R0 0.00 · vida 200 | 0, 0 · R0 0.00 · vida ~19 900 (!) · fund 2.5 | A2 ✔ (letal también: nadie pare; con fl 0 el cuerpo no muere pero no se reproduce) |
| MARGEN 0.03 | 0, 4 · 0.86 | 0, 4 · 0.86 · 9/9 establecidos | A2 ✔ |
| MARGEN 0.06 | 3, 8 · 0.88 | **7, 8** · 0.91 | A2 ✔ (sube más que con fl 1) |
| MARGEN 0.10 | 8, 9 · 0.94 | 7, 9 · 0.94 | A2 ✔ (≥ 10/18) |
| fab 0.25 (O1) | 4, 8 · 0.92 | 5, 8 · 0.93 · mayoría 2/2 | A3 ✔ |
| "todo" 0.5 | 5, 5 · 0.93 | **0, 0** · 0.29 · 37.5 fund | sin consigna la boca pela el mundo (A+C 600, mundo AC 1.3) y sin la limpieza regalada nadie se establece |
| LIMPIA 0 | 5, 6 · 0.95 · B+D 2 | **0, 0** · 0.24 · 51.5 fund · B+D 2 · mundo AC 0.56 | A1 ✔ = la sellada (0/180) |
| off+MARGEN 0.25 (nadie limpia) | 5, 6 (B+D 2) | (lote D fl 0, en curso) | A1 |
| off / off+PISO / off+LIMPIA / off+MARGEN+LIMPIA+PISO | 0,0 / 0,0 / 0,0 / 7,7 | (lote D fl 0, en curso) | A4 |
**Lectura del PASO A (dos semillas, sonda):** la **rampa de MARGEN con el resto de O1 se sostiene sin la limpieza regalada** (0/0 → 0/4 → 7/8 → 7/9: igual o
mejor que con fl 1), y lo que NO se sostiene es todo lo que vivía de los refundadores: LIMPIA 0 cae a 0/18 (confirma la sellada y ERR-191) y "todo" (0.5) cae
a 0/18. Con fl 0 la pista es más exigente y más limpia como instrumento: el cruce lo paga el propio linaje.
**ERR-191 (candidato, confirmado por el PASO A; redactado para que el coordinador lo abra):** *Con `fundador_limpio = 1` (ENMIENDA 5) cada refundación crea
una instancia nueva del carro con tabla vacía; un carro con PRUEBA prueba B y D una vez por instancia antes de morir. Los 2–4 linajes que se hunden en todo
monocultivo de 9 refundan cientos de veces y así retiran ~500–750 objetos malos por 100k pasos: una limpieza que ningún gen paga. Efecto medido: O1 sin limpieza
cruza 11/18 con fl 1 (B+D = 2 por linaje establecido) y 0/18 con fl 0 (sellada 5001–5020: 0/180); "todo" 10/18 contra 0/18. Afecta a toda comparación entre
carros que limpian y carros que no en la pista con fundador limpio (r2, corre_v143, o1_evo, termostato, mapa del 1-oct); no afecta a O1 de fábrica (5–8/9 en
las dos reglas). Remedio: reportar siempre B+D por linaje y fundadores; para preguntas sobre la limpieza, fl 0 o un fundador limpio que no pruebe letras ya
mordidas por el linaje (cambio de pista: fuera de este bloque).*
**Decisión 1 — regla de fundador de la serie:** las dos son defendibles; **decide fl 1 (canónica: `FL_SERIE = 1`)** porque es la letra con la que O1 cruzó
18–20/20 y con la que se midió el mapa y perillas; la rampa de MARGEN es la misma con las dos reglas (A2), así que la pregunta de la serie (¿sube MARGEN desde el
arranque?) no depende de la regla. **fl 0 queda como SEGUNDA SERIE descriptiva** (`FL_SERIE = 0`, semillas 884xxx) si la primera da FUNCIONA o MODESTO: separa
lo que el linaje paga de lo que le regalan los vecinos.
**Decisión 2 — arranque:** la escribe el humo `--humo_cadena` (abajo).

### 11 bis. Cierre del PASO A (17:10) y las dos decisiones
**Lote D con fl 0 (etiqueta corregida; `pasoA2.log`):** off+MARGEN 0.25 → **0, 0** (R0 0.24, 54 fund, B+D 2: nadie limpia) · off / off+PISO / off+LIMPIA → 0, 0 ·
off+MARGEN+LIMPIA+PISO → 2, 4 (R0 0.85) · +PEN_OTRO 0.35 → 3, 5 (R0 0.90). A1 ✔ ("MARGEN solo" cae a 0/18 sin la limpieza regalada), A4 ✘ a medias (el conjunto
sin HUECO da 6/18 y 8/18, no ≥ 8 en la primera; con fl 0 HUECO sí cuenta: 8/18 → fab 13/18). Lectura: **desde el apagado del genetista hay VALLE de 2+ con las
dos reglas de fundador**; la única pendiente de un gen es MARGEN con el resto de O1 puesto.
**Humo de la cadena (`--humo_cadena`, T 20 000, 1 pasaje sel, s 883990):** desde MARGEN 0.0 la cadena NO se extingue pero NO MUTA: 18 fundadores (9 base + 9 cámara al
principio), **15 partos en 9 linajes, R0 0.0, vida 20 000, profundidad 1, MARGEN de los vivos 0.0** — con consigna EN U el cuerpo sólo come bajo U, nunca llega a la
ventana de parto, no muere y no pare: el reloj mutacional no corre. **Decisión 2 (antes de la serie): `ARRANQUE_MARGEN = 0.03`.** Desde 0.03: 72 fundadores (63 de
cámara), 73 partos, R0 0.2, vida 5 717, profundidad 2 en 20k (≈ 700 eventos por 100k): el reloj corre. El brazo `off` de la serie = BASE (MARGEN 0.03, resto O1) =
el piso medido 0/4 (fl 1) y 0/4 (fl 0). Nulo con arranque 0.03: mediana neutra 0.010, P(sel > neu + 0.03) 0.06 → P(≥ 13/20) ≈ 1e-11 (`nulo_margen_salida.txt`).
**Humo de la serie (`--humo_serie` + `--reanuda`, 16:54–16:57, 8 corridas en dos procesos, 60 000 pasos, 0 abortos):** main de punta a punta: cadenas sel y neu (2 × 2
pasajes de 5k), pruebas sel, neu, fab, off (20k), JSON por pasaje y por trabajo, `--reanuda` saltó lo hecho, la letra se evaluó y dio NO SE LEE (V2 y V7 fallan a T
corto, como corresponde a un humo). Nota: ese humo corrió aún con arranque 0.0 (genoma final MARGEN 0.0 en 5k): sólo prueba la tubería.
**Arnés final:** `identidad_muro_perillas_salida5.txt` → **ARNES PASA, 40/40** (antes de fijar el arranque); con `SHAS_PROPIOS` fijados y arranque 0.03 →
`identidad_muro_perillas_salida6.txt` (línea final en el informe del PASO B).

## 12. AUDITORÍA PREVIA (5-oct, 17:25–17:50): cambios ANTES del commit y de la serie. Esta sección MANDA sobre las secs. 10–11 bis donde se contradigan.
**Diseño (punto 3): en la serie SOLO MUTA MARGEN** (`PS_MUTA = (0,)`, parámetro del carro que fija el runner y queda en el estado de cada corrida; V4 lo exige);
PRUEBA, PEN_OTRO, PISO, LIMPIA y HUECO quedan fijos en fábrica en sel y en neu. Todo el reloj cae en el gen de la letra (profundidad efectiva = profundidad) y PC
no mezcla otros genes. La variante "mutan los seis" (`PS_MUTA = (0,1,2,3,4,5)`) queda como posible serie descriptiva; no hay razón fuerte para dejarla.
**Nulo rehecho con p = 1** (`nulo_margen.py` → `nulo_margen_salida.txt`; arranque 0.03, σ 0.03, δ 0.01, clip [0, 0.6]):
| nulo | mediana por linaje (≥ 30 eventos) | mediana de siembra neutra (45 muestras) | P(> 0.03) | P(≥ 0.06) | PG (a) P(sel > neu + 0.03)/cadena → P(≥ 13/20) |
|---|---|---|---|---|---|
| deriva pura, p = 1 (el neutro de la serie) | 0.012 | 0.012 | 0.108 | 0.004 | 0.037 → 1.8e-14 |
| deriva pura, p = 1/6 (versión del mediodía) | 0.011 | 0.010 | 0.124 | 0.008 | 0.065 → 1.7e-11 |
| **ERR-192: purificadora sin gradiente** (sel: 9 linajes en cámara, muerte si MARGEN < 0.015, refundación copiando a otro; ninguna ventaja por encima) | — | **0.096** | 0.995 | **0.886** | (a) 0.955 → **1.000**; (b) P(sel ≥ 0.06)/cadena 0.886 → **P(≥ 13/20) ≈ 1.0** |
| idem, barrera 0.005 / 0.03 | — | 0.086 / 0.113 | 0.99 / 1.00 | 0.79 / 0.97 | (b) → 0.95 / 1.00 |
Los umbrales **MARGEN_G = 0.03** (deriva pura: 0.037 por cadena → 1.8e-14) y **FUNC = 0.06** (deriva pura: 0.004 por cadena) siguen siendo correctos contra la
DERIVA; contra la selección purificadora con cámara NO lo son (ERR-192, abajo). Con p = 1 el neutro cae igual de rápido (la estacionaria se alcanza en ~30 eventos)
y sel tiene 6 veces más reloj sobre el gen.
**ERR-192 (candidato, redactado): "nulo de deriva sin selección purificadora".** El nulo de deriva pura (PS_LEE 0) no es el nulo de "no hay gradiente": en sel el
gen SE LEE y MARGEN cerca de 0 es inviable, así que la mera supervivencia (barrera letal) más la cámara (la refundación copia a un linaje vivo) empuja el gen hacia
arriba sin que un MARGEN mayor sea mejor en nada. Simulado (`nulo_margen.py` (4)): con barrera en 0.015 y sin ventaja por encima, la mediana de sel llega a 0.096
y supera 0.06 en el 89 % de las cadenas (79–97 % con barrera 0.005–0.03): **la puerta (b) ≥ 0.06 es un falso positivo casi seguro bajo "barrera + cámara"**, y (a)
lo es siempre. Reserva del modelo: supone que un linaje bajo la barrera MUERE y es refundado; el humo (`--humo_cadena` desde 0.0) mostró que en esta pista
MARGEN 0 NO muere: se congela (vida 20 000, R0 0, sin refundaciones) y aporta su 0 a la siembra, lo que frena el trinquete; la verdad está entre los dos modelos y
no se puede fijar sin un control empírico. **Consecuencia para la letra:** PG (a ∧ b) y PC prueban que la selección por viabilidad/persistencia lleva el margen a la
zona funcional y que el genoma cruza más que el de la deriva; NO prueban que un margen mayor sea VENTAJOSO frente a uno menor por encima de la barrera. **Control que
separaría barrera de ventaja (propuesto, NO en la serie de esta noche):** brazo `pur` = sel con el gen leído por el cuerpo recortado a un TOPE (`MARGEN leído =
min(g, 0.045)`: la barrera sigue, la ventaja por encima de 0.045 desaparece); si en `pur` el gen también llega a ≥ 0.06 en ≥ 13/20, lo que sube es el trinquete
barrera + cámara. Costo: una cadena más por índice (+50 % de CPU); hook de una línea en `_ps_pon` (`PS_TOPE`), no construido para no invalidar el arnés de hoy.
**LA LETRA v2 (`corre_muro_perillas.lee_serie`; 10 casos sintéticos en el arnés (F)).** Validez (una falla → NO SE LEE): V1 completa y coherente · V2 fab > off en
≥ 16/20 · V4 estado por worker (carro, PERILLAS 1, `fl` 1, `muta` = [0], σ/δ/cámara/PS_LEE por brazo; prueba con un solo genoma = el del brazo) · V5 desde el
arranque · **V7a profundidad mutacional ≥ 30 y V7b refundaciones por cámara ≥ 3 000, cada una en ≥ 16/20, sobre el NEUTRO Y sobre SEL** (B-2; si sel no llega es
NO SE LEE, no NO). Se reporta la profundidad EFECTIVA sobre MARGEN (= profundidad, porque sólo MARGEN muta). Puertas (empates en contra): **PG = (a) MARGEN
mediano de la siembra final de sel > neu + 0.03 en ≥ 13/20 ∧ (b) MARGEN final de sel ≥ 0.06 en ≥ 13/20** · **PC** sel > neu pareado ≥ 13/20 ∧ suma ≥ +10.
| desenlace | condición | frase (máxima) | réplica |
|---|---|---|---|
| FUNCIONA | PG (a ∧ b) y PC | "en la pista vieja, la selección por persistencia lleva desde 0.03 el margen de la boca de O1 a la zona funcional y el genoma que deja cruza más que el de la deriva" (sin "ventaja": ERR-192) | sí |
| HAY ALGO MODESTO | (a ∧ b) sin PC | "el gen llega a la zona funcional pero no cruza más que la deriva" | sí |
| HAY ALGO MODESTO | PC sin (a) | "cruza más que la deriva sin que el gen suba por la letra" | sí |
| **CONSERVA, NO SUBE** | (a) sin (b) (con o sin PC; se dice) | "la selección impide que el margen caiga a 0; no lo sube" | **sólo si (b) queda a ±1 de 13** |
| NO | ni (a) ni PC | "con reloj medido, la selección no subió el margen desde 0.03" | sólo en el umbral |
| NO SE LEE | validez | — | no (semillas y preregistro nuevos) |
EN EL UMBRAL = cualquier conteo (a, b, PC-par) a ±1 de 13 o la suma a ±1 de 10. Bloque serie + réplica: si coinciden vale ése, si no el menor (orden NO SE LEE <
NO < CONSERVA < MODESTO < FUNCIONA). **Nunca** "la selección cruzó el muro" salvo mayoría (≥ 5/9) en ≥ 16/20 pruebas de sel como O1 (`sel_mayoria_como_O1`), y aun
así "O1 con una perilla libre, no el tronco".
**Descriptivos obligatorios junto al veredicto (punto 5):** `UNA_EVIDENCIA` (PG y PC son UNA evidencia: neu ≈ 0.01 no pare); cadenas sel con LIMPIA ≤ 0.5 (con sólo
MARGEN mutando debe ser 0) y pruebas sel con B+D ≤ 5 (cruzar sin morder nada malo = limpieza regalada, ERR-191: esas cadenas quedan sujetas a la regalía);
sel vs fab y sel vs off, neu vs off (pareados); mayorías por brazo; MARGEN final por cadena; relojes por brazo con la profundidad efectiva.
**Sesgo declarado (B-3):** el arranque 0.03, el margen de PG (0.05 → 0.03), la zona funcional 0.06, `FL_SERIE = 1`, "sólo MARGEN muta" y la puerta (b) se fijaron
DESPUÉS de ver el mapa de dos semillas (1-oct), el PASO A y los humos del 5-oct, y ANTES de cualquier corrida de la serie. La línea de la Parte I sec. 6 que decía
"PG margen 0.05" queda ANULADA por esta sección. Nada de la serie se ha corrido.
**Predicciones firmadas v2 (17:45; sustituyen a las de la sec. 10; cambios: B3 se parte en a/b por la puerta nueva; B4/B5 suben porque con p = 1 todo el reloj
cae en MARGEN y por el trinquete de ERR-192; B9 desaparece (los otros genes ya no mutan); B10 igual):**
| # | predicción | rango | p |
|---|---|---|---|
| B1 | fab suma de linajes que cruzan; off (= BASE 0.03) | [100, 150]; [15, 60] | 0.75 |
| B2 | V2 pasa (fab > off en ≥ 16/20) | | 0.85 |
| B3a | (a) MARGEN sel > neu + 0.03 en ≥ 13/20 | esperado 16–20/20 | 0.80 |
| B3b | (b) MARGEN final de sel ≥ 0.06 en ≥ 13/20 | esperado 12–18/20 | 0.55 |
| B4 | MARGEN mediano final: sel; neu | [0.05, 0.14]; ≤ 0.02 | 0.60 |
| B6 | suma de cruzan: sel; neu | [70, 130]; [10, 50] | 0.55 |
| B7 | PC pasa (par ≥ 13/20 y +10) | | 0.60 |
| B8 | sel NO alcanza mayoría como O1 (< 16/20); fab sí (≥ 16/20) | | 0.70; 0.70 |
| B10 | relojes del neutro: profundidad mediana [40, 90]; refundaciones [3 500, 5 500]; los de sel dentro de ±30 % | | 0.55 |
| B11 | V7a y V7b pasan en neu y en sel | | 0.75; 0.85 |
| B12 | cadenas sel con B+D ≤ 5 en la prueba: 0 (sólo MARGEN muta, LIMPIA queda en 1) | | 0.90 |
| V | SERIE: FUNCIONA / CONSERVA / MODESTO / NO / NO SE LEE | | 0.35 / 0.20 / 0.15 / 0.10 / 0.20 |
**Costo con sólo MARGEN mutando:** el mismo por corrida (la mutación no cuesta): ≈ 156 s × 14 corridas × 20 índices ≈ 44 000 s de CPU ≈ **6 h con pool 2**.

## 13. TRES BRAZOS: el control de GRADIENTE `pur` (5-oct, 18:00–18:30; tras el nulo de ERR-192, antes de cualquier dato de serie). MANDA sobre las secs. 10–12.
**Por qué:** el nulo de ERR-192 (sec. 12) mostró que un trinquete sin gradiente (barrera letal + cámara) da la puerta (b) con probabilidad ≈ 1: la serie de dos brazos
tenía el FUNCIONA casi garantizado y no informaba. **Diseño (tres cadenas pareadas por índice, mismas semillas, misma mutación, misma cámara):**
- `sel`: el cuerpo lee el gen (MARGEN libre).
- `neu`: `PS_LEE 0` (deriva pura; el cuerpo decide con fábrica).
- **`pur`**: idéntico a sel pero el cuerpo lee `min(MARGEN, TOPE_PUR = 0.045)` (`PS_TOPE`, parámetro del carro, fijado por el runner y registrado en el estado): la
  selección purificadora (MARGEN ≈ 0 inviable) y el trinquete actúan igual que en sel, pero subir por encima de 0.045 NO da ninguna ventaja; el gen heredado muta y
  viaja libre por encima del tope (se reporta el gen, no el valor leído). **Tope 0.045:** por encima del arranque (0.03 → 4/18 cruzan, R0 0.86) y por debajo de la zona
  que cruza (0.06 → 11–15/18, R0 0.88–0.91); punto medio del escalón de la rampa (sec. 8/11).
- Pruebas monomórficas T 100k, todas leídas SIN tope: sel, neu, **pur (¿cruza su gen heredado?: descriptivo)**, fab = O1, off = BASE (0.03).
- Identidad (arnés): pur con tope ≥ clip == sel bit a bit; genes de fábrica con tope 0 == O1 con MARGEN 0 escrito a mano; `genoma_ok` en toda prueba (leído == pedido).
**Nulo de gradiente** (`nulo_margen.py` (5), `nulo_margen_salida.txt`): sin gradiente, sel y pur son intercambiables (dos cadenas purificadoras independientes, barrera
0.015, p = 1): P(sel > pur + m) por cadena = 0.502 (m 0) · 0.423 (0.01) · **0.349 (0.02) → P(≥ 13/20) = 0.006** · 0.288 (0.03) → 0.0008; |sel − pur| mediana 0.037,
P90 0.099. **`MARGEN_GR = 0.02`** (falso positivo 0.6 % con empates en contra; la moneda pareada sin margen daría 13.5 %).
**LA LETRA v3 (`lee_serie`; 12 casos sintéticos en el arnés (F)).** Validez: V1 · V2 (fab > off ≥ 16/20) · V4 (estado por worker: `fl` 1, `muta` [0], `tope` None/None/0.045
en sel/neu/pur y None en toda prueba) · V5 · **V7a (profundidad ≥ 30) y V7b (refundaciones ≥ 3 000) en ≥ 16/20 sobre neu, sel Y pur**. Puertas (empates en contra, ≥ 13/20):
**PG** = (a) MARGEN sel > neu + 0.03 ∧ (b) MARGEN final de sel ≥ 0.06 · **PC** = sel > neu pareado ∧ suma +10 · **GR** = MARGEN final de sel > pur + 0.02 pareado.
| desenlace | condición | frase (máxima) | réplica |
|---|---|---|---|
| **FUNCIONA** | PG ∧ PC ∧ GR | "en la pista vieja, la selección sube desde 0.03 el margen de la boca de O1 porque un margen mayor persiste más (sel > pur), y el genoma que deja cruza más que el de la deriva" | sí |
| **TRINQUETE** | PG ∧ ¬GR (con o sin PC; se dice) | "la selección purificadora y la deriva llevan el margen a la zona funcional; no hay evidencia de gradiente" | sólo si GR a ±1 |

**TRINQUETE no prueba ausencia de gradiente:** con n = 20, un gradiente real menor que ~0.03–0.05 de margen queda bajo el P90 de |sel − pur| (0.099) y da TRINQUETE; la potencia de GR no está calculada (H-3, auditor corto). La réplica desde TRINQUETE sólo se dispara con GR a ±1 de 13 (`trinquete_gr_umbral`, en la regla de parada del runner; H-1). Descriptivo H-4: GR estratificado por la razón de profundidad sel/pur (n de cadenas con razón dentro de ±30 % y GR sólo en ellas), sin tocar la letra.

| HAY ALGO MODESTO | PG ∧ GR sin PC | "el gen sube con gradiente pero no cruza más que la deriva" | sí |
| HAY ALGO MODESTO | PC sin (a) | "cruza más que la deriva sin que el gen suba por la letra" | sí |
| CONSERVA, NO SUBE | (a) sin (b) | "la selección impide que el margen caiga a 0; no lo sube" | sólo si (b) a ±1 |
| NO | ni (a) ni PC | "con reloj medido, la selección no subió el margen desde 0.03" | sólo en el umbral |
| NO SE LEE | validez | — | no |
EN EL UMBRAL = cualquier conteo (a, b, PC-par, GR) a ±1 de 13 o la suma a ±1 de 10. Bloque: si serie y réplica coinciden vale ése, si no el menor (NO SE LEE < NO <
CONSERVA < TRINQUETE < MODESTO < FUNCIONA). Nunca "cruzó el muro" salvo `sel_mayoria_como_O1` (≥ 16/20), y aun así "O1 con una perilla libre".
**Descriptivos obligatorios:** los de la sec. 12 más `gradiente_sel_vs_pur` (pareado, medianas, por cadena), `pur_prueba_sin_tope` (cruzan, mayorías, R0 del gen heredado
de pur leído sin tope), pareados sel/pur y pur/neu, relojes de los tres brazos con profundidad efectiva.
**Sesgo declarado:** el brazo `pur`, su tope 0.045, la puerta GR y su margen 0.02 se fijaron el 5-oct tras el nulo de ERR-192 (sec. 12) y antes de cualquier dato de serie;
el humo de la serie con pool 3 (abajo) es el único dato del montaje de tres brazos y es a T corto (no cuenta).
**Costo:** tres cadenas + cinco pruebas por índice = (15 pasajes + 5 pruebas) × ~156 s ≈ 3 120 s por índice; serie ≈ 62 500 s de CPU → **≈ 5.8 h con pool 3** (≈ 8.7 h con
pool 2); réplica igual. `POOL_MAX = 3` (un trabajador por brazo en cada cadena; la cola reparte las pruebas al terminar cada cadena).
**Predicciones firmadas v3 (sustituyen a las v2; lo que cambia: V se reparte entre FUNCIONA y TRINQUETE; B13–B15 nuevas; el resto igual):**
| # | predicción | rango | p |
|---|---|---|---|
| B1 | fab suma; off | [100, 150]; [15, 60] | 0.75 |
| B2 | V2 | | 0.85 |
| B3a | (a) sel > neu + 0.03 | 16–20/20 | 0.80 |
| B3b | (b) sel ≥ 0.06 | 12–18/20 | 0.55 |
| B4 | MARGEN final mediano: sel; neu | [0.05, 0.14]; ≤ 0.02 | 0.60 |
| B6 | cruzan: sel; neu | [70, 130]; [10, 50] | 0.55 |
| B7 | PC | | 0.60 |
| B8 | sel sin mayoría como O1; fab con ella | | 0.70; 0.70 |
| B10 | relojes neutros: prof [40, 90], refund [3 500, 5 500]; sel y pur dentro de ±30 % | | 0.55 |
| B11 | V7a y V7b en los tres brazos | | 0.70; 0.85 |
| B12 | cadenas sel con B+D ≤ 5 en la prueba: 0 | | 0.90 |
| **B13** | MARGEN final mediano de pur | [0.04, 0.10] (el trinquete lo sube aunque leer más no sirva) | 0.60 |
| **B14** | GR: sel > pur + 0.02 en ≥ 13/20 | esperado 8–14/20 | **0.40** |
| **B15** | pur (gen leído sin tope en la prueba) cruza menos que sel pero más que neu: sel > pur > neu en suma | | 0.50 |
| V | SERIE: **FUNCIONA 0.22 / TRINQUETE 0.30** / CONSERVA 0.13 / MODESTO 0.10 / NO 0.05 / NO SE LEE 0.20 | | |
Predicción honesta: con la rampa saturando en 0.06–0.10 y el tope en 0.045, la ventaja real de sel sobre pur es pequeña (entre 0.045 y ~0.08 de margen leído: de ~R0
0.87 a ~0.91) frente a un trinquete que mueve ±0.04 por cadena: GR es la puerta más dura de la serie; por eso FUNCIONA 0.22 y TRINQUETE 0.30.
