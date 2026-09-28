# PREREGISTRO (BORRADOR del creador) — examen del CRITERIO DE TRONCO v4 + T-R sobre v14.4b = v14.3 + TERMO′

**Escrito ANTES del humo del runner** (28-sep-2026, creador de TERMO′). Antes de escribir esto se corrió sólo:
- la construcción por anclas (`construye_v144b.py`), la búsqueda de semillas (`busca_semillas_v144b.py`, no simula) y la selección
  estructural de T-D (`diagnostico_codigos.solapamientos`, no simula);
- el arnés `identidad_v144bex.py` (**151/151**) y el arnés del carro `identidad_termob.py` (**11/11**).

Las predicciones (sec. 5) están en `umbrales_examen_v144b.PRED` desde la **primera** construcción, **antes** de correr ningún arnés; salen
del mecanismo y de los crudos de la serie de TERMO (47101–47180), que ya existían. Los arneses imprimen lecturas de una semilla de
identidad; ninguna cambió una predicción ni un umbral. La sec. 12 (humo) se escribe después y se dice.

Diseño decidido por el coordinador (28-sep, tras el NO PASA de TERMO en su serie: cae T-C (ii) y T-E). El creador lo construye y no lo
cambia; lo que ve mal lo declara en la sec. 7. Misión: llegar a la AGI por este camino. **El examen v4 es la puerta de NO REGRESIÓN del
organismo común.** Shas y comandos definitivos los fija el coordinador (sec. 3 y 11).

## 1. Hipótesis
**H-v144b:** el tronco v14.3 con TERMO′ no hace nada peor que v14.3 en lo que el tronco ya hace (T-A…T-F, en los mundos de la letra).
Además **se desdice en el mundo vivo con la pieza actuando** (T-R) y **sube el crecimiento neto del linaje** en el mundo vivo (T-G), con
el control TERMOINV que no lo hace. Todo en semillas nuevas, en serie y réplica.

## 2. Qué cambia respecto de v14.4 (TERMO), por qué, y qué puerta lo prueba
Todo lo demás es v14.4: la misma letra (`termo_letra`, el mismo texto en los seis organismos; regla 14 R4), TERMOINV (`termo = 2`) como
control de T-G, los contadores de sólo lectura y la consigna U = 1.0 en el mundo vivo.

**(1) LA TABLA OLVIDA.** Por estímulo mordido, TERMO guardaba la suma del dS nominal y el número de mordidas (s = suma/n). Esa memoria
es **suma sin olvido**: tras la inversión de T-C (ii), A siguió “sentida buena” y TERMO la siguió mordiendo (rev CAND −12 contra OFF 44).
- TERMO′ guarda el **último** dS nominal sentido: `_adS[k] = [dS_0, (dS_1,) 1]`. La letra lee s = dS/1 = dS.
- Con dS fijo por estímulo la s es la misma que la media, salvo ulp → las mismas decisiones (arnés (T); ver 7.3). Tras una inversión,
  **una** mordida basta para que lo que fue bueno deje de gobernarse (arnés (V): la memoria de A es exactamente [−0.4, 0, 1]).
- Memoria: la misma forma que en v14.4 (2 o 3 números por estímulo); el contador pasa a ser la constante 1. **Memoria nueva respecto de
  v14.3: sí** (la de TERMO).
- **La prueban T-C (ii) y T-R.**

**(2) SIN UMBRAL DE PARTO NO HAY CONSIGNA.** En `organismo_v144b` y `organismo_v144bg` (una necesidad, sin medida de parto), el kwarg
`rep_umbral` pasa a defecto `None`. Con `None`, la pieza **no decide**: devuelve la decisión de v14.3 tal cual y no toca contadores.
- Resultado: con sus defectos, v14.4b y v14.4bg son v14.3 y v14.3g **en la física, bit a bit**. Arnés (I): 12 escenarios del examen y
  3 reglas, con dec = a_no = a_si = 0; (D): la tarea E2 de la batería, a T = 100 000, y la tarea px0 de T-B, a T = 200 000, son
  idénticas a las del tronco en todas las claves.
- La guarda es el **mismo texto** en los tres organismos. En `organismo_v144bcal` el defecto sigue siendo 1.0 y la pieza **actúa**
  (T-A, T-C ii, T-D, T-G).
