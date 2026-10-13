# SELECCIÓN de bloques para la siembra (13-oct-2026)

Escrita ANTES de sembrar. Manda `../PREREGISTRO.md` (§ Diseño, "Bloques").

## Criterio
1. Filas de la tabla de `experimentos/INDICE.md` (73 filas, foto al 23-sep).
2. Se descarta la fila si su **estado** contiene `borrador`, `preparado`, `en curso`, `exploratorio`, `sin cerrar` o
   `instrumento listo`, o si su **veredicto registrado** contiene `sin registro`, `sin dato`, `sin PASA/CAE`,
   `no es dato` o `preparado, sin serie` (no hay veredicto registrado).
3. Se descarta si la carpeta no contiene (en cualquier subcarpeta) al menos un `PREREGISTRO*.md` y un `corre_*.py`.
4. Quedan **50 candidatas**. Se barajan con `random.Random(20261013).shuffle(lista)` sobre la lista en el orden de la
   tabla del INDICE.
5. Se abren en ese orden. Se acepta la carpeta si, al abrirla, el JSON de resultados de la serie que respalda el
   veredicto está en un directorio `datos/` (el `datos/` del repo, donde escriben los runners de esa época, o un
   `datos/` dentro de la carpeta). Si no, se pasa a la siguiente y se anota.
6. Carpetas con varios experimentos: se toma el **primer `PREREGISTRO*.md` en orden alfabético** que tenga su
   `corre_*.py` y su JSON en `datos/`. La copia contiene sólo ese experimento.

Código usado (fuera del repo, junto a la clave): lee el INDICE, aplica 2–3 y baraja con la semilla.

## Orden barajado (las 50 candidatas)
1 etapa2_politica · 2 v9_reverificacion · 3 bug01 · 4 nivel7_hija_dispersa · 5 capacidad_grande · 6 nivel8_curiosidad ·
7 nivel13_alma · 8 criterio_v4 · 9 etapa4_v9 · 10 v10_direccion_division · 11 nivel05_familia_variante_BAv ·
12 v12_ceguera_graduada · 13 mundo_anclado · 14 junta_fase5 · 15 creacion_C · 16 nivel4_puerta_codigo ·
17 nivel09_cuerpo_nuevo · 18 v11_evo_division · 19 nivel6_mapa · 20 v11_generaliza · 21 creacion_A · 22 nivel7_3T_k ·
23 3T_confirmatorio · 24 nivel10_composicion_v14 · 25 nivel09_cuerpo_nuevo_b2 · 26 nivel7_xor_lectura ·
27 nivel8_metaplasticidad · 28 nivel9_probar_si_mismo · 29 nivel8_mundo_largo · 30 nivel11_mundo_vivo · 31 nivel6_rodeo ·
32 nivel07_fanin_expansion · 33 junta_20260921 · 34 creacion_B · 35 ramas · 36 etapa3_v9 · 37 etapa5_comunicacion ·
38 v9_memoria_rechazo · 39 aprende_barrer · 40 criterio_v3 · 41 tronco_v15_dE5 · 42 v13_reverificacion ·
43 nivel3_asociacion · 44 nivel8_escala_mapa · 45 nivel6_2d · 46 nivel06_rodeo_obligado · 47 nivel12_mundo_familias ·
48 v13_dos_vias · 49 nivel8_novedad_sitio · 50 carrera_escuderias

## Descartadas al abrirlas
- **7 `nivel13_alma`**: los JSON de la serie (`alma_<brazo>_s<semilla>_*.json`) están en la raíz de la carpeta, no en
  un `datos/`. No cumple el punto 5.
- **11 `nivel05_familia_variante_BAv`**: los crudos de las tres series (`serie_bav_*_crudo.json`) están en la raíz de
  la carpeta; en `datos/humo/` sólo hay humos. No cumple el punto 5.

## Las 10 seleccionadas
| orden | carpeta | experimento copiado | JSON de resultados |
|---|---|---|---|
| 1 | `etapa2_politica` | `PREREGISTRO_frontera_hambre.md` | `datos/frontera_hambre_20260916_153342.json` |
| 2 | `v9_reverificacion` | `PREREGISTRO_reverificacion_v9.md` | `datos/reverificacion_v9_20260916_165658.json` |
| 3 | `bug01` | `PREREGISTRO.md` (experimento 1, decaimiento local) | `datos/bug01_decaimiento_20260915_130802.json` |
| 4 | `nivel7_hija_dispersa` | `PREREGISTRO_hija_dispersa.md` | `datos/hija_dispersa_s61-80_20260918_000202.json`, `datos/hija_dispersa_s81-100_20260918_000954.json` |
| 5 | `capacidad_grande` | `PREREGISTRO_capacidad_grande.md` | `datos/capacidad_grande_20260917_142455.json` |
| 6 | `nivel8_curiosidad` | `PREREGISTRO_curiosidad.md` | `datos/curiosidad_s41-60_20260917_211739.json` |
| 8 | `criterio_v4` | `PREREGISTRO_calibracion_v4.md` | `datos/critv4_20260922_132544.json`, `datos/critv4_rep_20260922_135746.json` (+ crudos) |
| 9 | `etapa4_v9` | `PREREGISTRO_etapa4_v9.md` | `datos/etapa4_v9_20260916_170519.json` |
| 10 | `v10_direccion_division` | `PREREGISTRO_v10.md` | `datos/v10_confirmatorio_20260916_175557.json` |
| 12 | `v12_ceguera_graduada` | `PREREGISTRO_v12.md` | `datos/v12_superficie_20260917_154123.json` |

## Qué lleva cada copia
El preregistro, el `corre_*.py`, los instrumentos de la carpeta que el runner importa (organismo/mundo generados y su
constructor; el arnés de identidad si existe), los JSON de resultados y sus `.log` (todos < 15 KB) dentro de `datos/`, y
`VEREDICTO.md` con la entrada del REGISTRO que declara el veredicto (copiada de `registro/REGISTRO_etapas_1_2.md`; las
líneas de origen van en su cabecera). En `criterio_v4` va también la letra `CRITERIO_TRONCO_v4.md`. No se copian los
módulos del tronco que viven en `organismo/` ni los de otras carpetas que el runner importa.

60 copias, 6 por bloque, nombradas `c01`…`c60` en orden barajado con `random.Random(20261013)`.
