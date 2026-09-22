# PREREGISTRO — EL MUNDO DE LA FASE 10 (diseño y validación). Brazo F0 (Fable solo), 21-sep-2026

**Misión (primera frase, no negociable):** llegar a la AGI por este camino: un organismo mínimo con reglas locales, sin retropropagación, que sube la escalera del brief con cada peldaño preregistrado, medido con controles y replicado. El método manda sobre el cómo.

**Encargo:** `../ENCARGO_mundo_fase10_20260921.md`. **Escribo sólo en `F0_fable_solo/`.** JUACO se lee por ruta absoluta (`C:\Users\User\Documents\PROYECTOS\JUACO\bundle`). Sin Pool, sin commits. Semillas: **2401–2420** (serie) y **2421–2440** (réplica); grep de `s24xx-`, `semillas 24xx`, `desde 24xx` en `experimentos/`, `registro/`, `datos/`: libres. Humo con las semillas 1 y 2, ya vistas (como el humo de la fase 9).

---

## 0. El hecho que manda (leído, no rehecho; §7 del encargo)

Cuatro series de la fase 9 (1501–1520, 1621–1640, 1581–1600, 1601–1620) declaran que el cuerpo recién nacido que lee el nodo por relevancia viva rechaza lo malo al primer encuentro sin dejar de comer y vive ~6× el cuerpo vacío; y que **ni el nodo ORÁCULO cruza R₀ 0.90** (0.508 / 0.557): el muro es el mundo. Lo que este preregistro hace es **cambiar el mundo** y medir si el tronco v14.2, sin una regla nueva, lo cruza.

Lo que encontré leyendo el instrumento (antes de medir nada): en el mundo vivo **`see()` ve el objeto más cercano a cualquier distancia del anillo**; "dónde" es gratis. El mapa del nivel 6 (`mundo_mapa.py`: `r_vis`, tabla M posición → último patrón, sesgo sobre la locomoción sólo con la retina vacía) es el instrumento que ya existe para cobrarlo.

## 1. Hipótesis

**H10 (del encargo):** existe un mundo donde un linaje mortal sólo se sostiene si transmite (R₀ ≥ 1 con nodo + mapa; < 0.5 sin nodo o con nodo barajado) y donde lo transmitido crece (los cuerpos 5.º–12.º explotan ≥ 2× las combinaciones del 1.º), sin cambiar el organismo.

**H10-F0 (la mía, firmada antes del humo formal; la calibración del §3.3 ya la insinúa):** con el tronco v14.2 tal cual, **no**. Dos propiedades del organismo, no del mundo, lo impiden: (a) la boca decide con la fila de valor de la **necesidad activa** solamente (CUELLO_MIN sólo actúa saciado): un cuerpo con la tabla casi perfecta muerde el veneno cuando tiene sed y la sal cuando tiene hambre (medido: 57/63 y 85/259 exposiciones en el mundo F10; 75/83 y 101/508 en el mundo del tronco, `REGISTRO.md` 20:08); en el mundo del tronco lo compensa porque ve todo el anillo y come 1.5–2× más bueno. (b) Con la retina vacía la locomoción casi no se mueve (p ≈ 0.005 + ruido): **no explora**; el mapa sólo devuelve lo ya visto. Un mundo que cobra "dónde" lo mata de hambre; uno que no lo cobra deja el mapa inerte. **Predigo que el ancla V-6 (RENACE 0.80–1.30) CAE y que M10-1 no se cruza en ningún brazo.** Si la serie lo confirma, el resultado es: *para pasar las puertas de la fase 10 hay que cambiar el organismo (ruta de la boca entre necesidades, o exploración), y eso lo decide el director, no este diseño* (§8 del encargo).

## 2. El mundo (§2.1 del encargo, con sus números)

Instrumento `mundo_fase10.py`, construido POR ANCLAS por `construye_mundo_fase10.py` desde `organismo_f9.py` (`3a821884394d66c9`; cadena verificada de 7 shas hasta `organismo_v14.py` `feefc88b1fd8d434`) + 7 donantes con bloques literales verificados (v142 `17528d767fcebaf6` para B-5, `organismo_vivo_codigo.py` `839fa71f9c84cb26`, `organismo_f9c.py` `9dd1fb91ecec35ae` para el ORÁCULO, `mundo_mapa.py` `207d6a1954336b18`, `organismo_v3cal.py` `148014f68cb01785` para el placebo, `organismo_familias.py` `b9dd561a0cf056b8` para la retina `_D`, `mundo_muralla.py` `6e515713c86d8bf4` como patrón de rng propio). 48 anclas documentadas en la salida del constructor. **Memoria nueva del organismo: cero. Regla de aprendizaje nueva: ninguna.** La tabla M es el instrumento del nivel 6 (memoria del individuo; se borra al morir con `muerte_real`; el inmortal la conserva).

