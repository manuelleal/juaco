# PREREGISTRO — subida del nivel 8, tanda 3: memoria lenta con repaso (pieza 2, "retener lo ausente") (23-sep-2026)

Misión: llegar a la AGI por este camino. Creador de la tanda 3 del nivel 8 (pedido del director: "lanza este además").
Escrito **después** de un diagnóstico y tres humos de práctica (semillas 15890, 15891, 15890 otra vez; no son de la serie) y
**antes** del humo final (15893) y de la serie 15801–15820 y la réplica 15821–15840, que no se han corrido. Cualquier cambio
posterior a este archivo es **candidato a ERR**.

## 0. De dónde parte
- Tanda 1 (`subida_n8`, REGISTRO «SUBIDA N8», serie + réplica): el tronco v14.2 sigue aprendiendo la comida nueva por encima
  del a priori (×2), pero **olvida lo ausente: RET40 = 0.625 en las dos** (P4). La fusión no lo arregla (RET40 −0.075).
  Tanda 2 (`subida_n8b`, sin serie): el cuello de la adquisición es de muestreo (neofobia), no de celdas.
- Pieza 2 del 100 % (tabla §0 de `subida_n8/PREREGISTRO_n8.md`): "retener lo ausente mientras aprende lo nuevo", peso 20, hoy 0.
- Líneas que **no** repito: metaplasticidad (refutada 18-sep), fusión (tanda 1), almacén externo de pares patrón→R (K4,
  "memoria escondida", `v11_consolidacion/ESPEC_exploracion_autorepaso.md`).
- **Diagnóstico de práctica (s15890, BASE, un proceso; declarado, no es dato):** de las 20 comidas de los 40 primeros, el
  olvido tiene tres vías mezcladas: (a) el **código cambia** (3 de 20: la puerta pierde la evidencia del código exacto y la
  lectura cae a la vía lenta, que dice «veneno»); (b) **interferencia** en celdas compartidas con el mismo código (el valor
  rápido pasa de +1.07 a −1.19 aunque el estímulo se mordió 6 veces más); (c) **neofobia**: en el último cuarto las 20 comidas
  viejas se visitan 284 veces y se muerden 11: lo que se lee como veneno no se vuelve a probar, y no se corrige.
  El repaso sólo puede tocar (b) (y, por la conducta, algo de (c)); (a) queda fuera por diseño (§2).

## 1. Hipótesis
**H-REP (sistemas complementarios; McClelland, McNaughton y O'Reilly 1995; Kumaran, Hassabis y McClelland 2016; repaso
generativo, Shin et al. 2017; repaso despierto tras la recompensa, Foster y Wilson 2006).** Si tras cada mordida el
organismo repasa, intercalado, patrones reconstruidos desde **sus propias huellas por celda** (la media del patrón cuando la
celda recibió recompensa positiva o negativa, que el tronco ya guarda) y los consolida en sus pesos de valor con la misma
regla local de la mordida, retiene los 40 primeros estímulos mejor que el tronco sin pagar la adquisición de lo nuevo; y lo
que lo hace es el **contenido** de la huella (el signo), no el mero hecho de repasar.

## 2. Mecanismo mínimo y memoria nueva
- **Organismo:** tronco v14.2 sin cambios. `organismo_repaso.py` (`1dce42830f4230bc`) se construye **por anclas**
  (`construye_n8c.py`, 5 anclas con conteo exacto) desde `experimentos/subida_n8/organismo_flujo.py` (`14afed5aa16e09bf`,
  anclado al congelado `organismo/organismo_v142.py` `17528d767fcebaf6`, que sólo se lee). Con `repaso=0` es
  `organismo_flujo` EXACTO en todas las claves (arnés A, A1) y la BASE reproduce medida por medida el JSON de la serie de
  `subida_n8` en la semilla 12601 (arnés A3).
- **Órgano REPASO** (`repaso=1`): tras cada mordida real, `dosis` veces: (1) elige una celda activa con huella
  (`zp+zn > 0`) con un generador APARTE `[semilla, 8338]`; (2) sortea el signo de la huella en proporción `zp:zn`;
  (3) reconstruye P̂ = los `round(masa)` píxeles más altos de `mup/zp` (o `mun/zn`); (4) aplica UNA actualización
  Rescorla-Wagner sobre `code(P̂)` en Wp/Wn, con el drenaje `lam`, `eta`, `aversion` y el techo 3 de la mordida; objetivo =
  la **última R vivida de ese signo**. **No** divide, no funde, no toca `mu/err/mup/mun/zp/zn`, la vía lenta, la energía,
  el rng del organismo ni **la evidencia `ncod` de la puerta** (reconocer sigue exigiendo mordidas reales: el repaso no
  fabrica familiaridad). Estático verificado (arnés F1–F4).
