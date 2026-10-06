# PREREGISTRO (CONFIRMATORIO) — BALDWIN EN BLOQUES: la selección construye la PLASTICIDAD (creador Opus, 29-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas). Encargo aprobado por el director (29-sep). Escrito DESPUÉS del arnés de identidad (31/31, números sólo de identidad) y ANTES
del humo y de toda serie. La letra está en código: `corre_baldwin.py`, función `lee()`.

## 1. Hipótesis
BLOQUES (FUNCIONA ×2) fija por selección una regla de rechazo FIJA ("no muerdas si el píxel dice B/D"). Cuando el mundo cambia
(inversión A↔B, C↔D), ese instinto mata: 0/108 linajes con reglas persisten (BLOQUES3, 28-sep), y la selección apaga el olvido
(BLOQUES4–6). Hinton y Nowlan (1987): la plasticidad en vida aplana el valle de dos pasos. Dunlap y Stephens (2009): el aprendizaje
evoluciona si el cambio ENTRE generaciones es alto y la experiencia DENTRO de la vida es fiable. El barrido del 28-sep varió el periodo
absoluto sin controlar periodo/vida, y las reglas no tenían bit plástico.
**H:** si cada regla lleva un gen heredable "plástica", con el periodo de inversión ≈ 10 vidas la selección fija reglas plásticas y
el linaje persiste donde el instinto fijo muere; sin inversión, la selección apaga la plasticidad.

## 2. Mecanismo mínimo y memoria nueva
- **Memoria nueva: 1 bit + 1 float por regla** (`RPL[s, r] = [bit, w0]`). Cero parámetros de aprendizaje nuevos.
- Regla de boca plástica: cuando el cuerpo muerde y la condición de la regla se cumplía al decidir, su peso EN VIDA
  `w ← clip(w + η·(R − w), −3, 3)`, con η = `eta_s` del cuerpo si R > w y `eta_s · aversion` si no. Es la regla de la vía lenta del
  cerebro (lectura directa de la retina) con la MISMA señal R = RV[letra, necesidad] con que aprenden Wp/Wn y Wps/Wns (Rescorla-Wagner
  local; fábrica: eta_s 0.15, aversion 1.0).
- **El hijo hereda el bit y w0 del padre, NO el w aprendido.** La HGT copia bit y w0 del vecino; el banco del vivero guarda w0 y bit.
- Genética del bit con rng PROPIO (no toca el azar de las reglas): una regla insertada es plástica con prob. 0.5; cada regla invierte su
  bit con prob. 0.01 en cada nacimiento. **Base neutra declarada: 0.5.**
- Sólo reglas de boca (acción 0) aprenden. En las demás el bit es neutro. Sólo kit 1 (el de BLOQUES).

## 3. Instrumento y anclas
- `construye_baldwin.py` (sha c9cad63496519fb7) → `motor_baldwin.py` (d0a620d2f5e2605e): 16 anclas desde
  `bloques/opusM/motor_bloques3.py` (21b5ee28d086b3be). Con kit 1, motor_bloques3 es motor_bloques (el de la serie BLOQUES), por la
  cadena de arneses (identidad_bloques2 18/18; identidad_bloques3 10/10).
- Runner `corre_baldwin.py`. **Entrada (regla 14):** cada corrida ES `corre_bloques.corre` (a090b82eae9f1ee3, se importa sin tocarla)
  con el gemelo cambiado. Sólo se agregan `baldwin` (medidas) y `cfg_worker` (la BQ_CFG que registró el motor).
- **Arnés `identidad_baldwin.py`: 31/31, y 34/34 tras la auditoría (sec. 14)** (salida `identidad_baldwin_salida.txt`):
  - A1: FIJO_V sin inversión == corre_bloques.corre(BLOQ_V) con motor_bloques, campo a campo;
  - A2: plast 0 con inversión == motor_bloques3, bit a bit;
  - A3: la vía plástica sin reglas plásticas == plast 0;
  - B: los controles difieren y la pieza actúa;
  - H: sin Lamarck (w0 intacto en 101 vivos, lo aprendido no se hereda; 1665/1665 hijos genéticamente == padre);
  - Q: corte + reanuda == entera;
  - D: determinismo;
  - L: la letra en 7 casos sintéticos;
  - R: banderas y candados.