| requisito | perilla del mundo (valor) | medida verificable |
|---|---|---|
| 1. Recursos que se agotan y se mueven | `parches=6`, `cap=5` unidades, `regen=30`, `vida_parche=8000` (≤ T/4 = 25 000); sitio y tipo sorteados por semilla con el rng DEL MUNDO `920000+1000000*seed` (ERR-60; patrón de `mundo_muralla`) | **V-1:** estancia máxima de un parche ≤ T/4 en todos los brazos; en MUNDO_FIJO (control) = T−1 |
| 2. Dónde vale tanto como qué | `r_vis=8` (ve 17 de 40 sitios), `usa_M=1`, `olvida_M=1` (percepción de ausencia: donde recordaba algo y no hay nada ni pendiente de reaparecer, olvida), `gamma_M=0.6, H_M=20, disc_M=0.9` (mundo_mapa, literal) | **V-2:** R₀(ORÁCULO_SIN_MAPA) < 1 y R₀(MAPA_SIN_TABLA) < 1 y R₀(ORÁCULO) ≥ 1 |
| 3. Estímulos compuestos | 4 familias (los 4 patrones del tronco, 6 px) × 4 variantes one-hot (4 px) = **16 tipos en 10 píxeles**; los 16 con K=3 sobre 30 celdas hacen alias estructurales inevitables (`alias_nac` se mide) | **V-3:** en REL_D0 (desambiguar=0), tasa de mordida de lo malo con alias ≥ 2× la de lo malo sin alias (mordidas/exposiciones agregadas; exposiciones reportadas) |
| 4. Cambios no avisados | `cambia_cada=5000` (19 cambios en T=100 000): cada cambio, dos tipos del mismo eje con valencia opuesta se la intercambian (balance bueno/malo intacto: trampa 3); cada `cambia_fam=4` cambios, una **familia entera** cambia con la de su eje (el veneno cambia de familia) | **V-4:** cobertura de la tabla al morir (fracción de las 16 celdas (tipo, necesidad informada) con el signo correcto): SIN_HERENCIA mediana < 0.50; REL cuerpos 5..12 > 0.80 |
| 5. Más de un cuerpo | **opción declarada, no medida**: la cola FIFO de descendientes ya existe (`cola_max=200`); nace uno cuando muere el vivo. No se nombra hasta medirla | V-5: sólo declaración |
| 6. Coste de vida | CUERPO campo a campo el de la fase 9 (`costo=costo_a=0.001`, `dote=0.6`, `rep_X=500`, `rep_umbral=1.0`, CUELLO_MIN, rep2, h1; arnés I10) | **V-6 (ANCLA, bloqueante):** R₀ NADA ∈ [0.10, 0.30], R₀ RENACE ∈ [0.80, 1.30] |

**Cuerpo:** tronco **v14.2** (`desambiguar=1`); la cadena viva estaba en v14.1 (`construye_f9.py` lo declara), así que el ancla de la fase 9 se compara con `desambiguar=0` en el arnés (I3) y el ancla del mundo nuevo se mide con v14.2 (V-6). `rep_acum=0` (el nivel del ancla H-1).

### 2.1 Los doce brazos (todos en el mismo mundo salvo MUNDO_FIJO)
RENACE (inmortal con mapa, cota del mundo) · NADA (tronco solo: sin nodo, sin mapa) · SIN_HERENCIA (sin nodo, con mapa) · **REL** (nodo por relevancia + mapa: el candidato) · REL_SIN_MAPA · NODO_BARAJADO (recompensas del nodo permutadas) · ORÁCULO (tabla verdadera + mapa) · ORÁCULO_SIN_MAPA · MAPA_SIN_TABLA (`learn=False`: sin tabla ni locomoción aprendida, declarado) · MUNDO_FIJO (REL sin cambios, parches que ni se agotan ni se mudan: el mundo blando) · PLACEBO (REL consumiendo y descartando un sorteo por paso, `organismo_v3cal` literal) · REL_D0 (REL con `desambiguar=0`: el alias sin reparar). 12 × 20 semillas = 240 corridas de T = 100 000 (~20 s cada una en un núcleo: ~15 min con Pool 7; no hace falta gemelo numba, §4.4 del encargo).

### 2.2 Medidas (todas de solo lectura, `f10=1`)
R₀ = descendientes / (muertes + 1) (H-1); `vida_med`; `fundadores`; por cuerpo que muere: `cuerpo` (índice k en la corrida), `gen` (generación desde la última fundación, fijada al parto), `cob_s` (signo correcto), `cob_c` (|v| ≥ 0.5), `expl` = combinaciones (tipo bueno × cuarto del anillo) mordidas con efecto positivo, `enc` (exposiciones), `pe/pb` (exposiciones/mordidas de lo malo [con alias, sin alias]), `causa` (alias/limpio/drenaje: última mordida mala ≤ 100 pasos antes), `celdas`, `des` (divisiones B-5), `alias_nac/alias_fin`. **"1.ª generación" = el cuerpo 1 de la corrida** (el único que con certeza no leyó nada); **"5.ª generación" = cuerpos 5..12** (mediana): leen lo que dejaron ≥ 4 cuerpos. Con un nodo que no se vacía, el índice del cuerpo es lo que "sabe más": no uso `gen` (se reinicia al refundar).

## 3. Puertas — letra escrita ANTES de correr (`UMBRALES` del runner, ERR-31; una línea por puerta, ERR-89)

