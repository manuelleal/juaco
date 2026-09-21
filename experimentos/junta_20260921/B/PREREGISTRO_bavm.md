# PREREGISTRO — **BA-vm** (fase 5): *la variante vota con su PEOR casilla, no con la suma*

**Estado:** escrito el 21-sep-2026 por el creador B de la junta, **antes** de construir el instrumento y **antes** de cualquier corrida de serie.
El detalle completo (hipótesis, mecanismo en código, predicción con rangos, refutadores, trampas y ERR evitados) está en
`experimentos/junta_20260921/B/PROPUESTA.md` §3–§4 y **no se repite aquí**: esta página es lo que el coordinador necesita para construir el runner.
Cualquier cambio posterior va en ERR numerado, con fecha, motivo y semillas nuevas.

## 1. Criterio — SIN TOCAR UNA LETRA
Las **puertas ABSOLUTAS P0–P7 y la MISIÓN** de `experimentos/nivel05_familia_variante_BAv/PREREGISTRO_bav.md` §3 (ERR-90), copiadas tal cual:
`N ≥ 18` · `CANAL ≥ 15` · `CORTADO ≤ 5` · `BAR-T ≤ 5` · `VALOR ≤ 5` · `BAR-H ≤ 10` · `dist(PAR) ≥ 15` **y** `dist(PAR0) ≤ 5` ·
`R6: muertes ≤ 1.5 × muertes(b4b)` **y** `okU ≥ okU(b4b) − 0.10` · **MISIÓN: `BAR-T ≤ 5` Y `dist(PAR) ≥ 15`**.
**Se declara candidato sólo si pasa P0–P7 y la MISIÓN en LAS DOS series.** Una puerta caída en cualquiera cierra la línea.
**Ninguna puerta se normaliza por `CORTADO`** y **nada se rejuzga hacia atrás** (regla 3).

## 2. Mecanismo · memoria nueva CERO
Una perilla `dentro` con tres valores y **una línea** dentro de `_suma_tipo`:
`'suma'` = `organismo_familias_bav` bit a bit · `'minv'` = mínimo **escalado por el nº de casillas conocidas**, sólo en el tipo VARIANTE
(**el candidato**) · `'min'` = el mínimo escalado en los **dos** tipos (**la ablación preregistrada**; si pasa `min` y no `minv`, el resultado es
`min`). `dentro != 'suma'` **EXIGE `dos_tipos=1`** y **LANZA** en cualquier otro caso o si el valor no es uno de los tres.
No se toca: emisor, canal, mundo, **escritura**, `_dir_var`, `_bin4`, `_topk_tipo`, `_MGv` y su desempate, `_MEv`, vía rápida, puerta, boca,
metabolismo ni el consumo del rng.

## 3. Instrumento, anclas y arnés (antes de medir nada)
- `construye_familias_bavm.py` por anclas sobre `organismo_familias_bav.py` (**`2dca0a3e239481f0`**; aborta si cambia), con tripwire de
  `organismo_familias_ba` `1f196ee786b2040d`, `a1` `8833e1dcfb62f26d`, `b6` `b10cbd4ddd0c32a3`, `b5` `e0b6b90f6f92d5c1`,
  `b4b` `b3dd1d7e66a2d147`, `organismo_v14` `feefc88b1fd8d434`. Postcondiciones: escritura intacta · `_dir_var`/`_bin4` intactos ·
  `_topk_tipo` intacto · `rng.` con el mismo recuento · la línea nueva exactamente **una** vez.
- `identidad_familias_bavm.py`: **apagado ≡ `bav` BIT A BIT** en las 6 configuraciones de lectura (incluida `conj_tipo=2`), 8 mundos × (k, sufijo),
  canal en sus tres modos, ancla larga a T = 120 000 sin consumir rng; cadena ≡ `ba` ≡ `a1` ≡ `b6` ≡ `b5` ≡ `b4b` ≡ **`organismo_v14`**;
  la regla nueva **reimplementada FUERA** coincide con `W_tabla` en los 32 estímulos; **perillas mal escritas que LANZAN (≥ 8)**; y
  **CONTROLES QUE DEBEN DIFERIR (ERR-88, ≥ 2 de 3 semillas): `BA-vm ≠ BA-v`, `BA-vM ≠ BA-v`, `BA-vm ≠ BA-vM`, `BA-vm-sh ≠ BA-vm`.**
  *Si alguno de los tres primeros NO difiere, la perilla está desconectada y la serie NO se corre.*