## 4. Mundo, condiciones y brazos
- ECO w90, carro FABRICA_ECO (hijo ingenuo), genética MUT0 + reglas heredables (kit 1 = BLOQ_V), vivero finito t_corte 100 000.
- **Vida medida:** mediana de `vida_media_muertos_2a` de BLOQ_V en las dos series de BLOQUES = 2289 y 2257 pasos. VIDA = 2270.
- **Periodo de inversión P** (múltiplo de 2000, exigencia de motor_bloques3):
  | condición | P | P/vida |
  |---|---|---|
  | P6k | 6 000 | 2.6 |
  | P22k | 22 000 | 9.7 |
  | P68k | 68 000 | 30.0 |
  | Pinf | sin inversión | ∞ |
- **Brazos:**
  - PLAST_V: candidato; el bit se hereda.
  - FIJO_V: = BLOQ_V, sin bit.
  - PLAST_AZA: el bit se sortea 0/1 al nacer para cada regla; la regla sí se hereda.
  - PLAST_RW0: el bit se hereda, pero el blanco del aprendizaje es RV[letra seudoazar, necesidad]. El peso deriva con la misma magnitud,
    sin la consecuencia. Es un control que puede ganar.
- **Serie:**
  - en P22k, los 4 brazos;
  - en P6k, P68k y Pinf, sólo PLAST_V y FIJO_V.
  - Son 10 brazos × 20 = 200 corridas.
  - Recorte declarado: AZA y RW0 sólo en P22k, por costo.
- **T:** 500 000 (el de BLOQUES) si el costo proyectado por el humo para la serie con pool 2 es ≤ 2 h; si no, 300 000. Esta regla se fija
  ANTES del humo; lo que se elija queda en la sec. 13.
- **Semillas NUEVAS** (grep del 29-sep: 564xx no aparece en .py/.md/.txt de PROYECTOS/JUACO fuera de datos):
  - serie 56401–56420;
  - réplica 56421–56440;
  - arnés 56491–56494;
  - humo 56495.

## 5. Medidas
- **persiste:** linaje vivo en T (`corre_bloques`/`nucleo`).
- **frac_pl (principal):** entre las reglas de boca que discriminan letras de los cuerpos vivos en T, la fracción plástica. Son las reglas
  sobre el píxel del foco cuya condición se cumple en 1, 2 o 3 de las 4 letras. Si no hay vivos o no hay tales reglas, vale None y cuenta
  como "no cumple".
- Descriptivas: frac_pl_boca (todas las de boca), |w − w0| de las plásticas, n_aprende, n_inv, K, t_ext, vida_media_muertos_2a,
  serie temporal `serie_pl`.

## 6. La letra (código: `lee()`)
**Validez (todas; si falla alguna: NO SE LEE):**
- V0: completa (200), sin abortos, T y t_corte correctos, bloqueados 0.
- V1: el ancla FIJO_V_Pinf persiste ≥ 15/20 (BLOQUES reproduce).
- V2: cfg_worker de cada corrida = la del brazo.
- V3: n_inv ≥ 1 en todo brazo con inversión, y 0 en Pinf.
- V4: la pieza actúa (n_aprende > 0 en ≥ 18/20 de PLAST_V_P22k).
- V5 (cambiado por la auditoría H-1, sec. 14): AZA, mediana entre semillas de `frac_pl_ult` en [0.3, 0.7]. `frac_pl_ult` es el último
  dato de `serie_pl` con ≥ 10 reglas discriminantes vivas: el bit ANTES de la extinción, no en T. Si hay menos de 8 semillas con
  dato, V5 **no aplica** (cuenta como cumplida) y el control AZA decide sólo por PB.

**Puertas:**
- **PA rescate:** PLAST_V_P22k persiste ≥ 15/20 y FIJO_V_P22k ≤ 5/20.
- **PB controles:** PLAST_V_P22k persiste ≥ PLAST_AZA_P22k + 5 y ≥ PLAST_RW0_P22k + 5.
- **PD la selección prende la plasticidad:** frac_pl ≥ 0.5 en ≥ 15/20 semillas de PLAST_V_P22k.
- **PE la selección la apaga cuando no paga:** frac_pl ≤ 0.2 en ≥ 15/20 semillas de PLAST_V_Pinf.

**Veredicto:**
- FUNCIONA = PA ∧ PB ∧ PD ∧ PE.
- HAY ALGO MODESTO = (PA ∧ PB) ∨ (PD ∧ PE).
- NO, en otro caso.

Nota de la trampa 2 (acierto sin balancear): la base neutra de frac_pl es 0.5, y PD pide ≥ 0.5, igual que el azar. Lo que PD prueba es
la CUENTA de semillas: con arrastre por linaje la fracción es casi 0 o 1 por semilla, y 15/20 bajo neutralidad tiene p ≈ 0.02. PE
(≤ 0.2) va contra la base.

