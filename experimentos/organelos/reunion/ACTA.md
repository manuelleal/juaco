# ACTA de la reunión — PASAJES SERIADOS (28-sep-2026; Fable moderadora, Opus A ECO, Opus B pista). EXPLORATORIO, sin commits.

Escrita 19:00 (reloj del PC) por cierre forzado de la moderadora; contiene todo lo que había a esa hora. Opus A y Opus B AGREGAN sus números
finales en la sección 6 (sólo agregar). Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación,
peldaños preregistrados con controles que pueden fallar y réplicas). Principio del director: que la evolución construya el órgano.

## 1. VEREDICTO EXPLORATORIO (una línea)
**HAY SEÑAL en un pasaje, NO HAY SEÑAL de acumulación entre pasajes:** transferir los vivos baja ~30–35 % los fundadores repuestos ya en el
pasaje 1 (5/5 juguete, 3/3 Opus A) y lo sostiene 20 pasajes; ni un pasaje más lo baja más (plano p1→p20), y el control con G0 fresco llega
al mismo techo dentro de cada pasaje de 50k. El techo lo pone lo que el organismo puede variar (nube: MC > C 20/20), no el tiempo.

## 2. Qué se probó
- Esquema (CANAL 18:41): cadenas de pasajes cortos; al final de cada uno, muestra AL AZAR de los genomas VIVOS (sin juez) siembra el
  siguiente con la mutación de siempre. Control: los mismos pasajes sembrados con G0/la inicial (sin herencia entre pasajes).
- Opus A, ECO (reunion/opusA/, arnés 13/13, PREREGISTRO_pasajes.md antes del humo): base ING (FABRICA_ECO, hijo ingenuo, vivero
  permanente), T_p 50 000 × 20 (= 1e6 acumulado), semillas 47801–47805, brazos PAS_SEL (15 genes), PAS_RES (G0 mutado una vez),
  PAS_AZA (sin herencia dentro), PAS_SELM (15 + rep_umbral), PAS_F1 (referencia). Medida: fund_2a (repuestos en [T_p/2, T_p]),
  r = fund_2a/F1 − 1, K, K_nac, genes.
- Opus B, pista (reunion/opusB/, arnés 24/24, PREREGISTRO_pasajes_pista.md 18:52): V143_PAS = V143 + g (termostato) + 15 genes POR CUERPO,
  heredables padre→hijo; T 25 000 × 10, cadenas c1–c4 (semillas 58300+10c+p), brazos pas / ctl (inicial cada pasaje) / pasg (sólo g) /
  termo / o1. Refundador dentro del pasaje p ≥ 1 sale de la siembra del p−1. Luego "prueba del muro" T 100k con la siembra del p9 (5839x).
- Fable, juguete (reunion/fable/pasajes_juguete.py, lee_juguete.py, juguete_*.json): ECO ING, CEREBRO, T_p 20k × 10 (47004–47008) y 50k × 8
  (47001–47003); SEL (vivos → 90 fundadores con reposición), RES (G0), BAR (RESORTEO: genes barajados entre cuerpos).

## 3. Números por pasaje
**Juguete T_p 20k, 5 semillas, mediana (SEL / RES; pareado):** p0 K 97.4 = 97.4, fund_2a 2555 = 2555 (identidad) · p1 K 103.8 / 98.2 (5/5),
fund_2a 1647 / 2548 (5/5, −35 %) · p3 103.5 / 97.8 (5/5), 1661 / 2501 · p5 102.4 / 99.0 (5/5), 1713 / 2492 · p7 102.3 / 97.2 (5/5), 1847 / 2498 ·
p9 101.5 / 97.2 (4/5), 1758 / 2508 (5/5). Genes SEL: alpha 1.67 → 2.18, tau_e 0.73 → 0.56, dist_G0 0.11 → 0.23; RES plano (alpha 1.2–1.4).
**Juguete T_p 50k, 3 semillas:** K SEL < RES 0/3 en p1–p7 (RES 104–105 con K_nac 22–25: auge transitorio de G0 en [25k, 50k]); fund_2a
4135–4367 vs 4101–4514 (SEL<RES 1–3/3). **RESORTEO (BAR) vs SEL:** iguales (K SEL>BAR 2/5…5/5…2/5; fund_2a ~1700 vs ~1700 a 20k; 1–2/3 a 50k).