- **La prueban T-E y T-B** (y con ellas T-C (i) y T-F examen). Por construcción, ahí el candidato es el tronco contra sí mismo: esas
  puertas ya no miden a TERMO, sólo que la pieza esté de verdad muda. Se declara.

**DECLARACIÓN (2) es POST-HOC.** Se decidió **después** de ver caer T-E en el examen de TERMO. El diagnóstico del coordinador, sobre el
crudo EX: E2 es la reversión; E1, E2J, E2K y E2L caen porque en los mundos de una necesidad el termostato come ~10 % menos (A Q4 70
contra 80; D 61–63 contra 74–76) y muere menos, y la cláusula “come ≥ 0.8 × tronco” cae semilla a semilla.
- En esos mundos no hay parto. U = 1.0 fue una constante **inventada** por el creador anterior (PREREGISTRO_examen_v144 sec. 2 y 7.3).
- **Alternativa descartada:** mantener U = 1.0 en los mundos de una necesidad. La pieza seguiría actuando donde su consigna no significa
  nada, y T-E volvería a medir saciedad, no regresión.
- **Precedente:** B-5 (v14.2) y la reparación N (v14.3) entraron al tronco siendo **inertes** en los mundos del tronco donde no tenían
  nada que reparar.
- **Coste declarado:** (2) quita a T-E y T-B su poder de detectar un daño de TERMO′ en la conducta de una necesidad. Si TERMO′ entra, el
  tronco tendrá una perilla que sólo actúa donde hay umbral de parto.

## 3. Instrumento y anclas (`experimentos/tronco_v14_4b_examen/`; los orígenes sólo se leyeron) — **shas fijados por el coordinador el 28-sep antes de la serie**
| archivo | sha16 (creador, 28-sep) | origen (sha) | qué es |
|---|---|---|---|
| `organismo_v144b.py` | `54e9300ee13f42b7` | `tronco_v14_4_examen/organismo_v144.py` (`e3768f6eab05b964`) | el candidato (a CONGELADOS si pasa) |
| `organismo_v144bg.py` | `92b60c6f367b7440` | `…/organismo_v144g.py` (`1ea7fb43f41a69c5`) | su mundo de regla |
| `organismo_v144bcal.py` | `548e0b75049aaa30` | `…/organismo_v144cal.py` (`a5a891e1d819e1bb`) | v14.4b en el mundo vivo (instrumento) |
| `bateria_v144b.py` | `fb90ced8264da980` | `…/bateria_v144.py` (`e928b202d9d66702`) | examen v3′ apuntando a v144b |
| `bateria_generaliza_v144b.py` | `48b0fbd741c0da50` | `…/bateria_generaliza_v144.py` (`3263ab8d8f45e7cd`) | entrada `organismo_v144b`, campo a campo |
| `corre_examen_v144b.py` | `124049e2a917e7d3` | `…/corre_examen_v144.py` (`8bb63d3f421040dd`) | el runner (+ T-R) |
| `umbrales_examen_v144b.py` | `a31576e7202a69a3` | `…/umbrales_examen_v144.py` (`0df02bd6a4d548c4`) | letra, semillas, PRED |
| `busca_semillas_v144b.py` | `a1e30923098fc170` | `…/busca_semillas_v144.py` (`e3220d8311115207`) | búsqueda de semillas |
| `carros/V143_TERMOB.py` | `ff532f78fdc80888` | `organelos/termo/carros/V143_TERMO.py` (`3db639cab75641fb`) | carro de la pista (muro) |

- `construye_v144b.py` los genera por anclas. Cada ancla aparece exactamente una vez, salvo los **renombres de módulo**
  (v144 → v144b), que llevan su cuenta exacta como tripwire. `--verifica` compara el disco con la construcción.
- `construye_v144b.py` `9a46d9ea4bbc98ac` · `identidad_v144bex.py` `c866e0575fbe2d7c` · `identidad_termob.py` `ca2d83efda4c26e3`.
- Arneses: `identidad_v144bex.py` (el runner lo exige antes de cada serie) e `identidad_termob.py` (el del carro; no entra al examen).