- **Memoria nueva: 2 números** (última R positiva y última R negativa vividas). **Constante nueva: `dosis`** (1 o 10).
  La dosis 10 sale de la práctica (un repaso cada 20 pasos ≈ 10 por mordida); la dosis 1 es la sin constante. Se declara.
- **Controles del mismo presupuesto (10 repasos por mordida):**
  - **BARAJ10** (`repaso=2`, puede ganar): el mismo P̂, pero el **signo del objetivo** sale de la huella de **otra** celda
    sorteada. Misma proporción de objetivos positivos (arnés B5: 0.801 contra 0.799). Si empata o gana, lo que retiene es
    repasar, no lo que se repasa.
  - **SINHUE10** (`repaso=3`, "repaso sin consolidación de la huella", K6 de `v11_consolidacion`): el mismo P̂, objetivo =
    `K·(Wp[c]−Wn[c])`, el valor **actual** de la celda: repasa lo que hoy cree, no la huella. Si empata o gana, la segunda
    memoria no aporta.
- **Mundo:** el de `subida_n8` sin cambios (`mundo_n8.py` `b0b57d7ff02afe4e`, importado de solo lectura): retina 12,
  200 estímulos de peso 3, uno cada 1000 pasos, ventana 8, p_viejo 0.25, valencias 5/5 por bloque; T = 200 000.

## 3. Brazos (5 × 20 semillas por serie)
| brazo | repaso | dosis | pregunta |
|---|---|---|---|
| base | 0 | – | el tronco (validez: reproduce subida_n8) |
| rep1 | 1 | 1 | dosis sin constante |
| **rep10** | 1 | 10 | **brazo principal** |
| baraj10 | 2 | 10 | control que puede ganar: ¿importa el contenido? |
| sinhue10 | 3 | 10 | control: ¿importa la huella o basta repasar el valor actual? |

## 4. Medidas (`corre_n8c.py`; las de `subida_n8` con la misma definición, más las de retención)
- **RET40** = acierto de signo balanceado de los 40 primeros en t = T−1; **RET40_com / RET40_ven** = por clase;
  **RET40_rel** = de las comidas de los 40 primeros que estaban aprendidas (valor > 0) al salir de la ventana, fracción que
  sigue > 0 al final. **ADQ_tarde, ADQ_tarde_com, PRIOR_tarde_com** (entradas 140–189, al salir de la ventana), NULO, muertes,
  repasos. Letra de pareados: «A > B» = A mayor en **≥ 15/20** y diferencia mediana **≥ 0.03**.
- Nota honesta sobre el techo: en `subida_n8` la comida temprana se adquiere 0.43–0.60 y el veneno sale gratis (≈ 1.0);
  si sólo se retuviera lo adquirido, RET40 ≈ (0.5 + 1)/2 ≈ 0.75. **Pasar de 0.75 exige que el repaso además haga volver a
  probar comida vieja.** Por eso P1 tiene p baja.

## 5. Predicciones firmadas (medianas de 20 semillas; REP = rep10)
| | predicción | p |
|---|---|---|
| P1 | **Central del encargo, puede fallar:** REP RET40 ≥ 0.75 | 0.10 |
| P2 | REP > BASE en RET40: ≥ 15/20 **y** diferencia mediana ≥ 0.05 | 0.35 |
| P3 | **Puede fallar:** la adquisición no baja más de 0.05: mediana REP − mediana BASE en ADQ_tarde_com **y** en ADQ_tarde ≥ −0.05 | 0.30 |
| P4 | REP > BARAJ10 en RET40 (el contenido de la huella) | 0.55 |
| P5 | REP > SINHUE10 en RET40 (la huella, no el valor actual) | 0.40 |
| P6 | Muertes REP / BASE ≤ 1.15 | 0.80 |
| P7 | REP RET40_ven ≥ 0.85 (no compra comida vieja confundiendo veneno viejo) | 0.75 |
| P8 | Validez: BASE RET40 en 0.55–0.70 (reproduce subida_n8) | 0.85 |
| P9 | REP > BASE en RET40_rel | 0.45 |
| P10 | Dosis: mediana(REP10 − BASE) > mediana(REP1 − BASE) en RET40 | 0.60 |
| P11 | REP1 y BASE no se separan en RET40 (ninguno gana con la letra) | 0.70 |

