# PREREGISTRO — examen del CRITERIO DE TRONCO v4 sobre v14.4b = v14.3 + TERMO′ (TERMO con memoria que olvida)

**Escrito ANTES del humo** (28-sep-2026, creador). Antes de esto se corrió:
- la construcción por anclas;
- la búsqueda de semillas;
- el arnés (129/129);
- el **EXPLORATORIO** de TERMO′ (`explora_termop.py`). Sus números están **a la vista** y se declaran en la sec. 5.

Encargo del coordinador: un candidato distinto de TERMO, con memoria que se desdiga, para que no caiga por reversión (T-E y T-C).
Misión: llegar a la AGI por este camino.

## 1. Hipótesis
**H-v144b:** v14.3 + TERMO′ no hace nada peor que v14.3 en T-A…T-F y sube el crecimiento neto del linaje en el mundo vivo (T-G), con el
control TERMOPINV, en semillas nuevas, serie y réplica.

## 2. La pieza (lo único que cambia respecto de TERMO)
- **La letra es la misma**: `termo_letra`, el mismo texto de v14.4.
- **Cambia la memoria de lo sentido.** En TERMO era una suma sin olvido (media de todas las mordidas). En TERMO′ es una **media móvil**:
  - en la primera mordida, e ← dS;
  - en las siguientes, e ← e + ema_c·(dS − e);
  - se guarda como `[e_0, (e_1,) 1]`, así que la letra lee s = e.
- **ema_c = 0.05** es la tasa que el tronco **ya tiene** (sus medias condicionadas, hija dispersa D); en el carro es la misma
  (`FABRICA kw['ema_c']` = 0.05). **Constantes nuevas: cero.** Memoria: la misma forma que TERMO (nueva respecto de v14.3, declarada).
- **Mundo quieto** (el dS de un estímulo no cambia): e == dS exacto, y TERMO′ decide como TERMO salvo empates de coma flotante en el
  umbral (TERMO usaba suma/n).
- **Tras invertir** (+0.8 → −0.4): e cruza 0 en ~22 mordidas, porque 0.95^k < 1/3. Con TERMO, del orden de 300–800.
- **Por qué esta opción y no leer una memoria que v14.3 ya tiene** (las filas de valor Wp/Wn por necesidad, que sí se desdicen):
  - su escala es la del refuerzo (+1/−3), no la del dS; la consigna U + s/2 dejaría de tener sentido;
  - en la carrera esas filas se **borran al nacer** cada cuerpo, mientras que lo sentido es del linaje. El efecto de TERMO en la pista
    depende de que los recién nacidos ya sepan qué es bueno.

## 3. Instrumento (todo por anclas desde el examen de v14.4, con sha fijado; `construye_termop.py`, `construye_examen_v144b.py`)
| archivo | sha16 | origen |
|---|---|---|
| `organismo_v144b.py` | `c8f0c25302f20fd9` | `tronco_v14_4_examen/organismo_v144.py` (`e3768f6eab05b964`): una línea (la acumulación) |
| `organismo_v144bg.py` | `19106bea564d4a94` | `organismo_v144g.py` (`1ea7fb43f41a69c5`) |
| `organismo_v144bcal.py` | `b9c2cf7b73007a96` | `organismo_v144cal.py` (`a5a891e1d819e1bb`) |
| `bateria_v144b.py` / `bateria_generaliza_v144b.py` | `01e00e0d3c283561` / `3bbd29d3d71b022a` | las de v14.4; una entrada nueva campo a campo |
| `corre_examen_v144b.py` / `identidad_v144bex.py` | por `construye_examen_v144b.py --verifica` | `corre_examen_v144.py` (`8bb63d3f421040dd`) / `identidad_v144ex.py` (`6a714b193b6222dc`) |
| `umbrales_examen_v144b.py` | — | **importa** letra, T-G y brazos de `umbrales_examen_v144` (`0df02bd6a4d548c4`); sólo cambian semillas y predicciones |

**Arnés `identidad_v144bex.py`: RESULTADO 129/129** (167 s; JSON `datos/humo/identidad_v144bex_20260928_131619.json`, `4a69216ea63996d6`).
Es el de v14.4, con el bloque de la memoria cambiado:
- en el mundo quieto, e == dS exacto con "mordidas" = 1;
- tras invertir, A queda negativa (−0.155) y B positiva (0.698);
- el carro V143_TERMOP acumula con la misma regla y la misma ema_c.

La letra se compara en 37 960 casos con los **cuatro** carros (TERMO, TERMOINV, TERMOP, TERMOPINV). Pieza apagada == v14.3 bit a bit: (A) 21/21.

## 4. La letra: la del examen de v14.4, **sin un número cambiado**
T-A…T-F y T-H son las del examen de v14.3 (ERR-122 incluida). T-G es la de v14.4: CUELLO_MIN, m = 1, n = 80, control TERMOPINV,
P(T-G | nulo) 0.042. Ver `PREREGISTRO_examen_v144.md` sec. 4.