## 4. La letra, puerta por puerta
**T-A…T-F y T-H son la letra de v14.4 (la del examen de v14.3), sin tocar un número. T-G es la de v14.4.** Umbrales: `umbrales_examen_v144b.py`
(LETRA, NUM, ERR122, TG importados). Los n y los montajes son los de PREREGISTRO_examen_v144 sec. 4, con las semillas de la sec. 8.

**T-R (NUEVA, más estricta; no reemplaza nada; eliminatoria):** la reversión con la pieza **actuando**. T-C (ii) pasa por la letra v4
(NI en `rev`, margen 12.5) **y** la pieza actúa (a_no + a_si > 0) en ≥ 95 % de las 80 corridas CAND de T-C (ii). Es el análogo de G-3.
- Por qué: con (2) el principio es “la pieza sólo actúa donde hay consigna”. Una reversión aprobada con la pieza muda no probaría (1).
- Comprobado antes del humo:
  - en la serie de TERMO, la pieza actuó en T-C (ii) en **80/80** corridas (`serie_pool6.log`; dec 5 284, a_no 3 168 por corrida);
  - en el arnés (P), actúa en T-C (ii) con TERMO′;
  - el juez aplicado a la serie de TERMO da T-R **NO**, porque T-C (ii) cae con la pieza actuando 80/80 (arnés (J)).
- La reserva (4′) también sustituye T-R.
- **Veredicto: PASA ⇔ las ocho puertas (siete de v4 + T-R) en serie y réplica legibles.**

## 5. Predicciones firmadas (p = probabilidad de que la puerta PASE en UNA serie; `umbrales_examen_v144b.PRED`)
**El mecanismo que las ordena, visto antes de correr:**
- (2) hace del examen v3′ y de T-B el tronco contra sí mismo.
- Sin inversión (T-A, T-D, T-G), TERMO′ decide como TERMO: se esperan los números de la serie de TERMO.
- **En T-C (ii), (1) quita a la pieza el gobierno de A a la primera mordida mala, PERO se lo da sobre B** (la comida nueva, desde su
  primera mordida después de invertir). B pasa a comerse sólo con E < 1.4.
- En TERMO, antes de invertir, la pieza bajó las mordidas de la comida ~25 % (A 152 contra 204 del OFF por cuarto) y también las del
  veneno (119 contra 156).
- `rev = mordB_Q4 − mordA_Q4` es una **diferencia de conteos**. Si todo baja ~25 %, `rev` baja de ~44 a ~33: d ≈ −11 contra el margen
  −12.5, con LI ≈ −15. **T-C (ii) y T-R siguen siendo las puertas en riesgo aun con la tabla que olvida** (trampa 3).

| puerta | predicción numérica | p |
|---|---|---|
| legible | TRONCO_B pasa T-A, T-C (ii) y T-F vivo | 0.97 |
| T-A | como TERMO: `r` VIVO CAND mediana en [−45, −20] (OFF ≈ −75), CUELLO_MIN en [0, +15] (OFF ≈ −6); muertes 0.6–0.95 × | 0.95 |
| T-B | CAND == TRONCO en la física (40/40 idénticas): G1 1.000, G2 ≥ 0.95; azar G2, el del tronco, en [0.31, 0.60] | 0.95 |
| T-C | (i) == tronco (p 0.97); **(ii) `rev` CAND mediana en [15, 40] (OFF ≈ 44), media de d en [−20, −3]: LI > −12.5 con p 0.35** | **0.33** |
| T-D | como TERMO: C1, C2 y C6 pasan | 0.95 |
| T-E | CAND == TRONCO en la física (120/120 idénticas) | 0.97 |
| T-F | examen: razón 1.0; vivo: muertes de T-C (ii) 0.9–1.1 ×, T-A ≤ 1.0 × | 0.90 |
| T-G | como TERMO: d media de G-1 en [+8, +22] (LI > 1 con p 0.92); G-2 p 0.98; G-3 80/80 | 0.90 |
| **T-R** | la pieza actúa en T-C (ii) en 80/80: T-R ≈ T-C (ii) | **0.34** |
| **serie** | producto ≈ 0.25 (T-C ii y T-R son casi la misma apuesta) | **0.25** |
| **serie + réplica** | **veredicto previsto: NO PASA** (p ≈ 0.85), por T-C (ii) y T-R | PASA ≈ 0.15 |