Mi apuesta global: **NO o HAY ALGO MODESTO** (p ≈ 0.45 / 0.35); FUNCIONA p ≈ 0.07. La práctica (con la versión de repaso cada 20
pasos, ≈ 10 por mordida, no con la de este preregistro): RET40 REP − BASE = +0.125 (s15890) y 0.00 (s15891); REP − BARAJ =
+0.20 y +0.175; adquisición de comida −0.04 y −0.12. Con 1 repaso por mordida (s15890): RET40 +0.05, adquisición −0.12.

## 6. Letra (el runner la aplica: `--veredicto SERIE.json REPLICA.json`, última línea)
- **NO SE LEE:** P8 falla en alguna de las dos (la base no reproduce el instrumento).
- **FUNCIONA:** P1, P2, P3, P4, P5, P6 y P7 en la serie **y** en la réplica. Se diría: *«con un órgano de repaso de sus
  propias huellas (2 números de memoria nueva, reglas locales), el tronco retiene los 40 primeros de 200 estímulos por encima
  de 0.75 sin pagar la adquisición de lo nuevo, y es el contenido de la huella lo que retiene (dos series)»*.
- **HAY ALGO MODESTO:** P2, P4, P6 y P7 en las dos, pero falla P1, P3 o P5. Se diría: *«repasar las huellas retiene más que
  el tronco y es el contenido de la huella, pero [no llega a 0.75 | cuesta adquisición | no se separa del repaso del valor
  actual]»* (se nombra lo que falla).
- **NO:** cualquier otro caso. Si P2 pasa y P4 no: *«repasar retiene, pero el contenido no importa»* (el runner lo nombra).
- **Prohibido:** «consolida como el hipocampo», «acumula», «aprendizaje abierto», «no olvida»; RET40 sin RET40_com y
  RET40_ven al lado; hablar de «sistemas complementarios» como mecanismo demostrado (es la inspiración, no lo medido).

## 7. Puntos del nivel que movería (propuesta; decide el director)
- **FUNCIONA:** pieza 2 **+15** de 20 (los 5 restantes piden más de 40 ausentes y un segundo mundo). Nivel 8 → 60–65 %
  según lo que el director fije de aprende_barrer y subida_n8.
- **HAY ALGO MODESTO:** **+5**.
- **NO:** **+0**; queda medido que repasar desde las huellas por celda no alcanza, y que la vía (a) (código que cambia) y la
  (c) (neofobia) son las que mandan: el siguiente candidato tendría que tocar la puerta o el muestreo (enlaza con subida_n8b).

## 8. Semillas (verificadas con grep el 23-sep en todo `PROYECTOS\JUACO`, worktrees incluidos, en .py y .md y en nombres de archivo)
- Serie **15801–15820**, réplica **15821–15840**. Práctica 15890–15891 (usadas), humo final **15893**.
- `grep -rIn -E "\b158[0-9]{2}\b" --include=*.py --include=*.md` sin coincidencias antes de este paquete; ningún archivo con
  `s158xx` en el nombre. (Los JSON de datos antiguos traen números 158xx dentro de vectores; no son semillas.)

## 9. Comandos (sólo el coordinador) y costo
```
python experimentos/subida_n8c_memoria_lenta/identidad_n8c.py        # 29/29, ~65 s, un proceso
python experimentos/subida_n8c_memoria_lenta/corre_n8c.py --serie base,rep1,rep10,baraj10,sinhue10 --desde 15801 --n 20 --pool 6
python experimentos/subida_n8c_memoria_lenta/corre_n8c.py --serie base,rep1,rep10,baraj10,sinhue10 --desde 15821 --n 20 --pool 6
python experimentos/subida_n8c_memoria_lenta/corre_n8c.py --veredicto <JSON serie> <JSON replica>
```
Costo: 100 corridas × ~19–22 s ≈ **35 min de CPU por serie**, ~7 min de pared con Pool 6; las dos ≈ 70 min de CPU.
El runner verifica shas y la entrada campo a campo (regla 14) antes de correr; aborta ante banderas desconocidas o abreviadas.