## 7. Secundarias (no deciden)
- Curva de la mediana de frac_pl por P/vida: 2.6, 9.7, 30 e ∞. D1: con P6k la fracción es mayor que con P68k.
- Pareados:
  - K de PLAST_V contra FIJO_V en cada P;
  - t_ext en P22k;
  - frac_pl de P22k contra Pinf;
  - frac_pl de PLAST_V contra RW0.
- RW0: cuántas semillas llegan a frac_pl ≥ 0.5.
- **frac_pl en el tiempo** (auditoría, punto 3): por brazo plástico, la mediana entre semillas de `serie_pl` cada 50 000 pasos y el
  último dato antes de extinguirse. Separa "la selección nunca prendió el bit" de "el brazo murió con el bit prendido".

## 8. Regla de parada y réplica
- La réplica (56421–56440) se corre sólo si la serie da FUNCIONA o HAY ALGO MODESTO.
- El bloque es el mínimo de las dos (`--bloque`).
- `--serie` y `--replica` se niegan:
  - si el preregistro, el runner, el motor o el constructor no están commiteados y sin cambios;
  - si ya hay un veredicto;
  - si hay carpeta previa sin `--reanuda`;
  - si otro lanzamiento tiene el candado `EN_CURSO.lock`.
- Pool ≤ 2.

## 9. Predicciones (antes del humo y de la serie)
**Del director (la letra):**
- en P/vida ≈ 10, PLAST_V persiste ≥ 15/20 y FIJO ≤ 5/20;
- frac_pl ≥ 0.5 en ≥ 15/20;
- en Pinf, frac_pl ≤ 0.2 en ≥ 15/20.

**Del creador (propias, con rango; se declaran refutadas si caen fuera):**
| # | predicción | rango / p |
|---|---|---|
| C1 | FIJO_V_P22k persiste | 0–3/20 (p de PA-FIJO ≤ 5: 0.90) |
| C2 | PLAST_V_P22k persiste | 0–10/20, mediana esperada ~3 (p de ≥ 15: 0.15) |
| C3 | PLAST_AZA_P22k persiste en el rango de PLAST_V ± 4 (el bit heredable no es lo que rescata) | p 0.55 |
| C4 | PLAST_RW0_P22k persiste | 0–5/20 |
| C5 | FIJO_V_Pinf y PLAST_V_Pinf persisten | 17–20/20 cada uno |
| C6 | frac_pl de PLAST_V_Pinf, mediana | 0.25–0.65: cerca de la base, no ≤ 0.2 (p de PE: 0.25) |
| C7 | K(PLAST_V_Pinf) < K(FIJO_V_Pinf) pareado | ≥ 12/20 |
| C8 | t_ext(PLAST_V_P22k) > t_ext(FIJO_V_P22k) pareado | ≥ 13/20 |
| C9 | D1 (fracción con P6k > P68k) | p 0.45 |

- **Mecanismo de C7:** la regla de rechazo plástica se erosiona cuando muerde veneno teniendo sed (R = 0) o sal teniendo hambre (R = 0).
  Eso es un costo de la plasticidad en el mundo estable.
- **Mecanismo contra C2:** una regla de rechazo con w0 = −3 no vuelve a morder, y por eso no aprende que la letra cambió. Para que la
  plasticidad rescate, la selección tiene que bajar |w0| Y prender el bit: un valle de dos pasos, justo lo que Baldwin dice aplanar.
- **Veredicto esperado:**
  | veredicto | p |
  |---|---|
  | FUNCIONA | 0.07 |
  | HAY ALGO MODESTO | 0.20 |
  | NO | 0.65 |
  | NO SE LEE | 0.08 (incoherente con la letra vieja: ver sec. 14) |

## 10. Qué lo refuta
- "La selección construye la plasticidad cuando el mundo cambia a la escala de ~10 vidas" cae si PLAST_V_P22k no supera a FIJO y a los
  dos controles (PA, PB) y la fracción plástica no se fija (PD).
- Si PLAST_AZA o PLAST_RW0 rinden igual que PLAST_V, lo que ayuda es la plasticidad o el ruido, no su selección.
- Si PD pasa y PE no, la plasticidad es barata y no hay presión para apagarla (lectura: casi neutra).
- **Declarado (auditoría H-3):** PD y PE NO son vías independientes de PA. frac_pl se mide en los vivos en T, así que:
  - PD sólo puede pasar si PLAST_V_P22k persiste en ≥ 15/20, justo lo que pide PA;
  - PE sólo puede pasar si PLAST_V_Pinf persiste en ≥ 15/20.
  La rama (PD ∧ PE) del MODESTO no rescata un linaje muerto. Un brazo extinguido cuenta como "no cumple" en PD y PE; el
  descriptivo en el tiempo (sec. 7) dice si el bit se había prendido antes de morir.