**Opus A, ECO T_p 50k (r = fund_2a/F1 − 1; s47801 / s47802 / s47803, hasta 18:58):**
- PAS_SEL: p1 −0.30 / −0.37 / 4667 · p2 −0.34 / −0.37 · p4 −0.33 / −0.39 · p8 −0.29 / −0.34 / 4560 · p12 −0.30 / −0.34 · p16 −0.27 / −0.39 ·
  p20 −0.32 / 3838. alpha 2.47 → 3.95 (s47801), tau_e 0.67 → 0.28; K 103.5 → 99.7; K_nac 21.5 → 13.8.
- PAS_RES (control): p1 −0.30 / −0.37 · p4 −0.35 / −0.35 · p8 −0.29 / −0.29 · p12 −0.26 / −0.31 · p16 −0.31 / −0.25 · p20 −0.30. alpha plano 1.5–2.5.
- PAS_SELM (16 genes): p1 −0.34 / −0.26 · p4 −0.34 / −0.32 · p8 −0.26 / −0.21 · p12 −0.33 / −0.26 · p16 −0.33 / −0.35 · p20 −0.27; rep_umbral
  0.99 → 0.89 (s47801), 0.99 → 0.62 (s47802): el margen sube por selección; K 101–108, K_nac 16–27 (más alto que SEL en s47802/03, descriptivo).
- PAS_AZA (sin herencia dentro): p1 −0.05, p2 +0.06, p3 +0.03, p4 0.00, luego −0.13…−0.37 (ruidoso); K_nac 7–21. PAS_F1: fund_2a 6240–6542 estable.
- Pasaje entero (REP, s47801, CANAL 18:52): SEL −17 % p1 → −34 % p2 → −28 % p16; RES −13…−22 %: la herencia entre pasajes AHORRA el transitorio.

**Opus B, pista T 25k (hasta 18:58):** p0 pas == ctl bit a bit en c1–c4. c1 p1: pas R0 0.19, cruzan 1/9, fund [1,17,0,19,1,11,60,1,16],
g_siembra 0.047; ctl R0 0.18, 0/9, fund [0,22,0,0,1,8,0,6,57], g 0.014; pasg 0.09; termo 0.875 (4/9); o1 p0 0.75. Techo del R0 real a T 25k
≈ 0.89 (ERR de Opus B, 18:53): por pasaje manda FUNDADORES POR LINAJE. Los pasajes p2–p9 y la prueba del muro: sección 6.

**Nube (coordinador 19:05, parcial, eco_sel_largo):** L (T 1e7) → NO, K techo antes de 1e6 (cambio −0.02); MC > C 20/20, +2.84 cuerpos.

## 4. Errores de instrumento declarados
- Fable: grep de semillas de las 18:50 miró sólo dos carpetas; 47201–47280 estaban usadas (Opus A lo cazó; usó 47801–47805). Mis 4700x
  aparecen en dos logs viejos de datos/ (no como semilla ECO); juguete, declarado.
- Fable: la ventana [T_p/2, T_p] con G0 fresco cae en un TRANSITORIO que depende de T_p (K_nac RES 15 @20k, 22–25 @50k, 12.6 @1e6). El control
  G0 no es base estable en K; en fund_2a sí discrimina a 20k. RESORTEO no discrimina (SEL ≈ BAR): NO ponerlo de puerta.
- Opus A: reloj (dos sellos adelantados). Opus B: arnés v1 falló por el nombre del carro en 'id' (v2 normaliza; salida v1 guardada); techo del
  R0 real a T 25k. Los sellos de hora del CANAL de los Opus hasta ~18:48 van adelantados respecto del reloj del PC.
- Vocabulario: nada de "evoluciona" sin medida. Permitido: "la transferencia de vivos baja ~30–35 % los fundadores repuestos desde el
  pasaje 1 y no baja más en 20 pasajes"; "más genes mutables (SELM) suben K_nac en 2 de 3 semillas (descriptivo)".

## 5. Qué merece preregistro y nube esta noche
- NO merece nube "más pasajes de lo mismo": la acumulación entre pasajes no aparece en tres instrumentos (juguete, Opus A, nube L).
- SÍ merece (si Opus B lo confirma en la sección 6): la PRUEBA DEL MURO con la siembra del último pasaje (g + 15 genes) contra ctl/TERMO/O1,
  T 100k, cruza_real, fundadores por linaje. Es la única vía en que los pasajes tocan el muro (la palanca es el establecimiento).
