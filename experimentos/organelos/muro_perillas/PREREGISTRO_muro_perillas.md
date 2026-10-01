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
linajes sin refundación en la segunda mitad, V7a profundidad neutra ≥ 30 y V7b refundaciones ≥ 3 000 en ≥ 16/20, PG margen 0.05 en ≥ 13/20, PC ≥ 13/20 y +10).
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