| puerta | letra | nulo · margen · n |
|---|---|---|
| **V-6 ANCLA** | R₀ NADA ∈ [0.10, 0.30] y R₀ RENACE ∈ [0.80, 1.30] (medianas, 20 semillas). Si cae, lo demás se REPORTA y no se declara (como F9-1) | rangos del encargo; ERR-93 calibró NADA [0.097, 0.22] y RENACE [0.60, 1.40] con 5 series del mundo viejo |
| V-1 | estancia máxima de un parche ≤ 25 000 en todos los brazos (20/20); MUNDO_FIJO debe fallar | determinista por construcción (vida_parche 8000) |
| V-2 | med R₀(ORÁCULO_SIN_MAPA) < 1 · med R₀(MAPA_SIN_TABLA) < 1 · med R₀(ORÁCULO) ≥ 1 | absolutas |
| V-3 | REL_D0: (Σpb_alias/Σpe_alias) / (Σpb_limpio/Σpe_limpio) ≥ 2.0, con ≥ 20 exposiciones de cada clase; se reporta lo mismo en REL (B-5) | nulo = 1.0; margen ×2 |
| V-4 | med cob_s(SIN_HERENCIA, todos los cuerpos) < 0.50 · med cob_s(REL, cuerpos 5..12) > 0.80 | absolutas |
| **M10-1** | REL: R₀ ≥ 1.0 con fundadores ≤ 2 en ≥ 15/20 · med R₀(NADA) < 0.5 · med R₀(NODO_BARAJADO) < 0.5 | absoluta; 15/20 deja pasar ≥ 0.95 a un candidato con p(semilla) ≥ 0.88 |
| **M10-2** | REL: razón expl(5..12)/expl(1) mediana ≥ 2.0, A₁₂ **pareado por semilla** ≥ 0.85 (fracción de semillas con expl5 > expl1, nulo 0.50), n ≥ 15 semillas con expl1 > 0 · NODO_BARAJADO razón ≤ 1.2 | nulo A₁₂ 0.50; margen 0.35: con n = 20 y p = 0.5 la probabilidad de A₁₂ ≥ 0.85 por azar es 0.001; exposiciones del cuerpo 1 y 5..12 reportadas al lado (trampa 3) |
| **M10-3** | MUNDO_FIJO: razón expl(5..12)/expl(1) ≤ 1.2 | **defecto de letra declarado:** el cuerpo 1 nunca lee el nodo en NINGÚN mundo, así que la razón 5/1 mide "leer el nodo", no "acumular por el cambio". Predigo que CAE por la letra en el mundo blando; propongo (para el coordinador, sin recalibrar) M10-3′: razón cuerpos 5..12 / cuerpos 2..4 |
| M10-4 | identidad bit a bit con perillas apagadas (arnés I1–I2, 12 escenarios × 2 semillas + rng a T = 120 000) e **inercia del mapa** sin `r_vis` (I7): las baterías `bateria_v142` y `bateria_generaliza_v142` corren `organismo_v142.run(seed, **kw)`, así que la identidad de `run` es la identidad de las baterías; el coordinador las corre si quiere el 8/8 impreso. Coste 1.00× por identidad | — |
| M10-5 | se reporta: celdas al morir (REL/NADA/RENACE), divisiones B-5, pares alias (bueno, malo) al nacer y al morir y su diferencia `sep` | — |
| PLAC | \|med R₀ PLACEBO − REL\| ≤ 0.15 · A₁₂(R₀ PLACEBO vs REL) ∈ [0.35, 0.65] · razón M10-2 de PLACEBO / REL ∈ [0.8, 1.25] | el nulo exacto entre los brazos (regla 15); ningún umbral de arriba es igual al nulo (A₁₂ 0.85 vs 0.50; ×2 vs ×1) |

**Refutadores.** H10 queda refutada si V-6 pasa y M10-1 cae en las 20 semillas (el mundo conserva el ancla y aun así el linaje con nodo + mapa no se sostiene). H10-F0 queda refutada si RENACE ∈ [0.80, 1.30] o si REL cruza R₀ ≥ 1 en ≥ 5 semillas. El diseño se declara **inválido** (no la hipótesis) si V-1 cae, si el PLACEBO cae PLAC, si algún control que debe diferir no difiere (arnés), o si la contabilidad H1-8 (`coherente`) falla en alguna corrida.

## 4. Predicciones firmadas (F0, antes del humo formal de 6 corridas; con la calibración del §3.3 a la vista)

| qué | predicción (rango) | prob. de PASAR la letra |
|---|---|---|
| V-6 NADA | 0.05–0.20 | 60 % |
| V-6 RENACE | **0.10–0.40** (fuera del ancla) | **10 %** |
| V-1 | ≤ 8 000 en todo brazo móvil | 95 % |
| V-2 | ORÁCULO_SIN_MAPA 0.05–0.25 (<1 ✓); MAPA_SIN_TABLA 0.0–0.15 (<1 ✓); ORÁCULO 0.05–0.40 (≥1 ✗) | 5 % |
| V-3 | razón 1.0–2.5 | 45 % |
| V-4 | SIN_HERENCIA 0.45–0.60 (la mitad de las celdas se acierta por azar de signo: cob_s del cuerpo vacío ≈ 0.5, **defecto de la medida declarado**; cob_c es la honesta) ; REL 5..12 0.65–0.85 | 25 % |
| M10-1 | REL R₀ 0.05–0.35; 0/20 semillas ≥ 1.0 | **3 %** |
| M10-2 | razón 1.5–4 (los cuerpos 5..12 viven más y exploran más: la razón mide también vida, por eso van las exposiciones al lado); A₁₂ 0.7–0.95; NODO_BARAJADO razón 0.8–1.8 | 35 % |
| M10-3 | MUNDO_FIJO razón 1.5–4 → CAE por la letra | 30 % |
| M10-4 | identidad 100 % | 99 % |
| PLAC | pasa | 85 % |
| **paquete entero** | | **< 2 %** |

Y la que más me importa: **la causa de muerte del inmortal será mayoritariamente 'limpio' (veneno con código no aliasado, mordido con la otra necesidad activa), no 'alias' ni 'drenaje'** (70 %).

## 5. Controles que deben poder fallar (§2.3)
NADA · NODO_BARAJADO · SIN_HERENCIA · MUNDO_FIJO · ORÁCULO_SIN_MAPA · MAPA_SIN_TABLA · PLACEBO · INMORTAL (RENACE) — los ocho del encargo, más REL_SIN_MAPA y REL_D0. Los que **deben** fallar por la letra: MUNDO_FIJO en V-1; NADA y NODO_BARAJADO en M10-1; ORÁCULO_SIN_MAPA y MAPA_SIN_TABLA en V-2. El arnés (`identidad_mundo_fase10.py`) exige que 13 controles **difieran** del candidato (D1–D13).