## 6. Qué significa cada veredicto y qué refuta H-v144b
- **PASA** (serie y réplica legibles, ocho puertas): v14.4b puede entrar al tronco. **Decide el director** (sec. 10).
- **NO PASA:** no se congela; v14.3 sigue siendo el tronco. Se lee dónde cae:
  - **(a) T-C (ii) y T-R, con `rev` CAND > 0 y A Q4 ≈ OFF.** TERMO′ **se desdice** (A deja de morderse como comida) pero come menos de la
    comida nueva, y la letra de conteos absolutos lo castiga. (1) funciona; la regresión es la del termostato en una puerta de conteos.
    **Refuta la parte de no regresión de H-v144b tal como está escrita.** No autoriza a cambiar el margen.
  - **(b) T-C (ii) con A Q4 ≫ OFF.** (1) no bastó; refuta (1).
  - **(c) T-E o T-B.** (2) no es inerte: sería un error del instrumento (el arnés (I)/(D) dice que lo es). Primero ERR, no conclusión.
  - **(d) T-G.** El termostato no sube el crecimiento en semillas nuevas: la serie de TERMO no replica.
- **NO SE LEE:** TRONCO_B cae también en la reserva → ERR.
- Vocabulario si PASA: *“el termostato de boca con memoria del último bocado sube el crecimiento neto del linaje en el mundo vivo, se
  desdice tras la inversión y no empeora nada de lo que hacía v14.3, replicado”*. Prohibido: “cruza H-1”, “regula como un animal”.

## 7. Lo que el creador ve mal o arriesgado (candidatos a ERR; nada se cambió por ellos)
1. **(2) es post-hoc** (sec. 2). Precedente y alternativa declarados; el director decide si lo acepta.
2. **Inconsistencia de (2) con el mundo vivo — HALLAZGO que el coordinador debe mirar.**
   - T-C (ii) (`mini_vivo.BRAZOS['VIVO']`) y T-D (`corre_sal.BASE`) corren con `reproduccion = 0`: dentro de `run`, `rep_mide` se fuerza
     a 0. **Ahí tampoco hay medida de parto.**
   - Aun así, la pieza actúa con U = 1.0 (el defecto de `organismo_v144bcal`), igual que en TERMO.
   - Aplicado al pie de la letra (“sin umbral de parto no hay consigna”), (2) silenciaría la pieza también en T-C (ii) y T-D. T-C (ii)
     pasaría trivialmente y T-R caería (la pieza no actuaría). El diseño del coordinador la mantiene actuando ahí, y así se construyó.
   - Consecuencia: el principio de (2) se aplica por **organismo** (una necesidad contra dos), no por mundo. Se declara.
3. **Empate de ulp (arnés (T)).** Con U = 1.0 en una necesidad (`vivo = 0`; examen AB con `rep_umbral = 1.0` explícito), TERMO′ y TERMO
   divergen en la consulta 408 de la semilla 49045:
   - E = 1.4 exacto contra el umbral U + s/2: 1.4 en TERMO′, 1.4000000000000001 en TERMO (su media es 0.8000000000000004, 3 ulp);
   - TERMO′ no muerde y TERMO sí. TERMO′ es la letra exacta; la media de TERMO redondeaba.
   - En los cuatro montajes del mundo vivo sin inversión, en dos semillas, y en px0, son **idénticos**. Ninguno de los montajes que
     divergen está en el examen.
4. **T-R cuenta la actuación en toda la corrida.** La pieza gobierna A antes de invertir y B después, así que su cláusula de actuación
   se cumple casi seguro. T-R exige, en la práctica, T-C (ii) con la pieza encendida.
   - Separar la telemetría antes y después de la inversión sería un cambio de sólo lectura en `organismo_v144bcal`. No se hizo: el
     encargo era “todo lo demás idéntico”.
5. **La puerta de conteos castiga comer menos** (sec. 5). Es la misma familia que la cláusula “come ≥ 0.8 × tronco” de 7.6 del examen
   de v14.4. Ahora cae en T-C (ii), donde la pieza sí actúa.
6. **El examen no ve 3T-k** (como en v14.4). Aquí es menos grave: `organismo_v144b` con sus defectos es v14.3 en la física (arnés (I)).
   Si PASA, correr 3T-k con la pieza portada antes de congelar.