- `corre_familias_bavm.py`: **regla 14** (entrada campo a campo contra el bloque 6, 33 campos) · **ERR-54** (crudo antes de analizar) ·
  **ERR-89** (`b4b` obligatoria) · P-I2/P-I3/P-I4/P-I5 por brazo · imprime P0–P7 + MISIÓN por celda · `--humo` que **escribe su JSON**
  en `datos/humo/` · `--pool N` manda sobre `JUACO_POOL` (ERR-86).
- **Diagnóstico nuevo** (no decide ninguna predicción, no toca estado ni rng): `canal_lee_herm` = qué lee la tabla **para la HERMANA** en el paso
  exacto de la entrega, `[valor, habla, exactas FORMA, exactas VARIANTE]`. Es lo único que hoy no se pudo verificar (PROPUESTA §5).

## 4. Celdas, brazos y semillas
- **Celdas (8):** `b4b` (base de R6, obligatoria) · `b5k3` · `b6suf` (instrumento; deben reproducir sus números dentro de ±4 o no se lee nada) ·
  `A1` · `BA-v` (la fila de hoy, el pareado que da el contraste) · **`BA-vm`** (candidato) · `BA-vM` (ablación) · `BA-vm-sh` (memoria barajada).
- **Brazos (7), dirección (−) sola (ERR-53):** `CANAL`, `CORTADO`, `BAR-H`, `BAR-T`, `VALOR`, `PAR`, `PAR0`. Todo por **conducta de la boca** (ERR-44).
- **Emisor:** el del bloque 6 **sin tocar** (b4b bit a bit). Se mide la **lectura**, no el habla.
- **Semillas NUEVAS: serie `1541–1560`, réplica `1561–1580`** (verificadas libres con grep; única vecindad ocupada: 1501–1540 de la fase 9).
  **Humo: `918–920`** (901–903 la junta, 912 el humo de BA-v, 913–915 la mini-prueba de hoy, 916–917 el bloque del alias de `creacion_B`).
  El runner **rechaza** cualquier semilla de 821–1000 y de 1501–1540.
- **T = 100 000.** Coste por serie: 20 emisores + 8 celdas × 7 brazos × ~19 semillas ≈ **1 084** corridas (≈ 35–45 min con Pool 6).
  Si hay que recortar, el orden de sacrificio declarado **ahora** es: primero `BA-vM`, después `A1`. `b4b`, `b5k3`, `b6suf`, `BA-v`,
  `BA-vm` y `BA-vm-sh` **no se pueden quitar**.

## 5. Comando de la confirmación (lo corre el coordinador)
```bat
cd C:\Users\User\Documents\PROYECTOS\JUACO\bundle
python -u experimentos/junta_20260921/B/construye_familias_bavm.py
python -u experimentos/junta_20260921/B/identidad_familias_bavm.py
python -u experimentos/junta_20260921/B/corre_familias_bavm.py --humo --semillas 918,919,920
python -u experimentos/junta_20260921/B/corre_familias_bavm.py --serie --desde 1541 --pool 6
python -u experimentos/junta_20260921/B/corre_familias_bavm.py --serie --desde 1561 --pool 6
```
La serie **se para sola** antes de gastar una corrida si un sha de origen cambió, si la entrada difiere del bloque 6 en algo que no sea una
perilla de celda, o si algún control que DEBE diferir no difiere.

## 6. Probabilidad firmada
`P(candidato declarado) = 18 %`. La puerta que más probablemente lo mata es **R6** (35 % de pasarla en las dos series): `BA-v` ya va a 1.46× y
1.50× contra `b4b`, y esta regla hace la tabla **más pesimista**. Si R6 cae, la frase que queda registrada es:
**«la referencia exacta a familia Y variante está medida (1 de 32, hermana fuera en 37/37) y la paga en comida»** — y la fase 5 se cierra en 75 %
con un canje nombrado, no con una ausencia.