## 6. Las cuatro trampas (regla 5) y las propias
1. **Canal social simétrico:** el que escribe en el nodo es el cuerpo que muere; el que lee es el que nace (rng propio `700000+…`); nadie se lee a sí mismo. El ORÁCULO no lee lo vivido: lee la tabla.
2. **Acierto sin balancear:** V-3 y M10-2 llevan exposiciones al lado; `p1` y `c1` se reportan juntos (J en el crudo); `cob_s` se reporta con `cob_c`.
3. **El mundo que se come la comida:** los cambios son intercambios (balance bueno/malo constante); las exposiciones por brazo se imprimen en cada puerta; el mismo rng del mundo por semilla en todos los brazos hasta que la conducta los separa.
4. **Sitios fijos que se memorizan:** sitios y tipos de los parches sorteados por semilla (`_rmun`), se mudan cada 8 000 pasos o al agotarse; el ring no tiene geometría; MUNDO_FIJO es el control que los deja fijos.
5. **Propia:** la razón M10-2 confunde "saber más" con "vivir más" (un cuerpo que vive 600 pasos explota más que uno que vive 60): por eso exposiciones y vidas de los cuerpos 1 y 5..12 van en la misma línea, y se reporta `expl_t`.
6. **Propia:** `cob_s` del cuerpo vacío no es 0 sino ≈ 0.5 (signo al azar de una tabla en 0 cuenta como error: `_v9*_s9>0` con `_v9=0` es falso → 0; pero tras dos mordidas la mitad de las celdas se acierta por la vía lenta lineal). Se lee con `cob_c`.

## 7. Fallos pasados que este diseño podría repetir y cómo los evita (ERR-35..93)
- **ERR-35 / regla 4 (recalibrar tras ver datos):** la calibración del mundo (§3.3) tocó perillas del **mundo** antes del humo formal y se declara; ningún umbral de puerta se movió ni se moverá.
- **ERR-37 / ERR-44 (medida que no distingue):** `cob_s` no distingue "sabe" de "acierta el signo por azar": por eso `cob_c` al lado.
- **ERR-38 / regla 14 (perilla muerta, batería copiada con kwargs distintos):** CUERPO y NODO campo a campo contra `corre_f9` (I10); 13 controles que deben diferir; `lect_div` se imprime; `identidad_corta` dentro del runner.
- **ERR-39 (control de paja):** MUNDO_FIJO, PLACEBO y REL_SIN_MAPA son controles que **pueden ganar**.
- **ERR-40 (medida que premia morir):** R₀ = desc/(muertes+1) y r; nunca "rechaza más" sin "sigue comiendo".
- **ERR-41/42 (kwargs y JSON perdido):** humo de un proceso que escribe el JSON antes de la serie; crudo antes del análisis (ERR-54).
- **ERR-45 (cláusula insatisfacible):** V-4 "una vida < 50 %" puede serlo con `cob_s` (≈ 0.5 por azar): declarado arriba; se juzga por la letra y se reporta `cob_c`.
- **ERR-60 (semillas de hijos):** el rng del mundo es `920000+1000000*seed`, fuera de las familias 700000+/800000+/850000+/860000+/870000+.
- **ERR-62 / H-1:** el ancla V-6 está para que la comparación con H-1 valga; si cae, nada se declara.
- **ERR-85/86:** sin Pool aquí; `--pool`/`JUACO_POOL` para el coordinador.
- **ERR-87:** `lee_json` con prefijo + sello exacto. **ERR-89:** una línea por puerta. **ERR-90:** puertas absolutas donde se puede.
- **ERR-91 / regla 15:** PLACEBO entre los brazos; ningún umbral igual al nulo; el A₁₂ pareado de M10-2 se declara con su nulo (0.50) y su margen (0.35).
- **ERR-92:** los rangos del ancla son los del encargo, que ya integró las cinco series (ERR-93).
- **ERR-93 (J balanceado):** `p1` y `c1` en el crudo de cada corrida.
- **Desviación propia, declarada (candidato a ERR):** la calibración usó 50 mini-corridas de un proceso (T = 20 000, ~3 min de CPU), más de las 6 que la regla 3 permite por humo. Todas en `REGISTRO.md` con sus números.

## 8. Humo formal (UN proceso, 6 corridas de T = 100 000: RENACE s1, NADA s1, REL s1, REL s2, ORÁCULO s1, ORÁCULO_SIN_MAPA s1) — predicciones ANTES de lanzarlo
- **HH1 (instrumento, bloquea):** contabilidad H1-8 coherente y `len(f10.cuerpos) == muertes` en las 6.
- **HH2 (instrumento, bloquea):** `lect_div > 0` en REL, ORÁCULO y ORÁCULO_SIN_MAPA.
- **HH6 (instrumento, bloquea):** estancia máxima de parche ≤ 25 000 en las 6.
- **HH3 (hipótesis):** R₀(RENACE, s1) < 0.8.  **HH4:** R₀(NADA, s1) ∈ [0.03, 0.30].  **HH5:** cob5(REL) > cob1(REL) en las dos semillas.
Si HH3–HH5 fallan, se anotan; ningún umbral cambia.

## 9. Comando exacto de la serie (la corre el coordinador)
```
cd C:\Users\User\Documents\PROYECTOS\JUACO-EXO\equipos\fase10\F0_fable_solo
set PYTHONIOENCODING=utf-8
python identidad_mundo_fase10.py 30000
python corre_mundo_fase10.py --humo
python corre_mundo_fase10.py --serie --desde 2401 --pool 7            (réplica: --desde 2421)
```
Salida: `datos/mundo_fase10_s2401-2420_<sello>.json` (crudo), `_veredicto_<sello>.json`, `.log`.

## 10. Arnés — resultado: **79/79 PASA** (266 s, un proceso, 21-sep 20:26; `identidad_mundo_fase10_salida.txt`)
Primera pasada 77/79: I6 difería sólo por el eco de configuración `nodo_or=1` que `organismo_f9c` agrega al dict `f9` (contenido leído idéntico); el arnés lo quita antes de comparar y se relanzó entero.