- SÍ merece, en ECO: PAS_SELM vs PAS_SEL (16 vs 15 genes) con 20 semillas y réplica, medidas K_nac y fund_2a pareadas en p4 y p8 (T_p 50k):
  es lo que la nube MC señala (más genes = techo más bajo) y en el PC va 2/3 en K_nac. Predicción de Fable: SELM < SEL en fund_2a ≥ 15/20, p 0.35.

Encargo de nube (comandos; rama nueva nube/pasajes-20260928 desde organelos; Pool 3 = tres cadenas a la vez, una por proceso; ANTES de todo,
grep de 4781x–4785x en todo el repo, bundle y carrera incluidos):

    cd experimentos/organelos/reunion/opusA
    python corre_pasajes.py --humo
    for s in $(seq 47811 47830); do python corre_pasajes.py --cadena PAS_SEL  --s $s --n 8 --T 50000; done
    for s in $(seq 47811 47830); do python corre_pasajes.py --cadena PAS_SELM --s $s --n 8 --T 50000; done
    for s in $(seq 47811 47830); do python corre_pasajes.py --cadena PAS_F1   --s $s --n 8 --T 50000; done
    python corre_pasajes.py --lee            # réplica en 47831–47850 si la serie no da NO
    cd ../opusB && python corre_pas.py --humo
    for c in 5 6 7 8 9; do python corre_pas.py --cadena $c --npas 10 --T 25000 --brazos pas,ctl,termo,o1; done
    # prueba del muro: el comando exacto lo agrega Opus B en la sección 6 (T 100000, siembra del p9 fija, semillas 5839x)

Preregistro antes de la serie: predicción numérica con p; puertas (ECO: SELM < SEL en fund_2a ≥ 15/20; pista: fundadores por linaje pas < ctl
≥ 15/20 y R0 real pas vs TERMO pareado); validez (p0 pas == ctl; F1 en rango 6 200–6 600); control G0/inicial. Siguiente ERR libre: ERR-153.

## 6. Agregados de los Opus (sólo agregar, con hora del PC)

### 6.A — Opus A (ECO), agregado 19:50 (reloj del PC). EXPLORATORIO.
**Veredicto:** NO para SEL (los pasajes seriados no bajan los fundadores más allá de la corrida larga, ni más rápido: la igualan) ·
HAY ALGO MODESTO para AZA (sin herencia dentro del pasaje, la transferencia de los VIVOS es selección por supervivencia: baja los
fundadores de −3 % a −13/−22 % y mueve alpha/tau_e al mismo sitio que SEL; no llega a SEL y deriva mucho entre pasajes).

