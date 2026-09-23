# INFORME — subida del nivel 8, tanda 3: memoria lenta con repaso (creador, 23-sep-2026)

**Veredicto del humo: HAY ALGO MODESTO, por confirmar. No es dato de serie.** En la semilla del humo (15893), repasar las huellas
propias retiene más que el tronco: RET40 0.6875 contra 0.575. Lo hace por encima de los dos controles del mismo presupuesto
(baraj10 0.525, sinhue10 0.475), y la adquisición tardía de comida baja 0.04. **No llega a 0.75**: la predicción central del
encargo (P1) cae en el humo. La serie 15801 y la réplica 15821 no se corrieron (necesitan Pool). Manda `PREREGISTRO_n8c.md`
(`2570835d050077ae`).

## Qué hice
- **Diagnóstico** (s15890, un proceso). El olvido de lo ausente tiene tres vías:
  - (a) el código cambia y la puerta cae a la vía lenta, que dice «veneno»;
  - (b) interferencia en celdas compartidas;
  - (c) neofobia: la comida vieja se visita 284 veces y se muerde 11.

  El repaso ataca la (b) y deja la (a) fuera a propósito: no fabrica evidencia para la puerta.
- **Instrumento por anclas.** `construye_n8c.py` (`22db8bbd5ea88401`, 5 anclas) genera `organismo_repaso.py`
  (`1dce42830f4230bc`) desde `subida_n8/organismo_flujo.py` (`14afed5aa16e09bf`).
  - Órgano: tras cada mordida, `dosis` repasos. Cada repaso reconstruye un patrón desde la huella por celda (`mup/zp`, `mun/zn`)
    y le aplica un Rescorla-Wagner con la regla de la mordida.
  - Memoria nueva: **2 números** (la última R+ y la última R−). Constante nueva: `dosis`.
- **Runner** `corre_n8c.py` (`2314ed1e7f99c104`).
  - Tres modos excluyentes y `allow_abbrev=False`.
  - `--serie` sólo acepta 15801/15821, `--n 20` y `--pool`.
  - `--veredicto` imprime la letra en la última línea.
  - El mundo es `subida_n8/mundo_n8.py`, importado de solo lectura y con el sha verificado.

## Salida del arnés (`identidad_n8c.py` `823c94f6ee81bc58` → `identidad_n8c_salida.txt`, 18:35:37)
```
(0a-0d) origen, tronco v142, construido y mundo por sha OK · (A) x2 repaso=0 == organismo_flujo, 31 claves OK
(A1) x2 flujo retina 12, 40 estimulos, fotos, dosis 1 y 10 inerte con repaso=0 OK · (A2) x3 == organismo_v142 en W, muertes,
divisiones, celdas, mordidas, visitas OK · (A3) BASE s12601 T 200000 == JSON de la serie de subida_n8 (2d6e45e313ed0401) en 21
medidas, 0 distintas OK · (B1) x4 repasos = dosis x mordidas, + y - suman OK · (B2-B4) actua, brazos distintos, determinista OK
(B5) baraj conserva la proporcion de objetivos + (0.801 vs 0.799) OK · (F1-F4) no toca huellas/ncod/KW/via lenta/energia/rng,
no lee valencias, 4 lineas marcadas OK · (G) regla 14: 125 campos, 0 distintos · (H) 11 invocaciones malas abortan sin escribir
datos (rc 2,2,2,2,1,...) · (I1-I3) letra sobre sinteticos; --veredicto ultima linea = letra; rechaza humo
TOTAL 29/29 en 64.4s
RESULTADO: 29/29
```

## Humo final (s15893, UN proceso, 5 brazos, T = 200 000, 92 s; `datos/humo/n8c_humo_…_s15893_20260923_183736.json`, `8c9035517f3cf4a5`)
| brazo | RET40 (com / ven) | RET40_rel | ADQ40_com | ADQ_tarde (com / a priori) | muertes | repasos |
|---|---|---|---|---|---|---|
| base | 0.575 (0.30 / 0.85) | 0.28 | 0.90 | 0.66 (0.32 / 0.28) | 408 | 0 |
| rep1 | 0.675 (0.40 / 0.95) | 0.43 | 0.70 | 0.70 (0.40 / 0.28) | 341 | 1262 |
| **rep10** | **0.6875 (0.45 / 0.925)** | 0.58 | 0.60 | 0.62 (0.28 / 0.20) | 383 | 9890 |
| baraj10 | 0.525 (0.10 / 0.95) | 0.22 | 0.45 | 0.68 (0.36 / 0.32) | 383 | 10050 |
| sinhue10 | 0.475 (0.20 / 0.75) | 0.17 | 0.60 | 0.64 (0.32 / 0.28) | 390 | 10360 |

## Qué falló (declarado)
- **Refutadas en práctica, antes del preregistro:**
  - «repasar mucho (cada 20 pasos) retiene sin costo»: la comida temprana bajó 0.20 en las dos semillas.
  - «un repaso por mordida basta»: en s15890, +0.05 de RET40 y −0.12 de adquisición.

  Por eso quedaron las dos dosis como brazos. La dosis 10 sale de la práctica, y lo declaro.
- **En el humo final, contra mi preregistro:**
  - **P1 cae** (0.6875 < 0.75).
  - **ADQ40_com baja** (0.90 → 0.60). Esa medida no está entre las principales: el repaso cuesta la adquisición **temprana**,
    no la tardía.
  - P11 va en contra en esta semilla: rep1 ya sube 0.10.
- **Límite de diseño:** el techo honesto de RET40 ronda 0.75 si sólo se retiene lo adquirido (el veneno sale gratis). La vía (a)
  (el código cambia) queda intacta.
- **Corridas usadas:** 1 diagnóstico y 4 humos de un proceso (≤ 200 000 pasos cada organismo), más el arnés (una corrida de
  200 000).

## Qué queda
- **Serie y réplica** (§9 del preregistro): unos 35 min de CPU cada una, ~7 min de pared con Pool 6. Después, `--veredicto`.
- **Puntos:** FUNCIONA +15 (p ≈ 0.07), MODESTO +5 (p ≈ 0.35), NO +0. Lo esperable es **+0 a +5**.
- **No verifiqué:**
  - la rama `Pool` (prohibida);
  - el tiempo exacto con un Pool ajeno corriendo.
- **Para el Frankenstein** (`experimentos/frankenstein/`, otro equipo): el órgano ya es una perilla (`repaso`, `dosis`) y se
  puede injertar por anclas. Allí sería exploratorio, no dato.