```
  sha organismo_v142 (TRONCO)    17528d767fcebaf6
  sha organismo_f9 (origen)      3a821884394d66c9
  sha organismo_f9c              9dd1fb91ecec35ae
  sha organismo_vivo_codigo      839fa71f9c84cb26
  sha organismo_v3cal            148014f68cb01785
  sha mundo_mapa                 207d6a1954336b18
  sha mundo_fase10 (DESTINO)     84e97674f709a900
  sha corre_mundo_fase10         31eb9aad9998a95c
  sha este arnes                 f91f6329b8673e22

--- I10 regla 14: CUERPO / NODO del runner == corre_f9 ---
  [    0s] OK    I10 CUERPO (17 campos) y NODO campo a campo == corre_f9  17 campos

--- I1: mundo del tronco, perillas apagadas == organismo_v142 (12 escenarios x 2 semillas, T=30000) ---
  [    3s] OK    I1                 AB por defecto s1  IDENTICO
  [    7s] OK    I1                 AB por defecto s2  IDENTICO
  [   11s] OK    I1                   AB invertido s1  IDENTICO
  [   14s] OK    I1                   AB invertido s2  IDENTICO
  [   18s] OK    I1            AB + patron nuevo C s1  IDENTICO
  [   22s] OK    I1            AB + patron nuevo C s2  IDENTICO
  [   26s] OK    I1            AB solap_AB=3 (E2L) s1  IDENTICO
  [   30s] OK    I1            AB solap_AB=3 (E2L) s2  IDENTICO
  [   33s] OK    I1             AB sin plasticidad s1  IDENTICO
  [   38s] OK    I1             AB sin plasticidad s2  IDENTICO
  [   42s] OK    I1           AB via lenta apagada s1  IDENTICO
  [   46s] OK    I1           AB via lenta apagada s2  IDENTICO
  [   49s] OK    I1                  AB sin puerta s1  IDENTICO
  [   53s] OK    I1                  AB sin puerta s2  IDENTICO
  [   57s] OK    I1      AB sin division por signo s1  IDENTICO
  [   61s] OK    I1      AB sin division por signo s2  IDENTICO
  [   65s] OK    I1           AB sin hija dispersa s1  IDENTICO
  [   69s] OK    I1           AB sin hija dispersa s2  IDENTICO
  [   73s] OK    I1       AB sin puerta por codigo s1  IDENTICO
  [   77s] OK    I1       AB sin puerta por codigo s2  IDENTICO
  [   81s] OK    I1    AB las dos perillas v14 off s1  IDENTICO
  [   85s] OK    I1    AB las dos perillas v14 off s2  IDENTICO
  [   89s] OK    I1    AB D comida solap_B=2 (E2K) s1  IDENTICO
  [   93s] OK    I1    AB D comida solap_B=2 (E2K) s2  IDENTICO

--- I2: el rng NO se consume (T=120000, semilla 1) ---
  [  108s] OK    I2 T=120000 s1  IDENTICO

--- I3: desambiguar=0 == organismo_f9 en los 9 brazos de corre_f9 (T=20000) ---
  [  111s] OK    I3     RENACE s1  IDENTICO
  [  114s] OK    I3     RENACE s2  IDENTICO
  [  117s] OK    I3       NADA s1  IDENTICO
  [  120s] OK    I3       NADA s2  IDENTICO
  [  123s] OK    I3         M1 s1  IDENTICO
  [  126s] OK    I3         M1 s2  IDENTICO
  [  130s] OK    I3        REC s1  IDENTICO
  [  133s] OK    I3        REC s2  IDENTICO
  [  136s] OK    I3        REL s1  IDENTICO
  [  140s] OK    I3        REL s2  IDENTICO
  [  142s] OK    I3   REL_FIJO s1  IDENTICO
  [  145s] OK    I3   REL_FIJO s2  IDENTICO
  [  149s] OK    I3    REL_BAR s1  IDENTICO
  [  153s] OK    I3    REL_BAR s2  IDENTICO
  [  155s] OK    I3   REL_AZAR s1  IDENTICO
  [  158s] OK    I3   REL_AZAR s2  IDENTICO
  [  163s] OK    I3  REL_TARDE s1  IDENTICO
  [  167s] OK    I3  REL_TARDE s2  IDENTICO

--- I4: mundo vivo + B-5 == organismo_vivo_codigo (desambiguar=1, sin reproduccion) ---
  [  170s] OK    I4 vivo desambiguar=1 s1  IDENTICO
  [  174s] OK    I4 vivo desambiguar=0 s1  IDENTICO
  [  178s] OK    I4 vivo desambiguar=1 s2  IDENTICO
  [  181s] OK    I4 vivo desambiguar=0 s2  IDENTICO

--- I5: rep2 + PLACEBO == organismo_v3cal (placebo=1, desambiguar=1) ---
  [  184s] OK    I5 placebo=0 s1  IDENTICO
  [  188s] OK    I5 placebo=1 s1  IDENTICO
  [  192s] OK    I5 placebo=0 s2  IDENTICO
  [  195s] OK    I5 placebo=1 s2  IDENTICO

--- I6: ORACULO == organismo_f9c (nodo_or=1, nodo_via=0), desambiguar=0 ---
  [  200s] OK    I6 ORACULO s1  IDENTICO
  [  204s] OK    I6 ORACULO s2  IDENTICO

--- I7: INERCIA del mapa sin r_vis (usa_M=1, olvida_M=1) ---
  [  208s] OK    I7 tronco s1  IDENTICO
  [  211s] OK    I7 vivo REL s1  IDENTICO
  [  214s] OK    I7 tronco s2  IDENTICO
  [  217s] OK    I7 vivo REL s2  IDENTICO

--- I8 / I9: f10 solo agrega 'f10'; determinismo (mundo F10, brazo REL, T=20000) ---
  [  223s] OK    I8 f10=1 vs f10=0 (menos la clave f10)  IDENTICO
  [  226s] OK    I9 determinismo REL  IDENTICO

--- D1..D12: controles que DEBEN diferir (mundo F10 salvo donde se dice, T=20000, semilla 1) ---
  [  229s] OK    D1 r_vis=8 != r_vis=None (cuerpo REL, mundo vivo del tronco)  DIFIERE (debe) 
  [  234s] OK    D2 usa_M=1 != usa_M=0 (r_vis=8, mundo vivo del tronco)  DIFIERE (debe) 
  [  236s] OK    D3 olvida_M=1 != olvida_M=0 (mundo F10)  DIFIERE (debe) 
  [  239s] OK    D4 parches=6 != parches=0 (mundo vivo, r_vis=8)  DIFIERE (debe) 
  [  242s] OK    D5 cambia_cada=5000 != 0 (mundo F10)  DIFIERE (debe) cambios 3
  [  245s] OK    D6 placebo=1 != 0 (mundo F10)  DIFIERE (debe) 
  [  249s] OK    D7 ORACULO != REL (mundo F10)  DIFIERE (debe) 
  [  252s] OK    D8 desambiguar=1 != 0 (mundo F10: B-5 actua)  DIFIERE (debe) des_splits REL 16
  [  255s] OK    D9 pats 16 tipos != pats del tronco  DIFIERE (debe) 
  [  259s] OK    D10a NODO_BARAJADO != REL  DIFIERE (debe) baraja_identidad 0
  [  259s] OK    D10b NADA != REL  DIFIERE (debe) lect_div REL 51/51
  [  260s] OK    D11 MUNDO_FIJO != REL  DIFIERE (debe) 
  [  264s] OK    D12 MAPA_SIN_TABLA != SIN_HERENCIA  DIFIERE (debe) 
  [  266s] OK    D13 REL_SIN_MAPA != REL  DIFIERE (debe) 

--- GUARDIAS ---
  [  266s] OK    G1 nodo_or sin nodo  F10: nodo_or exige nodo=1 (el oraculo sustituye el CONTENIDO del nodo,
  [  266s] OK    G2 olvida_M sin usa_M  F10: olvida_M exige usa_M=1 (no hay mapa que olvidar)
  [  266s] OK    G3 parches sin vivo  F10: parches exige vivo=1 (el mundo de la fase 10 es el mundo vivo)
  [  266s] OK    G4 f10 sin h1  F10: f10=1 exige h1=1 y rep2=1 (las medidas del cuerpo usan su nacimie
  [  266s] OK    G5 vals incompletos  F10: vals debe dar la valencia de TODOS los tipos de pats

VEREDICTO identidad_mundo_fase10: PASA  79/79   (266s, un proceso)
exit 0
```