Medida: r_rep = fundadores repuestos en el pasaje ENTERO / los de PAS_F1 (misma semilla y pasaje) − 1; mediana de 5 semillas; T_p 50 000.
| brazo (serie 47801–05) | p1 | p2 | p8 | p20 | p21–25 | p36–40 | acum. 1e6 (p1–20) | acum. 2e6 (p1–40) | alpha p1→p20 | tau_e p1→p20 |
|---|---|---|---|---|---|---|---|---|---|---|
| PAS_SEL | −17 | −35 | −31 | −33 | −33 | −34 | −32.0 % | −32.6 % | 1.86→4.07 | 0.74→0.37 |
| PAS_RES (G0 mutado, control) | −17 | −17 | −18 | −17 | — | — | −18.9 % | — | 1.86→1.78 | 0.74→0.68 |
| PAS_SELM (15 + rep_umbral) | −14 | −35 | −26 | −31 | — | — | −27.4 % | — | 1.87→4.55 | 0.72→0.35 |
| PAS_AZA (sin herencia dentro) | −3 | −9 | −19 | −23 | −13 | −16 | −13.0 % | −11.4 % | 1.45→4.14 | 0.85→0.33 |
| réplica 47811–15: SEL / RES / AZA | −18 / −18 / +1 | −35 / −18 / … | −31 / −18 / −6 | −30 / −17 / −19 | — | — | −29.8 / −18.1 / −8.5 % | — | 1.91→4.53 (SEL) | 0.72→0.31 |
Corrida larga ECO_SEL_ING (1e6): SEL −31.6 % (serie) / −30.6 % (réplica); AZA −5 %. En la 2a mitad de cada pasaje (fund_2a) SEL ≈ RES
(−29..−36 % ambos): dentro de un pasaje de 50k desde G0 ya se llega al techo; lo único que da la herencia entre pasajes es ahorrar el
transitorio (REP del pasaje entero SEL < RES 5/5 en p2–p20, serie y réplica). SEL: mejor pasaje p2 (−35 %) en serie y réplica.
Tendencia (media r_rep p16–20 − p1–5, por semilla): SEL 4/5 serie, 1/5 réplica (contra p2–5: 2/5, 1/5) → no acumula. AZA 4/5 serie,
5/5 réplica → acumula algo hasta p20; p21–40 (serie) vuelve a −2..−16 % por bloque: deriva (muestra de 90 de ~100 vivos por pasaje).
**Predicciones (PREREGISTRO_pasajes.md):** Q1, Q2, Q3, Q5, Q9 dentro. **Refutadas: Q4** (SEL<RES en fund_2a en p8: 3/5 y 1/5; sí 5/5 en
el pasaje entero, que no era la medida firmada), **Q6** (AZA p8 −19 %, fuera de [−10, +5]), **Q7** (r ≤ −0.325 en p8: 2/5 y 0/5), **Q10**
(SELM no baja más que SEL). **Q8** mixta (p20 −0.357 serie, −0.297 réplica).
**Errores de instrumento míos:** (1) sellos de hora del CANAL adelantados hasta ~18:48; (2) el preregistro firmó fund_2a (2a mitad) como
medida principal y la señal de herencia está en el pasaje entero (REP): lo digo, no lo cambio; (3) corre_pasajes.py se editó tres veces
tras el primer arnés (guarda de semillas ×2, --continua con su caso (C)); la cadena no cambió (arnés (D)/(C)); arnés final 14/14
(sha 858c2ae30293203b; salida f059e2f0a29f66b8); las corridas de p1–p20 se hicieron con la versión b72a2f0f3a5413a9 (misma lógica).
(4) vivos_final viene redondeado a 6 decimales: la transferencia recorta a [lo, hi] (declarado en el preregistro). (5) la extensión
p21–p40 no estaba en el plan (sólo serie; misma regla).
**Para la nube (§5):** las semillas 47811–47830 del comando CHOCAN con mi réplica (47811–15) y con la guarda del runner. Usar serie
47851–47870, réplica 47871–47890 (guarda ya ampliada; grep 19:26 limpio). Mi recomendación: NO a "más pasajes de SEL" (40 pasajes no
bajan de −33 %). SELM vs SEL con 20 semillas sólo si se quiere cerrar la pregunta de Fable; aquí SELM ≥ SEL en 4 de 5 bloques.
Archivos: reunion/opusA/{PREREGISTRO_pasajes.md, construye_pasajes.py, nucleo_pasajes.py, corre_pasajes.py, identidad_pasajes.py,
identidad_pasajes_salida.txt, tabla_pasajes.py, tabla_T50000_{serie,replica}.txt, tabla_pasajes_T50000_{serie,replica}.json, humo_salida.txt};
datos/pas_<brazo>_s<s>_T50000/ (137 MB en total: JSON por pasaje; decidir qué se versiona). Genomas del último pasaje (90 × 18, con
nombres): datos/pas_PAS_SEL_s<s>_T50000/genomas_ultimo_PAS_SEL_s<s>.json (s 47801–05 a p40; 47811–15 a p20), ídem PAS_SELM y PAS_AZA.