## 5. Predicciones (antes del humo; **con el exploratorio a la vista, declarado**)
**Exploratorio** (2 semillas, 49001–49002; `datos/explora_termop_examen_20260928_124457.json`, `fc6be0f273d33d7f`):
| medida | v14.3 | TERMO | TERMO′ |
|---|---|---|---|
| E2: muerde A en Q4 | 10, 11 | 160, 165 | **5, 7** |
| T-C (ii): rev | 38, 30 | −7, 8 | **22, 2** |
| T-C (ii): come B en Q4 | 198, 197 | 86, 84 | 163, 121 |
| T-C (ii): muertes | 102, 102 | 113, 90 | **77, 87** |

- **T-E se arregla:** TERMO′ se desdice en E2.
- **T-C (ii) probablemente sigue cayendo, pero por otra razón.** `rev` = mordidas de B − mordidas de A en Q4, **en números absolutos**. Un
  termostato come menos, también de lo bueno nuevo, porque no come cuando está lleno. Es la cláusula que en el preregistro de v14.4
  llamé "castiga comer menos" (riesgo 7.6). Aquí aparece en T-C (ii). Candidato a ERR: medirlo por visita (B mordida/visitada −
  A mordida/visitada). **No se cambia la letra**: haría falta ERR y un nulo nuevo.

| puerta | predicción | p |
|---|---|---|
| legible | como v14.3 y v14.4 | 0.97 |
| T-A | como TERMO (sin reversión son lo mismo salvo empates) | 0.55 |
| T-B | como TERMO | 0.90 |
| **T-C** | (i) p 0.85; **(ii) `rev` mediana 0–30 (OFF ≈ 42) → LI > −12.5 con p 0.2** | **0.15** |
| T-D | como TERMO | 0.85 |
| **T-E** | **E2 pasa** (muerde A en Q4 ≤ 1.10 × tronco); riesgo en E1/E2L "come A Q4 ≥ 0.8 ×" | **0.60** |
| T-F | las muertes de T-C (ii) bajan (77, 87 contra 102) | 0.75 |
| T-G | como TERMO: G-1 p 0.25 | 0.25 |
| **serie** | **NO PASA (p ≈ 0.95)**, sobre todo por T-C (ii) (comer menos, no la reversión) y por T-G | 0.02 |

## 6. Qué refuta
- Si E2 vuelve a caer por "muerde A Q4", **la olvidadiza no se desdice lo bastante rápido**: refuta el diseño.
- Si T-C (ii) cae con la memoria de A ya negativa y las muertes por debajo del tronco, queda escrito que la puerta mide **cuánto se come**,
  no si se desdice. Eso va al coordinador como ERR candidato, sin tocar este veredicto.
- Si cae T-G, el termostato no sube el crecimiento en el mundo vivo (lo mismo que para TERMO).

## 7. Riesgos declarados
Los siete de `PREREGISTRO_examen_v144.md` sec. 7 siguen vigentes (base distinta, 3T-k, U en mundos sin parto, etc.). Además:
- las predicciones de la sec. 5 se escribieron **con** el exploratorio a la vista;
- el carro `V143_TERMOP` cambió de sha durante el exploratorio de la carrera (`e883…` → `edf5…`), **sólo en comentarios**.

## 8. Semillas NUEVAS (`busca_semillas_v144b.py`: 44 040 archivos; en 49000–49999 y 149000–149999 sólo fragmentos de sha)
| papel | serie | réplica |
|---|---|---|
| examen v3′ y T-B | 49101–49120 | 49121–49140 |
| mundo vivo T-A (+ CTRL) y T-C (ii) | 49201–49280 (TRONCO_B 149201–) | 49301–49380 (TRONCO_B 149301–) |
| T-D ALIAS | 49509 49528 49563 49597 49621 49652 49718 49756 49871 (de 49501–49999) | 149519 149541 149592 149657 149658 149666 149670 149715 149719 (de 149501–149999) |
| T-D LIMPIAS | 49502 49516 49518 49519 49521 49526 49543 49564 49566 | 149504 149507 149514 149522 149532 149536 149547 149550 149556 |
| reserva | 49401–49480 | |
| humo / identidad | 49901–49903 / 49905–49907 | |

- Semillas ya usadas por el exploratorio: 49001, 49002, 49011–49015 y 49099.
- La carrera de TERMO′ usa 49941–49994.
- La regla 14 (R6) comprueba que ninguna se cruza.

## 9. Comandos (sólo el coordinador)
```
python experimentos/tronco_v14_4b_examen/corre_examen_v144b.py --serie --pool 6
python experimentos/tronco_v14_4b_examen/corre_examen_v144b.py --replica --pool 6 --con experimentos/tronco_v14_4b_examen/datos/examen_v144b_serie_<sello>.json
python experimentos/tronco_v14_4b_examen/corre_examen_v144b.py --bloque <serie.json> <replica.json>
```
Costo: 1 476 corridas y ~30–50 min por serie con Pool 6, igual que v14.4.

## 10. Humo — escrito DESPUÉS
(pendiente)