## 11. Humo — resultado (21-sep 20:30; `datos/humo/mundo_fase10_humo_20260921_203032.{log,json}`, sha del JSON `41667be59f5a5b79`; 97 s, un proceso; identidad dentro del runner 5/5)

**Instrumento:** HH1, HH2, HH6 SÍ (bloqueantes: contabilidad, lecturas, parches). **Hipótesis:** HH3 SÍ (RENACE R₀ 0.063 < 0.8), HH4 SÍ (NADA 0.085), **HH5 NO** (cob5 > cob1 en s1: 0.938 vs 0.75; en s2 0.688 vs 0.75: refutada a la mitad, autor F0).

| brazo (s) | R₀ | muertes | fund | vida | mnec [E, Ag] | causas alias/limpio/drenaje | cob1 → cob5..12 | expl1 → expl5 | enc1 → enc5 |
|---|---|---|---|---|---|---|---|---|---|
| RENACE (1) | **0.063** | 253 | 0 | 200 | 121/132 | 0/164/89 | 0.69 → 0.75 | 0.156 → 0.078 | 125 → 7 |
| NADA (1) | 0.085 | 366 | 336 | 64 | 180/186 | 46/314/6 | 0.63 → 0.50 | 0.156 → 0.016 | 157 → 4 |
| REL (1) | 0.046 | 283 | 270 | 151 | 160/123 | 24/193/66 | 0.75 → **0.94** | 0.156 → 0.047 | 76 → 8 |
| REL (2) | 0.065 | 307 | 287 | 139 | 146/161 | 19/239/49 | 0.75 → 0.69 | 0.125 → 0.0 | 96 → 20 |
| ORÁCULO (1) | 0.058 | 311 | 293 | 113 | 157/154 | 32/236/43 | 0.75 → 0.84 | 0.156 → 0.0 | 76 → 7 |
| ORÁCULO_SIN_MAPA (1) | 0.086 | 335 | 306 | 99 | 142/193 | 48/280/7 | 0.63 → 0.81 | 0.156 → 0.016 | 157 → 10 |

**Lectura (sin valor de veredicto, n = 1–2):** (a) **V-6 CAE como predije**: el inmortal con mapa y tabla (cob 0.75) muere 253 veces en 100 000 pasos; la causa dominante es `limpio` (veneno con código no aliasado mordido con la otra necesidad activa), no alias ni drenaje: la predicción que más me importaba (§4) acierta. (b) Ningún brazo se acerca a R₀ 1; ORÁCULO ≈ REL ≈ NADA ≈ 0.05–0.09: en este mundo **el conocimiento heredado no compra nada** porque el cuerpo no lo consulta al decidir con la otra necesidad. (c) **Defecto de instrumento hallado en el humo, declarado:** el cuerpo 1 nace con E = Ag = 1.0 (fundador) y antes del primer cambio, y vive 1 198 pasos contra 184 de los cuerpos 5..12 (que nacen con la dote 0.6 y con el mundo ya cambiado): la razón M10-2 "5..12 / 1" está sesgada **contra** la acumulación por construcción (expl1 0.14 vs expl5 0.02). La letra queda; para la serie propongo M10-2′: cuerpos 5..12 contra cuerpos 2..4 (misma dote, mismo mundo) — decisión del coordinador, sin recalibrar. (d) B-5 divide muchísimo (11 078 divisiones en REL s1: con 16 tipos y dos necesidades, R == 0 es frecuente); las celdas al morir siguen en 30 porque los cuerpos mueren jóvenes; RENACE llega a 68. (e) La cobertura del signo de los cuerpos 5..12 de REL (0.94 / 0.69) y ORÁCULO (0.84) sí supera a NADA (0.50): **la transmisión llena la tabla; la boca no la usa cuando manda la otra necesidad.**