## 11. Las cuatro trampas
1. **Canal simétrico:** el bit es simétrico (inserción 0.5, inversión del bit simétrica). La inversión es simétrica (A↔B, C↔D). La señal R
   es la del propio cerebro (−3/0/+1); no se creó una señal nueva.
2. **Acierto sin balancear:** ver la nota de la sec. 6. AZA mide la base (V5).
3. **Mundo que se come la comida:** tras una inversión, el anillo está lleno de lo que antes no se comía, que ahora es comida: un
   festín para quien cambie. Se declara; K y la composición del mundo quedan en el JSON (`mundo`).
4. **Sitios fijos / letras fijas:** en BLOQUES el instinto por identidad de letra era posible porque el significado era fijo. Aquí la
   inversión rompe justo eso, que es el punto del experimento.

## 12. Costo
Medido en el humo; se escribe en la sec. 13, junto con T. Pool 2.

## 13. Humo (después de escribir las secs. 1–12; semilla 56495, T 200 000, un proceso, 6 corridas; `humo_salida.txt`)
- Carpeta `datos/humo_s56495_T200000_20260929_121431/` (resumen sha b565113eeb6993fe). 0 abortos; la validez V0–V5 pasa en modo humo.
- **Costo medido (un proceso):**
  - FIJO_V_Pinf persiste: 16.1 s a T 200 000, unos 40 s a T 500 000.
  - Las corridas que se extinguen tras el vivero: 12.4–13.4 s.
- **Proyección de la serie (200 corridas, pool 2):**
  - peor caso, todo persiste: 200 × 40 s ≈ 8 000 s de CPU → ~67 min de pared (~80 min con contención);
  - caso de 40 persistentes: ~31 min.
  - Cabe en 2 h, así que por la regla de la sec. 4: **T = 500 000** (el de BLOQUES). La réplica cuesta lo mismo.
- **Vida medida en el humo** (`vida_media_muertos_2a`):
  - FIJO_V_Pinf 2097 (consistente con VIDA 2270);
  - en los brazos con inversión, 1235–1523, porque mueren tras el vivero.
- **Números del humo (n = 1; NO cuentan):**
  | brazo | persiste | t_ext |
  |---|---|---|
  | FIJO_V_Pinf | 1 (K 36.4) | — |
  | PLAST_V_Pinf | 0 | 105 844 |
  | PLAST_V_P22k | 0 | — |
  | FIJO_V_P22k | 0 | — |
  | PLAST_AZA_P22k | 0 | — |
  | PLAST_RW0_P22k | 0 | — |
  - En P22k los cuatro brazos mueren poco después de t_corte 100 000. La pieza actúa: n_aprende 2 294–22 437.
- **Aviso, no enmienda:** en el humo, PLAST_V_Pinf murió de hambre y sed (causas_2a [0, 0, 42, 32]) sin fijar el órgano de rechazo. El
  banco quedó con reglas de patas y parto; FIJO_V_Pinf, en la misma semilla, fijó "pixF1 < θ → boca −". Con una semilla no se lee.
  Si se repite en la serie, C5 y V1 no caen (V1 es FIJO), pero PE no puede pasar (frac_pl None). **Las predicciones de la sec. 9 NO se
  cambian.**

## 14. Cambios por auditoría antes de datos (29-sep; auditor: LISTO CON CAMBIOS; sin serie corrida)
- **H-1, V5:**
  - Antes V5 medía frac_pl de AZA en los vivos en T. Ahora se mide sobre `serie_pl`: el último dato con ≥ 10 reglas discriminantes,
    antes de la extinción (sec. 6). El mínimo de 10 reglas se agregó tras el humo, porque con 1–2 reglas el último dato vale 0 o 1 (0.0
    en el humo); no mira ninguna puerta.
  - Con < 8 semillas con dato, V5 no aplica y decide PB.
  - **Se declara:** mi p 0.08 de NO SE LEE era incoherente con la letra vieja. Yo mismo predecía que AZA muere (C3). Con AZA extinto,
    frac_pl en T es None y la V5 vieja fallaba, así que NO SE LEE era muy probable, no 0.08. Con la V5 nueva, p(NO SE LEE) ≈ 0.08
    queda como estimación, sin cambiar las demás.