7. **Memoria nueva** respecto de v14.3: sí (la de TERMO, ahora de un solo bocado).

## 8. Semillas NUEVAS (`busca_semillas_v144b.py`, 28-sep-2026; salida en `busca_semillas_v144b_salida.txt`)
| papel | serie | réplica |
|---|---|---|
| examen v3′ y T-B | 49001–49020 | 49021–49040 |
| mundo vivo T-A (+ CTRL) y T-C (ii) | 49101–49180 (TRONCO_B 149101–149180) | 49201–49280 (TRONCO_B 149201–149280) |
| T-D ALIAS (primeras 9 con \|D∩B\| = 3) | 49449 49492 49509 49528 49563 49597 49621 49652 49718 (rango 49401–49999) | 50004 50054 50181 50208 50212 50235 50250 50294 50296 (rango 50001–50600) |
| T-D LIMPIAS (primeras 9 con \|D∩B\| = 0) | 49407 49418 49431 49444 49450 49451 49457 49464 49466 | 50001 50005 50008 50011 50019 50020 50030 50031 50040 |
| reserva del mundo vivo | 49301–49380 (TRONCO_B 149301–149380) | |
| humo / identidad / práctica del carro | 49041–49043 (+ la ALIAS histórica 326) / 49045–49047 / 49091–49094 | |

- La búsqueda recorrió 9 745 archivos de texto (en la nube, `/home/user` = el repo; en el PC hay que re-correrla sobre `PROYECTOS/JUACO`).
- Rangos buscados: 49000–50600 y 149000–150600.
  - En `.py` y `.md` sólo aparecen fragmentos de sha, sellos de hora y `50000`.
  - En contexto de semilla aparecen: los JSON del propio arnés (49045 y 49046), `50000` en `juaco_eco` y nombres de archivo con sello
    de hora (1500xx–1504xx).
- **50000 se excluye** (es T/2 en medio repo). La regla 14 (R6) lo comprueba y exige además TRONCO_B dentro de 149001–149999.
- El rango propuesto por el coordinador era 49001–50600: los ALIAS salen ~1 de cada 45 semillas, así que T-D de la réplica necesita
  50001–50600.

## 9. Las cuatro trampas
1. **Canal simétrico:** no hay canal. En T-G el control es TERMOINV.
2. **Acierto sin balancear:** G1/G2 de T-B son balanceados; T-G y T-R se miden en `r`, en `rev` y en conteos de actuación.
3. **El mundo que se come la comida:** es parte del mecanismo **y el riesgo principal** (sec. 5, 7.5). Se reportan `vis[A]`/`vis[B]` por
   cuarto al lado de `rev`, las muertes por necesidad y la telemetría de la pieza.
4. **Sitios fijos:** el mundo vivo repone en posiciones sorteadas.

## 10. Procedimiento de congelado si PASA (lo decide el director)
Es el de PREREGISTRO_examen_v144 sec. 10, con v144b:
- 3T-k con la pieza antes de congelar;
- copiar byte a byte `organismo_v144b.py`, `organismo_v144bg.py`, `bateria_v144b.py` y `bateria_generaliza_v144b.py` a `organismo/`,
  con sus shas;
- el bloque de CONGELADOS lo pega el director;
- regla 1 nueva: `cd organismo && python bateria_v144b.py 6 && python bateria_generaliza_v144b.py organismo_v144b 20 --desde 101`;
- tag `v14.4b-tronco`.

## 11. Comandos y costo (sólo el coordinador; los agentes no corren `--serie`, ERR-115)
Antes de cada serie el runner corre el arnés (se para si no da 151/151), la regla 14 (44/44) y la selección de T-D.
- Serie: `python experimentos/tronco_v14_4b_examen/corre_examen_v144b.py --serie --pool 6` (nube: `/root/venv-juaco/bin/python`, `--pool 3`).
- Réplica: `… --replica --pool N --con experimentos/tronco_v14_4b_examen/datos/examen_v144b_serie_<sello>.json`.
- Bloque: `… --bloque <serie.json> <replica.json> [<reserva.json>]`. Reserva: `… --reserva --sustituye serie|replica --pool N`.
- Arnés del carro (muro): `python experimentos/tronco_v14_4b_examen/identidad_termob.py`.
- **Costo por serie: 1 476 corridas**, como en v14.4. La serie de TERMO tardó **40 min con Pool 6** en el PC (`serie_pool6.log`, 2 402 s).
  La estimación de la nube (Pool 3) está en la sec. 12.