```
HUMO MUNDO FASE 10 · 2026-09-21 20:30:32 · UN proceso, sin Pool (regla 3) · 6 corridas de T=100000
  mundo_fase10.py sha 84e97674f709a900 · runner sha 31eb9aad9998a95c · origen f9 3a821884394d66c9 · python 3.14.2 numpy 2.4.3
  MUNDO: r_vis=8, usa_M=1, escribe_M=1, olvida_M=1, parches=6, cap=5, regen=30, vida_parche=8000, cambia_cada=5000, cambia_fam=4, f10=1, desambiguar=1 · 16 tipos en 10 pixeles

ETAPA 1/3 — identidad dentro del runner (regla 14, ERR-38)
  OK   (0) regla 14: CUERPO y NODO campo a campo == corre_f9   17 + 6 campos
  OK   (1) mundo del tronco: NADA (desambiguar=0) == organismo_f9 NADA (= NADA_CM de H-1)   dif []
  OK   (2) mundo del tronco: perillas apagadas == organismo_v142 (TRONCO v14.2), todas las claves   dif []
  OK   (3) mundo F10: REL != NADA y REL != NODO_BARAJADO (DEBEN diferir, ERR-38)   lect_div REL 51/51 · R0 REL 4/52 NADA 6/87
  OK   (4) mundo F10: el mapa actua (REL != REL_SIN_MAPA) y el mundo cambia (n_cambios > 0)   n_cambios 3 · M_llenas 6

ETAPA 2/3 — 6 corridas: [('RENACE', 1), ('NADA', 1), ('REL', 1), ('REL', 2), ('ORACULO', 1), ('ORACULO_SIN_MAPA', 1)]
  [  27.9s] RENACE            s1  R0 0.063   desc 16   muertes 253  fund 0 vida 200.0   mnec [121, 132] cob1 0.688 cob5 0.75 expl1 0.156 expl5 0.078 rz 0.5 enc1/5 125.0/7.0 causas {'alias': 0, 'limpio': 164, 'drenaje': 89} pmax 8000 cambios 19 alias t None/0.197 coh None f10 True
  [  34.1s] NADA              s1  R0 0.0845  desc 31   muertes 366  fund 336 vida 64.0    mnec [180, 186] cob1 0.625 cob5 0.5 expl1 0.156 expl5 0.016 rz 0.103 enc1/5 157.0/4.0 causas {'alias': 46, 'limpio': 314, 'drenaje': 6} pmax 4190 cambios 19 alias t 0.451/0.412 coh True f10 True
  [  50.0s] REL               s1  R0 0.0458  desc 13   muertes 283  fund 270 vida 151.0   mnec [160, 123] cob1 0.75 cob5 0.938 expl1 0.156 expl5 0.047 rz 0.301 enc1/5 76.0/8.0 causas {'alias': 24, 'limpio': 193, 'drenaje': 66} pmax 8000 cambios 19 alias t 0.5/0.35 coh True f10 True
  [  65.9s] REL               s2  R0 0.0649  desc 20   muertes 307  fund 287 vida 138.5   mnec [146, 161] cob1 0.75 cob5 0.688 expl1 0.125 expl5 0.0 rz 0.0 enc1/5 96.0/19.5 causas {'alias': 19, 'limpio': 239, 'drenaje': 49} pmax 6251 cambios 19 alias t 0.395/0.381 coh True f10 True
  [  83.7s] ORACULO           s1  R0 0.0577  desc 18   muertes 311  fund 293 vida 112.5   mnec [157, 154] cob1 0.75 cob5 0.844 expl1 0.156 expl5 0.0 rz 0.0 enc1/5 76.0/7.0 causas {'alias': 32, 'limpio': 236, 'drenaje': 43} pmax 8000 cambios 19 alias t 0.3/0.38 coh True f10 True
  [  96.9s] ORACULO_SIN_MAPA  s1  R0 0.0863  desc 29   muertes 335  fund 306 vida 98.5    mnec [142, 193] cob1 0.625 cob5 0.812 expl1 0.156 expl5 0.016 rz 0.103 enc1/5 157.0/9.5 causas {'alias': 48, 'limpio': 280, 'drenaje': 7} pmax 6659 cambios 19 alias t 0.403/0.347 coh True f10 True

ETAPA 3/3 — predicciones del humo (HH1..HH6, escritas en el PREREGISTRO antes de lanzarlo)
  HH1: SI
  HH2: SI
  HH3: SI
  HH4: SI
  HH5: NO
  HH6: SI
  Solo HH1, HH2 y HH6 BLOQUEAN (son el instrumento). HH3, HH4 y HH5 son la HIPOTESIS: si fallan se anotan; NINGUN umbral cambia (regla 4).

PUERTAS sobre el humo (orientativo: n = 1-2 semillas, sin valor de veredicto)
  V-6    CAE   ANCLA (BLOQUEANTE): el coste de vida conserva el ancla del mundo vivo -- R0 NADA en [0.10, 0.30] y R0 RENACE en [0.80, 1.30]
          R0_NADA 0.085 en [0.1, 0.3] · R0_RENACE 0.063 en [0.8, 1.3] · vida NADA 64.0 · vida RENACE 200.0 · muertes_nec NADA [[180, 186]]
  V-1    PASA  RECURSOS QUE SE AGOTAN Y SE MUEVEN: ningun parche se queda mas de T/4 en su sitio (todos los brazos salvo MUNDO_FIJO, que DEBE fallar)
          estancia maxima de un parche <= 25000: violaciones ninguna en 5 brazos · MUNDO_FIJO (debe fallar) []
  V-2    REPORTA  SABER DONDE VALE TANTO COMO SABER QUE: R0(ORACULO_SIN_MAPA) < 1 y R0(MAPA_SIN_TABLA) < 1 y R0(ORACULO) >= 1 (medianas)
          R0 ORACULO_SIN_MAPA 0.086 (< 1) · MAPA_SIN_TABLA None (< 1) · ORACULO 0.058 (>= 1) · vidas 98.5 / None / 112.5 · REL_SIN_MAPA R0 None · muertes_nec ORACULO [[157, 154]]
  V-3    REPORTA  EL ALIAS CUESTA VIDAS: sin desambiguar (REL_D0), tasa de mordida de lo malo CON alias >= 2x la de lo malo SIN alias (mordidas/exposiciones agregadas; exposiciones reportadas, trampa 3)
          REL_D0: tasa de mordida de lo malo CON alias None (0/0) vs SIN alias None (0/0) -> razon None (>= 2.0) · REL (B-5): 0.448 vs 0.366 · muertes por causa REL_D0 []
  V-4    REPORTA  UNA VIDA NO ALCANZA, UN LINAJE SI: cobertura de la tabla al morir, mediana de SIN_HERENCIA < 0.50; cuerpos 5..12 de REL > 0.80
          cobertura al morir (signo): SIN_HERENCIA todos los cuerpos None (< 0.5) · REL cuerpos 5..12 0.813 (> 0.8) · REL con criterio |v|>=0.5 0.563 · NADA 0.5 · NODO_BARAJADO 5..12 None · ORACULO 5..12 0.844
  V-5    REPORTA  MAS DE UN CUERPO A LA VEZ: opcion DECLARADA (cola de descendientes, un cuerpo vivo); no se mide ni se nombra hasta medirla
          opcion declarada en el preregistro (cola FIFO de descendientes, un cuerpo vivo a la vez); nada medido, nada nombrado
  M10-1  REPORTA  SOSTEN: REL cruza R0 >= 1.0 con fundadores <= 2 en >= 15/20 semillas; NADA < 0.5; NODO_BARAJADO < 0.5 (medianas)
          REL: R0 >= 1.0 con fundadores <= 2 en 0/2 (>= 15) · mediana R0 REL 0.055 fund 278.5 vida 144.75 · NADA 0.085 (< 0.5) · NODO_BARAJADO None (< 0.5) · SIN_HERENCIA None · REL_SIN_MAPA None · ORACULO 0.058
  M10-2  REPORTA  ACUMULACION: combinaciones (tipo x cuarto) explotadas por los cuerpos 5..12 >= 2x las del cuerpo 1, pareado por semilla (mediana de razones >= 2.0 y A12 pareado >= 0.85, n >= 15); NODO_BARAJADO <= 1.2x
          REL: razon explotadas cuerpos 5..12 / cuerpo 1: mediana 0.15 (>= 2.0), n 2 (>= 15), A12 pareado 0.0 (>= 0.85) · expl1 0.141 expl5 0.024 · exposiciones cuerpo 1 86.0 vs 5..12 13.75 (trampa 3) · vidas 1198.5 vs 184.25 · NODO_BARAJADO razon None (<= 1.2) · NADA 0.103 · SIN_HERENCIA None · ORACULO 0.0
  M10-3  REPORTA  NO ES EL MUNDO BLANDO: en MUNDO_FIJO la razon cuerpos 5..12 / cuerpo 1 <= 1.2x
          MUNDO_FIJO: razon 5..12 / 1 None (<= 1.2) · R0 None vida None cob 5..12 None · (razon 5..12 / 2..4 se reporta como M10-3': no calculada aqui, ver crudo)
  M10-4  REPORTA  NO REGRESION: perillas apagadas == tronco v14.2 BIT A BIT y el mapa INERTE sin r_vis (identidad_mundo_fase10.py, pegado en el preregistro); las baterias las corre el coordinador; coste 1.00x por identidad
          identidad y coste por arnes (identidad_mundo_fase10.py, pegado en el preregistro); bateria_v142 y bateria_generaliza_v142 las corre el coordinador
  M10-5  REPORTA  REPRESENTACION (se reporta, no es puerta): celdas al morir, divisiones B-5, pares alias (bueno,malo) al nacer y al morir
          celdas al morir REL 30.0 vs NADA 30.0 vs RENACE 68.0 · divisiones B-5 (suma) REL 11077.5 REL_D0 None · pares alias (bueno,malo) al nacer 1.0 al morir 1.0 sep 0.0 · RENACE sep 0.0
  PLAC   REPORTA  VALIDEZ DEL NULO: |R0 PLACEBO - R0 REL| <= 0.15 y A12(R0 PLACEBO vs REL) en [0.35, 0.65]; razon M10-2 de PLACEBO en [0.8, 1.25] x la de REL
          |R0 PLACEBO - REL| None (<= 0.15) · A12 None en [0.35, 0.65] · razon M10-2 PLACEBO/REL None en [0.8, 1.25] · PLACEBO pasa M10-1 como REL: 0/0

JSON  C:\Users\User\Documents\PROYECTOS\JUACO-EXO\equipos\fase10\F0_fable_solo\datos\humo\mundo_fase10_humo_20260921_203032.json  (sha 41667be59f5a5b79)
HUMO terminado en 97.0s
exit 0
```

