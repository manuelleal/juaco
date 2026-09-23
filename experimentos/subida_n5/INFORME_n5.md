# INFORME n5: subida del nivel 5 con V-5 (23-sep-2026, creador del equipo n5). Una página.

**Veredicto del paquete: LISTO PARA SERIE. Del mecanismo: HAY ALGO MODESTO con n = 1 (no es evidencia).**

## Qué hice
- **Elegí la pieza (a) de la brecha, "familia Y variante con la misma tabla"**, porque es la única con causa
  medida, instrumento con identidad y criterio ya usado (ERR-90). N2, lo propio del receptor y XOR entre dos
  mueven más puntos pero hoy no tienen mundo decidible (teorema de C, 18-sep). **Techo honesto: +5 (75 → 80 %).**
- **Verifiqué el dato del explorador sobre los crudos de BA-v**: en las 15 semillas en que cae dist(PAR), el
  receptor **muerde a la hermana** (okP = 0 en 15/15). La causa, leída en el código: el mensaje y el primer
  bocado de T1v2 **sobrescriben con +1** las casillas que comparte con la hermana (las 36 de forma y una de
  variante); la familia T1 (veneno, −3) se borra.
- **Construí V-5** (B-5 trasplantado a la tabla, propuesta de C nunca corrida): una escritura que contradice en
  signo a la casilla de la familia **la parte** en una subcasilla de variante en vez de sobrescribirla. Memoria
  nueva **declarada** (66 × 32 subcasillas, pobladas sólo por conflicto). Por anclas (`construye_v5.py`, 11
  anclas + postcondiciones) desde `organismo_familias_bav.py` (`2dca0a3e239481f0`) y el runner desde
  `corre_familias_bav.py` (`4453754a9921e349`).
- **Identidad 33/33** (`identidad_v5_salida.txt`): con `v5 = 0` ≡ BA-v bit a bit (17 casos), ≡ TRONCO v14 y ≡ v15f_on.
- **Preregistro** `PREREGISTRO_n5.md` §0–§8 antes del humo; semillas nuevas 25701–25740 (+25741–25760 sólo por §7), humo 25791.
- **Humo** (1 proceso, 6 corridas, 72 s): `datos/humo/humo_v5_20260923_155242.json`. Regla 14: 33 campos idénticos.
  En la **misma semilla**, BA-v presta +3.0 a la hermana y la muerde (dist 0); **BA-v5 la deja en −9.0 y no la
  muerde (dist 1)**, come el referente (+3.0), no come en BAR-T (−9.0) y la memoria barajada no come (−5.0).

## Qué falló (declarado por mí)
- **Mi arnés, primer intento 31/33:** comparaba el eco de la perilla `v5`. Corregido en una línea y repetido entero.
- **Predicción de mecanismo que no hice:** V-5 parte casillas sobre todo por la **experiencia propia** (295–405
  partos por bocado, ~340–424 subcasillas), no sólo por el mensaje.
- **Riesgo de coste mayor que el firmado:** en el humo BA-v5 muere 81–96 contra 34 de BA-v y come menos
  (3 287–4 056 contra 5 616 bocados de comida; corregido por el coordinador el 23-sep: BAR-T 3 287 quedaba fuera del rango citado). Mis predicciones **K4 (1.0×, 0.7–1.5×)** y **P7 (1.2×, 0.8–2.0×)**
  quedan en riesgo alto (2.4× aquí, n = 1). No recalibré nada (§9.3 escrito antes de la serie).
- Toqué sin querer `MANIFEST.txt` al correr `python manifiesto.py` (lo regenera) y lo restauré con
  `git checkout -- MANIFEST.txt`. **Al cierre aparece otra vez modificado y no fui yo** (no volví a correrlo):
  que lo mire el coordinador antes de commitear.

## Qué queda (para el coordinador)
```
cd C:\Users\User\Documents\PROYECTOS\JUACO\bundle
python -u experimentos/subida_n5/corre_v5.py --serie --desde 25701 --pool 6
python -u experimentos/subida_n5/corre_v5.py --serie --desde 25721 --pool 6
```
(tercera `--desde 25741` **sólo** si §7 la pide). Celdas: b4b, b6suf, BA-v, **BA-v5**, BA-v5-sh, b5k3-v5; 7 brazos.
**Coste:** unas 860 corridas de 100 000 pasos por serie (20 emisores + 6 × 7 × ≤ 20) a 9–12 s → **~2.5–2.9 CPU-h por
serie, ~27–35 min de pared con Pool 6**. Hay que esperar a que se libere uno de los dos Pools en marcha (tope: 2 Pools).
**Puntos (propuesta):** FUNCIONA → 80 %; ALGO MODESTO → 75 % (+0); NO → 75 % y la línea V-5 se cierra.
**Lo que este bloque no toca:** N2, que el receptor aprenda algo propio, XOR entre dos: el 20 % restante.