### [20:55] Opus B (pista) — FINAL. Veredicto: HAY ALGO MODESTO (exploratorio): los pasajes llevan g sola de la zona letal al nivel de TERMO. NO cruza el muro.
Carpeta `reunion/opusB/`. Carro `V143_PAS` (construye_pas.py db39a136…, por anclas desde V143_EVO_BAJO 3187b373…): g + 15 genes del cerebro
por cuerpo; fundadores de la SIEMBRA = (g, cerebro) de los VIVOS de los últimos 5k pasos del pasaje anterior (sin juez). Arnés
`identidad_pas_salida.txt` 24/24 (v1 falló sólo por el nombre en 'id', declarado). Runner corre_pas.py 49322105…; resúmenes
`lee_cadenas_salida.txt` y `lee_muro_salida.txt`.
**Cadenas** (c1–c4, T 25k × 10 pasajes, semillas de pista 58300+10c+p; mediana de cadenas; R0 real aplastado por T corto, techo ~0.89):
| p | pas R0 · g | ctl R0 · g | pasg (sólo g) R0 · g | TERMO R0 | O1 R0 |
| 0 | 0.34 · 0.030 | 0.34 · 0.030 (== pas bit a bit, 4/4) | 0.21 · 0.037 | 0.71 | 0.75 |
| 3 | 0.48 · 0.125 | 0.09 · 0.015 | 0.28 · 0.093 | 0.59 | 0.71 |
| 5 | 0.70 · 0.149 | 0.06 · 0.039 | 0.58 · 0.121 | 0.53 | 0.67 |
| 9 | 0.61 · 0.245 | 0.21 · 0.037 | 0.67 · 0.195 | 0.75 | 0.74 |
pas>ctl 28/28 pares (c, p≥3), +0.58; pas vs pasg 14/28 (el cerebro no suma). g de los vivos SUBE en 10 pasajes sin techo (c4 0.34):
aquí SÍ hay acumulación entre pasajes (en ECO no), porque el refundador ya no vuelve a U[−0.1, 0.1]. Fundadores/linaje (media, p5–p9):
pas 19.2, ctl 12.9, TERMO 32.1, O1 14.2: NO bajan, suben (mediana 2 vs 5; establecidos 6.5 vs 5).
**Prueba del muro** (T 100k, letra del muro, siembra FIJA del p9 de cada cadena; 12 semillas 58391–58398, 58401–58404; n < 20: no es la letra):
| brazo | R0 real | mayorías que cruzan | linajes que cruzan | fund/linaje media · mediana |
| pas (g + cerebro) | 0.805 | 2/12 | 46/108 | 86.4 · 6 |
| pasg (sólo g) | 0.853 | 5/12 | 46/108 | 75.8 · 5 |
| TERMO (g 0.40 diseñado) | 0.926 | 7/12 | 56/108 | 115.4 · 1.5 |
| O1 | 0.950 | 12/12 | 88/108 | 8.1 · 0 |
| v143 | 0.619 | 0/12 | 28/108 | 186.0 · 17 |
| ctl | 0.387 | 0/12 | 24/108 | 55.1 · 26 |
| eco (cerebro ECO de Opus A, g inicial) | 0.311 | 0/12 | 22/108 | 54.8 · 35.5 |
Pareados: pasg>v143 12/12 (+0.26) · pasg>ctl 12/12 (+0.42) · pasg vs TERMO 6/12 (0.00) · pas>v143 10/12 (+0.17) · pas>ctl 11/12 (+0.30) ·
pas vs TERMO 5/12 (−0.03) · pas vs O1 1/12 · eco vs ctl 4/12 (−0.14).
Lectura: la selección entre pasajes CONSTRUYE el termostato (g 0.03 → ~0.2) y el bicho queda donde TERMO sin constante de diseño; el cerebro
(evolucionado aquí o en ECO) no ayuda en la pista. El muro no cae: la palanca (fundadores por linaje) no se mueve, igual que con TERMO.
No hay señal clara (fundadores no bajan, R0 < 0.90): NO dejo esqueleto del intento #7.
Errores de instrumento (míos): arnés v1 (id); techo del R0 real a T 25k; la prueba del muro NO tuvo predicciones numéricas firmadas antes
de correr (sólo anunciada en el canal 18:53); dos logs de humo del modo --muro quedaron en datos/c1_*/ (193124 falló por clave 'seed'
duplicada, 193135 T 2000 sembrado; el real es 193151); mis sellos de hora del canal iban ~1 min adelantados.
Predicciones (PREREGISTRO_pasajes_pista.md): Q1, Q2, Q3, Q5, Q9 se cumplen; Q4 y Q7 REFUTADAS (fundadores suben); Q6 no ocurre (como predije);
Q8 falla (TERMO/O1 a 25k por debajo del rango: el techo de T corto).
Nube, si el coordinador lo quiere (NO es el muro; sería "la selección encuentra el termostato", con preregistro nuevo y semillas nuevas):
    python experimentos/organelos/reunion/opusB/identidad_pas.py
    python experimentos/organelos/reunion/opusB/corre_pas.py --cadena <k> --npas 10 --T 25000 --brazos pasg,ctl        # k nuevas
    python experimentos/organelos/reunion/opusB/corre_pas.py --muro <carpeta de la cadena k> --semillas <s> --brazos pasg,ctl,v143,termo,o1
  (--cadena admite 1..9 y --muro sólo 58391–58398/58401–58408: hay que ampliar las guardas de semillas antes; puertas propuestas:
  pasg>v143 ≥ 15/20 y pasg>ctl ≥ 15/20 por la letra de TERMO.)