## 12. Arnés y humo (UN proceso) — escrito DESPUÉS de sec. 1–11 (28-sep ~20:05). Nada de esto cambió una predicción ni un umbral
**Arnés `identidad_v144bex.py` → RESULTADO 151/151** (100 s; `identidad_v144bex_salida.txt`; JSON
`datos/humo/identidad_v144bex_20260928_195543.json`):
- (0) 10/10 · (A) 15/15 · (I) 16/16 · (T) 12/12 · (V) 4/4 · (P) 9/9 · (L) 3/3 · (D) 6/6 · (R) 44/44 · (J) 16/16 · (K) 16/16.
- **La primera corrida dio 147/151** (JSON `…_195252.json`, que se conserva). Dos fallos fueron del instrumento del arnés:
  - (J) comparaba la T-G del examen de v14.3, que era **otra** T-G;
  - la T-G de v14.4 aplicada a sus crudos no se compara.
- Los otros dos son el **hallazgo 7.3**: en una necesidad con U = 1.0, TERMO′ ≠ TERMO por un empate de ulp. Se convirtieron en
  comprobaciones de que la primera decisión distinta es **sólo** ese empate: el nivel cae entre los dos umbrales y la media difiere en
  ≤ 4 ulp. No se ajustó nada del organismo.
- **Arnés del carro `identidad_termob.py` → 11/11 PASA** (60 s; `identidad_termob_salida.txt`):
  - V143_TERMOB == V143_TERMO en la física de la pista y en la telemetría de la pieza (9 carros, fundador limpio; s 49091 T 5 000 y
    s 49092 T 20 000);
  - TERMO = 0 == V143 entero;
  - TERMOINV con la tabla que olvida == V143_TERMOINV;
  - la pieza lee `_tmS`, no `_adS`.

**Humo `corre_examen_v144b.py --humo`** (9 s; 6 corridas, 200 000 pasos; `humo_salida.txt`; JSON
`datos/humo/examen_v144b_humo_20260928_200028.json`). **No es dato:**
- regla 14: 44/44.
- T-A CUELLO_MIN s49041, T 20 000: OFF `r` −5 (muertes 19) · CAND `r` +5 (muertes 11; dec 362, a_no 156, a_si 11) · CTRL `r` −11.
- **T-C (ii) CAND s49042, T 20 000:**
  - rev +5; muerde A por cuarto [25, 22, 25, 24] y B [25, 14, 33, 29];
  - `vis` de B en Q3–Q4: 97 y 54;
  - la pieza actúa (a_no 238, a_si 18);
  - memoria final: A [−0.4, 0, 1], B [0.8, 0, 1] (la tabla olvidó). **La pieza actúa en T-C (ii): T-R es medible.**
- T-D CAND ALIAS 326: \|W[sal]\| 0.01, W[veneno] −2.92.
- Examen E2 CAND s49043 (T 100 000, **inerte por (2)**): come B Q4 78; muerde A por cuarto [100, 100, 30, 11] (TERMO en su humo: [80,
  92, 208, 128]).
- Cableado de la etapa 8 con crudos sintéticos: el bueno pasa las ocho; el malo cae T-A, T-B, T-C, T-D, T-G y T-R.

**Duración** (este proceso, en la nube, por corrida de T = 100 000): mundo vivo 4.9 s, T-C (ii) 4.2 s, sal 4.8 s, examen 3.8 s; T-B supuesto
en 7.6 s. **1.9 h de CPU por serie.**
- El runner imprime “nube Pool 3 ~22 min”. Esa fórmula, heredada de v14.4, divide por un factor 1.75 de núcleo “más rápido” que aquí
  **no aplica**: estos segundos ya son de la nube.
- Estimación correcta: **nube Pool 3 ≈ 40 min por serie** (+ arnés ~2 min); **serie + réplica ≈ 1.4 h**. PC Pool 6: ~20–40 min.