- **H-3:** PD y PE dependen de la persistencia (sec. 10).
- **Punto 3:** descriptivo frac_pl en el tiempo (sec. 7; `frac_pl_t`, `frac_pl_ult` en el bloque `baldwin` del JSON).
- **H-5:** `EN_CURSO.lock` se crea con `os.open(O_CREAT | O_EXCL)`. Con `--reanuda` se borra el candado viejo y se vuelve a crear en
  exclusiva. Se agregó `.gitignore` (datos/**/ckpt/, datos/arnes/*/ckpt/, __pycache__/).
- **Arnés rehecho: 34/34** (`identidad_baldwin_salida.txt`). Nuevo:
  - 2 casos de la letra: V5 no aplica con 7 semillas con dato → FUNCIONA; V5 aplica con 8 y fracción 0.95 → NO SE LEE;
  - el candado exclusivo.
- **H-2, humo principal repetido con el runner final** (corre_baldwin 76e4c496fa42f4d5):
  - `datos/humo_s56495_T200000_20260929_122926/`, resumen sha ab30737f679f7ae4, `humo_salida.txt`.
  - Números idénticos al primer humo (el determinismo vale).
  - Validez V0–V5 OK; veredicto de humo NO (no cuenta).
  - frac_pl en el tiempo en PLAST_V: 1.0 a 50k y 1.0 a 100k, en P22k y en Pinf, y después se extinguen. Último dato de AZA: 0.51.
  - El primer humo (runner viejo) quedó en `humo_salida_v0_runner_viejo.txt` y `datos/humo_s56495_T200000_20260929_121431/`.
- **H-6, la vida corta de PLAST_V sin inversión (125–171 pasos). Diagnóstico: NO es un bug; es la firma de un linaje que colapsa al
  acabarse el vivero, y aparece igual en FIJO.**
  - **Revisión de código:**
    - (a) w NO arranca en 0: `_instala_pl` pone el peso en vida = w0 heredado. El arnés A3 prueba que la vía plástica sin reglas
      plásticas == BLOQUES bit a bit, y H0 que las reglas no plásticas conservan w == w0.
    - (b) La dirección es la correcta: el blanco es la R de la mordida. En el arnés H, con 2 reglas forzadas en w0 = 0, tras 4
      inversiones la de B/D queda en −0.53 y la de A/C en +0.32, que es el signo del significado vigente.
    - (c) No cuesta energía ni azar del mundo. El único costo es de conducta: una regla de rechazo plástica se erosiona hacia R = 0 si
      muerde veneno con sed o sal con hambre (C7).
    - `vida_media_muertos_2a` promedia sólo los nacidos después de T/2 que murieron. En un linaje extinto son los últimos hijos del
      colapso, que mueren de hambre y sed.
  - **Segundo humo DECLARADO** (no cuenta; semillas nuevas 56496–56498; PLAST_V_Pinf y FIJO_V_Pinf; T 200 000; un proceso, 6 corridas;
    runner 3fa74976724c0fce, que difiere del final sólo en V5; `humo2_salida.txt`; `datos/humo2_s56496-56498_T200000_20260929_122308/`,
    resumen sha 23a78dd17b66038d):
    | semilla | PLAST_V_Pinf | FIJO_V_Pinf |
    |---|---|---|
    | 56496 | muere (vida 150, r0_nac 0.10, hambre/sed 34/21) | persiste |
    | 56497 | persiste (K 35.9) | persiste (K 35.2) |
    | 56498 | persiste (K 38.9) | **muere (vida 272, r0_nac 0.13, hambre/sed 51/59)** |
    - Con los dos humos: PLAST_V_Pinf persiste 2/4 y FIJO_V_Pinf 3/4.
    - La firma "vida corta, muertes por hambre y sed, r0_nac bajo, más refundaciones" aparece también en FIJO (s56498). Es el linaje que
      no fijó el órgano de rechazo antes de t_corte, no la plasticidad.
    - PLAST_V sin inversión NO muere siempre, así que no hay defecto de diseño que invalide PE.
  - **Queda declarado un riesgo real:** con 4 semillas, la plasticidad podría bajar algo la persistencia sin inversión (2/4 contra 3/4;
    no se lee). Si en la serie PLAST_V_Pinf persiste poco, PE no puede pasar (H-3). Eso sería un resultado, no un fallo del
    instrumento.
- Las predicciones de la sec. 9 no se cambian.
