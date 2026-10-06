# PREREGISTRO — ECO_SEL LARGO: ¿la selección sigue subiendo K con 10× más tiempo? ¿Margen + cerebro juntos superan al cerebro solo? (creador, 28-sep-2026, BORRADOR)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros.

- Frente 2 (ECO), nivel 10 (JUACO-ECO). No es candidato a tronco. Carpeta `experimentos/organelos/eco_sel_largo/`, rama
  `nube/eco-sel-largo-20260928` (base `organelos` 87d82b2). Encargo: `experimentos/organelos/eco_sel/ENCARGO_NUBE_largo.md`.
- Lo escribe el creador **antes de la serie**; lo integra, commitea y corre el coordinador. §0 (shas) y §11 se completan tras el arnés y el
  humo; §1–§10 son las de este texto. **Borrador: el coordinador lo revisa y lo commitea ANTES de la serie** (regla 11: umbral cambiado
  después = ERR).

## 1. De dónde sale y qué pregunta
- **ECO_SEL = FUNCIONA ×2 en M y en C** (45301–45340, T = 1e6): en el linaje de F1 frío la selección natural sube K (media de vivos en
  [T/2, T]) de ~31 (F1) a ~35 (SEL_M, margen heredable) y ~39 (SEL_C, 15 genes del cerebro heredables), 20/20 ×4 contra F1; sin herencia
  (AZA) queda por debajo de F1. En SEL_C las muertes por veneno + sal caen de ~82 % a 2–3.5 % (descriptivo).
- **Dato previo que orienta la predicción:** en el humo de eco_sel (45395, T 200 000) SEL_C ya daba K 37.4; a 1e6 la mediana es 38.9–39.2.
  La mayor parte de la subida ocurre en los primeros 2·10⁵ pasos. Eso sugiere un techo cercano, no una rampa.

**Dos preguntas, dos veredictos que NO se combinan:**
- **L (larga):** con T = 1e7 (≈ 6 000 generaciones en vez de ≈ 600), ¿K de SEL_C sigue subiendo, o se estanca en el valor de T = 1e6?
  Es la pregunta de evolución abierta en su versión más pequeña: si hay techo o no en este mundo y con estos genes.
- **MC (combinado):** si mutan a la vez el margen (`rep_umbral`) y los 15 del cerebro (16 genes; `dote` y `rep_X` fijos), ¿K supera a
  SEL_C sola?

## 2. Mecanismo mínimo y memoria nueva
**Memoria nueva: cero. Mecanismo nuevo: cero.** El mundo, el carro (FAMB_RES0_ECO), el gemelo (`frio/motor_frio_rapido.py`), la genética
(`motor_eco`: mutación log-normal, p = 0.05 y σ = 0.15 por gen mutable, banco 200, 8 sombras, `donante` 'padre' o 'azar') son los de
eco_sel sin cambios. Sólo se agregan:
- brazo **SEL_MC** (genética `MC`): mutables = los 16 genes `eta … NK, rep_umbral` (orden de `motor_eco.NOMBRES`), con herencia;
- brazo **AZA_MC** (`MC_AZAR`): los mismos 16 con `donante = 'azar'` (el genoma de todo cuerpo nuevo sale de una entrada al azar del
  banco, mutada; el banco guarda el genoma nuevo). Varía igual y no se hereda;
- T = 1e7; telemetría por ventanas de T/10; checkpoint cada 100 000 pasos.

| brazo | genética | qué muta | papel |
|---|---|---|---|
| **F1** | MUT0 | nada | ancla de validez (V1) y control del tiempo solo (L-3) |
| **SEL_C** | CEREBRO | 15 genes del cerebro | hipótesis L; referencia de MC |
| **SEL_MC** | MC | 15 del cerebro + `rep_umbral` | hipótesis MC |
| **AZA_MC** | MC_AZAR | los mismos 16, sin herencia | control de deriva (L-2) y de herencia (MC-2) |
| SEL_M | MARGEN | sólo `rep_umbral` | **descriptivo** (no entra en la letra; §10) |

Todos: ECO w90, esc 90, 90 fundadores, quimiostato, tope 3000, carro FAMB_RES0_ECO, t_corte = 1 (frío), banco 200, 8 sombras, genes cada
2 000, checkpoint cada 100 000.

## 3. Instrumento y anclas
- `construye_eco_sel_largo.py` construye `nucleo_eco_sel_largo.py` por anclas (B1–B10) desde `eco_sel/nucleo_eco_sel.py`
  (sha **6a36e47ce61db3e1**, a su vez verificado con `construye_eco_sel.py --verifica`). Cambios: brazos SEL_MC/AZA_MC y genéticas MC/MC_AZAR;
  semillas; `_Tel` (telemetría por ventana alimentada por el mismo `ind_cb`) guardada en el checkpoint; checkpoint cada 100 000;
  `_extra_largo` agrega la clave `ventanas`. **Todas las claves de eco_sel quedan bit a bit** (arnés (A) a T = 1e6).
- `corre_eco_sel_largo.py`: runner y letra; `verifica()` exige los dos núcleos construidos por anclas y los shas fijados (FIJOS) antes de
  correr nada.
- **Telemetría (`ventanas`)**, bordes W_k = k·T/10:
  - vivos en el borde (el estado tras el paso W − 1, el mismo instante que la fila de `gen_t` y que `tam_total[W/1000]`);
  - de cada gen mutable del brazo: media y cuantiles 10/50/90 en los vivos del borde; `media_log` (18 genes) para el cruce con `gen_t`;
  - nacimientos por ventana (por t de nacimiento), muertes por causa (hambre, sed, veneno, sal) y vida media por ventana (por t de muerte).
  - Costo: ≈ 50 genomas × 10 bordes por corrida; despreciable (medido en §11).
- **K por ventana** (`kvent`): media de `tam_total` (una muestra cada 1 000 pasos) en las muestras de t = a … b **inclusive**; tras la
  extinción cuenta 0. `kvent(T/2, T)` es exactamente el `kbar` de eco_sel (arnés). Ventanas contiguas comparten la muestra del borde.
  - **K base** = [T/20, T/10] = [0.5e6, 1e6]: la misma cantidad que la K de eco_sel a T = 1e6 (y la dinámica no depende de T: arnés (P)).
  - **K final** = [9T/10, T] = [9e6, 1e7]. (La base mide 5·10⁵ pasos y la final 10⁶: declarado.)
- **Arnés `identidad_eco_sel_largo.py`** (salida `identidad_eco_sel_largo_salida.txt`): (K) anclas y shas · (A) a T = 1e6 F1 y SEL_C ==
  eco_sel en todas sus claves, la única nueva es `ventanas`, y kvent == kbar · (B) SEL_MC y AZA_MC con p_mut = 0 == F1 bit a bit; (B′) con
  σ = 0 sólo se mueven los 2 genes enteros (ver §11); controles con σ = 0.15 · (M) SEL_MC muta exactamente los 16 genes · (H) herencia exacta en SEL_MC; AZA_MC no hereda (caso H de ERR-149) · (C) gemelo ==
  motor Python · (D) frío limpio + control con vivero · (T) telemetría consistente con `gen_t`, `tam_total`, `n_nac` · (P) la dinámica no
  depende de T · (Q) corte de luz + `--reanuda` · (Z) determinismo · (F) nube-9 · (V) la letra en casos sintéticos · (R) banderas.

## 4. Semillas NUEVAS
- Grep del 28-sep (20:40 UTC) en el árbol de `nube/eco-sel-largo-20260928` y en **las 10 ramas remotas** (`git grep` sobre `origin/*` en
  `*.py *.md *.txt *.log`, nombres de archivo con `s454xx`, claves `"seed"/"semilla"/"desde"` en JSON) y `git log --all -S`: 45401–45440 y
  45491–45499 **no se usan como semilla** en ninguna parte (sólo aparecen en el encargo; las coincidencias en `datos/*.json|csv` viejos son
  valores numéricos, no semillas).
- **Serie 45401–45420; réplica 45421–45440** (si la serie no da NO en alguna de las dos preguntas).
- **Práctica 45491–45499:** el arnés usa 45492–45496; el humo 45491.

## 5. Medidas
- **K**, por semilla, pareada entre brazos (misma semilla = mismo mundo inicial). En F1 la K de eco_sel fue 29.9–31.7 (DE ≈ 0.5).
- **dK** = K final − K base, por semilla y brazo.
- Por qué no el rango contra sombras (la P1 de eco_sel): a T largo la deriva de las 8 sombras llena el rango (eco_sel §5), la prueba pierde
  potencia. Se reporta en t = 100 000 y en T como **descriptivo**.
- Descriptivo obligatorio: curva de K por ventana (mediana y cuantiles 10/90 sobre semillas, por brazo); genes por ventana (mediana sobre
  semillas de la media de los vivos en cada borde; cuantiles en el JSON); fracción de muertes por veneno + sal por ventana; nacimientos
  totales; persistencia; K [T/2, T].

## 6. Criterio por la letra (`corre_eco_sel_largo.veredicto`)
**Validez común (si falla, las dos preguntas son NO EVALUABLE):**
- serie completa: 5 brazos × 20, las mismas semillas, T = 1e7, t_corte = 1, ningún aborto, ningún brazo ajeno;
- **V1:** F1 persiste en T ≥ 17/20;
- **V2:** frío limpio en los 5 brazos (0 refundados, 0 fundadores repuestos);
- **VB:** una semilla con `bloqueados` > 0 en cualquier brazo (tope de cuerpos alcanzado) es **NO EVALUABLE** y cuenta como fallo en toda
  puerta pareada (el umbral sigue siendo 15 de 20); con **≥ 3** semillas así, las dos preguntas son NO EVALUABLE.

**Validez por pregunta — V3, la genética es la declarada** (`mutables` igual al del brazo; 0 valores de genes no mutables fuera de G0 en
los vivos; mutación en ≥ 18/20 de cada brazo que muta y 0 en F1): L mira SEL_C, AZA_MC y F1; MC mira SEL_MC, SEL_C, AZA_MC y F1.

**Pregunta L (todas sobre las semillas evaluables; un empate no cuenta como subir):**
- **L-1a:** dK(SEL_C) > 0 en ≥ 15/20.
- **L-1b:** mediana de dK(SEL_C) ≥ +2.0 cuerpos.
- **L-2, no es deriva (control que puede fallar):** (a) AZA_MC **no** cumple L-1a y L-1b a la vez, **y** (b) dK(SEL_C) > dK(AZA_MC),
  pareado, en ≥ 15/20.
- **L-3, no es el tiempo solo (control que puede fallar):** dK(SEL_C) > dK(F1), pareado, en ≥ 15/20. (F1 tiene la tabla de la familia,
  que es herencia cultural: si K subiera sola con el tiempo, subiría también en F1.)
- **FUNCIONA** = L-1a + L-1b + L-2 + L-3. **HAY ALGO MODESTO (sigue subiendo, menos de +2)** = L-1a + L-2 + L-3 sin L-1b.
  **NO** = cualquier otro caso (se estanca, baja, o lo explican la deriva o el tiempo).

**Pregunta MC (K final):**
- **MC-1a:** K final(SEL_MC) > K final(SEL_C), pareado, en ≥ 15/20. **MC-1b:** mediana de la diferencia ≥ +1.5.
- **MC-2, es la herencia (control que puede fallar):** K final(SEL_MC) > K final(AZA_MC), pareado, en ≥ 15/20.
- **FUNCIONA** = MC-1a + MC-1b + MC-2. **HAY ALGO MODESTO (supera por menos de +1.5)** = MC-1a + MC-2 sin MC-1b. **NO** = cualquier otro.

- El bloque de cada pregunta se declara sólo si serie y réplica dan el mismo veredicto; si no, vale el menor. La réplica se corre si la
  serie no da NO en alguna de las dos.
- **Lógica de eco_sel conservada:** el control que puede fallar nunca da MODESTO solo; MODESTO exige el control **y** la mitad del efecto
  (el conteo pareado sin el margen de magnitud). Sin control no hay veredicto positivo.

**Nulos (regla 15):**

| puerta | nulo | umbral | P(pasa ∣ nulo) | potencia |
|---|---|---|---|---|
| L-1a | dK sin tendencia: signo p = 0.5 | ≥ 15/20 | 0.021 | 0.80 si P(dK > 0) = 0.8 |
| L-1b | ídem | mediana ≥ +2 | ≪ 0.02 (la DE de K entre ventanas de una semilla es ≈ 0.5–1) | — |
| L-2b · L-3 · MC-1a · MC-2 | signo p = 0.5 | ≥ 15/20 | 0.021 c/u | 0.80 si P = 0.8; 0.99 si 0.9 |
| MC-1b | sin diferencia | mediana ≥ +1.5 | ≪ 0.02 (DE entre semillas de K ≈ 0.5–1.5) | — |
| V1 | el instrumento no sostiene F1: p = 0.6 | ≥ 17/20 | 0.016 | 0.87 si p = 0.9 |

## 7. Predicciones firmadas (creador, antes del humo con números)

| # | cantidad | rango | p |
|---|---|---|---|
| E1 | F1 persiste en T = 1e7 /20 | 17–20 | V1 0.85 |
| E2 | K base de F1 y SEL_C, mediana (debe repetir eco_sel) | F1 [29.5, 32.5] · SEL_C [37, 41] | 0.90 |
| E3 | dK(F1), mediana | [−1.5, +1.5] | 0.80 |
| E4 | dK(SEL_C), mediana | [−1, +3] | 0.70 |
| E5 | L-1a (SEL_C sube en ≥ 15/20) | — | 0.45 |
| E6 | L-1b (mediana ≥ +2) | — | 0.25 |
| E7 | AZA_MC persiste en T /20 · K final mediana | 2–14 · [0, 22] | 0.60 |
| E8 | L-2 y L-3 (dado L-1a) | — | 0.90 |
| E9 | K final de SEL_MC, mediana | [38, 48] | 0.70 |
| E10 | MC-1a (SEL_MC > SEL_C en ≥ 15/20) | — | 0.55 |
| E11 | MC-1b (mediana ≥ +1.5) | — | 0.40 |
| E12 | MC-2 | — | 0.95 |
| E13 | `rep_umbral` de los vivos en W_10 en SEL_MC, mediana | [0.50, 0.80] (el margen sube, como SEL_M) | 0.75 |
| E14 | fracción de muertes por veneno + sal en la ventana 10: SEL_C y SEL_MC < 0.06; F1 > 0.70 | — | 0.80 |
| E15 | alguna semilla con `bloqueados` > 0 | — | 0.03 |
| E16 | veredicto L de una serie | FUNCIONA 0.20 · MODESTO 0.25 · NO 0.50 · NO EVALUABLE 0.05 | — |
| E17 | veredicto MC de una serie | FUNCIONA 0.35 · MODESTO 0.15 · NO 0.45 · NO EVALUABLE 0.05 | — |
| E18 | bloque (serie + réplica iguales) | L FUNCIONA ×2 0.12 · MC FUNCIONA ×2 0.25 | — |

**La predicción más expuesta es E4/E6:** el creador apuesta a un techo cercano (humo de eco_sel: 37.4 a 2·10⁵, 39 a 10⁶). Razón: el
veneno ya no mata en SEL_C; lo que queda es forrajear en un mundo de 3 600 celdas con flujo fijo, y los genes del cerebro tocan el valor
y la boca, no las patas. Si dK ≥ +2 en ≥ 15/20, esta razón cae. Para MC la duda es si margen y cerebro suman o compiten por el mismo
límite (el flujo de comida): la predicción es que suman poco.

## 8. Qué refuta
- **H-L (sigue subiendo):** L-1a cae con la validez intacta (K de SEL_C no sube en ≥ 15/20 de 1e6 a 1e7).
- **«Es la selección y no la deriva ni el tiempo»:** L-2 o L-3 caen.
- **H-MC:** MC-1a cae con la validez intacta; **«es la herencia»:** MC-2 cae.
- **La predicción del creador (techo):** L FUNCIONA.

## 9. Las cuatro trampas
1. **Canal simétrico:** SEL_MC y AZA_MC difieren sólo en `donante`; SEL_C y SEL_MC sólo en `rep_umbral` mutable; F1 no varía. Mismos p, σ,
   banco, sombras y rng por cuerpo ([seed, linaje, 16, k]).
2. **Acierto sin balancear:** no hay clasificación; K es un conteo pareado por semilla.
3. **Mundo que se come la comida:** el quimiostato ES esa dinámica; K sube si el mismo flujo sostiene más cuerpos. En MC `rep_umbral` es
   historia de vida: un K mayor puede venir de parir con menos reserva, no de forrajear mejor. Se declara y el vocabulario lo respeta.
4. **Sitios fijos:** los objetos aparecen en celdas libres al azar; la tabla de la familia es por letra, no por lugar.

## 10. Decisiones difíciles (creador, 28-sep, 20:40–21:10 UTC), vocabulario y costo
- **20:45 — núcleo nuevo por anclas, no registro en memoria.** Registrar SEL_MC/AZA_MC en `nucleo_eco_sel` bastaba para los brazos, pero la
  telemetría necesita el mismo `ind_cb` y viajar en el checkpoint (si no, `--reanuda` la perdería). Alternativa descartada: envolver
  `run_solapadas` y un pickle paralelo (dos archivos que pueden desincronizarse en un corte). Construido desde `nucleo_eco_sel.py` (que ya
  es el construido de F1) con sha como tripwire; el arnés (A) demuestra que las claves de eco_sel no cambian.
- **20:50 — checkpoint cada 100 000 (eco_sel: 10 000).** El blob incluye `gen_t` (una fila cada 2 000 pasos) y `filas`/`coh` de todos los
  nacidos: crece linealmente con t, así que 1 000 checkpoints a 1e7 costarían O(T²) en disco y en CPU. Con 100 000 son 100 blobs; se
  pierden a lo sumo 10⁵ pasos en un corte. No cambia la corrida (tramos del gemelo iguales; arnés (A) y (Q)).
- **20:55 — L-2 y L-3 más estrictas que el encargo.** El encargo sugiere L-2 = «AZA_MC no cumple L-1». Eso deja pasar una deriva que sube
  +1.9 en 16/20. Se agrega el pareado dK(SEL_C) > dK(AZA_MC) y **L-3 contra F1**: F1 no varía genéticamente pero sí hereda la tabla de la
  familia (cultura); si K subiera sola con el tiempo, no sería la selección. Alternativa descartada: sólo la letra del encargo.
- **21:00 — sin puerta de firma contra sombras.** A 1e7 la deriva de las sombras llena el rango (eco_sel §5); una P1 allí sería una puerta
  sin potencia. Se reporta.
- **21:00 — bloqueados por semilla** (el encargo: «esa semilla es NO EVALUABLE»): cuenta como fallo y con ≥ 3 semillas no se lee. Eco_sel
  anulaba la serie entera con un solo bloqueado; aquí 1e7 pasos lo hacen más probable (aunque E15 lo da en 0.03).
- **21:06 — SEL_M SE CORRE, como descriptivo** (el humo mide +0.6 h por serie con Pool 3; §11): responde «¿el margen solo también sigue
  subiendo?» sin sumar puertas. Alternativa descartada: 4 brazos (−18 % de costo) y perder la curva del margen solo a 1e7. Si el
  coordinador necesita recortar, SEL_M es el primero que sale (la letra no lo usa; `BRAZOS_L` en el runner, y el sha del runner cambia).
- **Vocabulario.** Permitido: «capacidad de carga del linaje (K = cuerpos vivos sostenidos)», «la selección natural sube K» con la medida,
  «sigue subiendo / se estanca» con la ventana. Prohibido: «evoluciona» sin la medida, «aprende», «especie», «entiende», «evolución abierta»
  como logro (es la pregunta, no la respuesta), «más listo».
- **Costo:** §11.

## 0. Instrumento (sha a 16 del creador, 21:06; el coordinador los re-verifica y fija el de este archivo al commitearlo)

| archivo | sha | qué es |
|---|---|---|
| `construye_eco_sel_largo.py` | 65b5d9f5b5f98f73 | constructor por anclas (B1–B10) |
| `nucleo_eco_sel_largo.py` | 69f2b652ac46cd1b | construido desde `eco_sel/nucleo_eco_sel.py` 6a36e47ce61db3e1 (`--verifica`: IGUAL) |
| `corre_eco_sel_largo.py` | 69db795b7d952d93 | runner y letra (§6); `verifica()` antes de correr |
| `identidad_eco_sel_largo.py` | 277e42c5f8f535e9 | arnés; salida `identidad_eco_sel_largo_salida.txt` (e8c54bf85cb8660d): **65/65** |
| `eco_sel/nucleo_eco_sel.py` · `eco_sel/construye_eco_sel.py` | 6a36e47ce61db3e1 · f2f5ed3c54d1b2c5 | origen (verificado por su constructor) |
| `frio/corre_frio.py` · `frio/motor_frio_rapido.py` | 3ba8b0f5cf1fbbfa · ff9d890a5cce9dec | origen del núcleo de eco_sel · el gemelo |
| `juaco_eco/corre_eco_v12.py` · `corre_eco.py` · `motor_eco.py` · `carros/FAMB_RES0_ECO.py` | 1340d268e1fd93d8 · 47d9cee4d6462116 · bca3033878b59622 · 94ea78589bc2ce24 | orígenes |

## 11. Arnés, humo y costo (se completó DESPUÉS del arnés y del humo; §1–§10 no se tocaron salvo la decisión de SEL_M, 21:06)
- **Arnés, 1ª corrida (20:49–20:54): 61/64.** Salida `identidad_eco_sel_largo_salida_v1_61de64.txt` (cc0382d55ee042f6). Cayeron:
  - (B) ×2 «SEL_MC/AZA_MC con σ = 0 == F1» (el caso del encargo). ****ERR-150** (numerado por el coordinador, 28-sep antes de la serie), del diseño del
    caso, no del instrumento:** `motor_eco.muta` redondea los genes ENTEROS y, si el valor no cambia, los mueve ±1 según el signo de z; con
    σ = 0, z = 0 → −1 siempre. `memoria_rechazo` y `NK` están entre los 16 de MC, así que con σ = 0 se mueven (en eco_sel el caso sólo se
    corrió con `rep_umbral`, real). Se partió en (B) p_mut = 0 == F1 bit a bit y (B′) σ = 0 deja los 14 reales en G0 y mueve sólo los 2 enteros.
    Con σ = 0.15 la regla es simétrica (z > 0 o < 0): no sesga la serie.
  - (T) SEL_MC: los cuantiles de la telemetría (valores crudos) contra los de `vivos_final` exigían igualdad exacta, pero `vivos_final`
    guarda los genes redondeados a 1e−6 (diferencia medida 5e−7). Tolerancia 2e−6. Mismo candidato a ERR (caso mal escrito).
- **2ª corrida (20:54–20:59): 63/65** (`..._v2_63de65.txt`, 6f86253c54aa9bbd): el caso nuevo (B) exigía `mutables == los 16`, pero el
  motor reporta como `mutables` los genes con p > 0, y con p_mut = 0 son ninguno (`distintas []`: la física sí era idéntica). Corregido.
- **Arnés final (20:59–21:04): 65/65** en 283 s, salida `identidad_eco_sel_largo_salida.txt` (e8c54bf85cb8660d). Núcleo, runner y letra
  **sin cambios** entre las tres corridas (sólo el arnés). Lo que muestra:
  - (A) a T = 1e6 (semilla 45492), F1 y SEL_C del núcleo largo == eco_sel en TODAS sus claves (la única nueva es `ventanas`); K de eco_sel
    30.547 y 39.501; kvent(T/2, T) == kbar exacto. SEL_C por ventanas de 10⁵: 35.6 → 39.1.
  - (B) p_mut = 0 == F1; (B′) σ = 0 mueve sólo los enteros; controles con σ = 0.15 fallan como deben.
  - (M) con p_mut = 1 cambian padre → hijo exactamente los 16 genes (dote y rep_X nunca); (H) SEL_MC 360/360 hijos == muta(padre);
    AZA_MC 1/222 (0.5 %) en hijos de padre no fundador.
  - (C) gemelo == Python; (D) frío limpio y el control con vivero refunda 389; (T) telemetría == gen_t y tam_total; (P) la dinámica no
    depende de T; (Q) corte en t = 100 000 + reanuda == entera; (Z) determinismo; (F); (V) 27 casos de la letra; (R).
- **Humo (21:04–21:05):** `corre_eco_sel_largo.py --humo`, semilla 45491, T 200 000, un proceso, 5 corridas, 36 s. JSON
  `datos/humo/eco_sel_largo_humo_s45491_T200000_20260928_210439.json` (79ca6704cde88baf) y log (c37f8f04e409428a).
  - Los 5 brazos persisten; 0 refundados, 0 bloqueados; mutables 0/15/16/16/1; 0 genes fuera.
  - Veredicto de prueba: NO EVALUABLE (una semilla), como debe. **Una semilla a 2·10⁵ no se lee; §7 NO se toca.**
- **Costo (medido con la CPU compartida con otra serie Pool 3: contaminado, probablemente pesimista):**
  - por corrida a 1e6: F1 32 s, SEL_C 41.5 s (arnés (A)); a 2·10⁵: 5.7 (AZA_MC) – 8.3 s (SEL_C, SEL_MC).
  - extrapolado lineal a 1e7: F1 ≈ 5.4 min, SEL_C y SEL_MC ≈ 6.9 min, SEL_M ≈ 5.6, AZA_MC ≈ 4.8 (menos si se extingue).
  - **Serie de 100 corridas ≈ 10 h de CPU → ≈ 3.3 h con Pool 3** (4 brazos sin SEL_M: ≈ 2.7 h). Réplica igual.
  - Checkpoint: el blob pesa 2.7–4.1 MB entre 1e5 y 9e5 y crece ≈ 0.15 MB por 10⁵ pasos → ≈ 15–20 MB a 1e7; `guarda` tarda ≤ 0.02 s;
    100 checkpoints por corrida: despreciable. Uno solo en disco por corrida (se reemplaza).
  - Memoria: 216 MB en el humo, 416 MB en el arnés (dos núcleos y el motor Python); a 1e7 `filas`/`coh`/`gen_t` crecen (≈ 175 000
    nacidos por corrida): estimado < 1 GB por trabajador; con Pool 3 cabe (15.7 GiB).
  - **Disco:** cada JSON a 1e7 ≈ 1–1.5 MB (gen_t de 260 filas y tam_total de 10 001): ≈ 100–150 MB por serie. El coordinador decide
    qué se commitea.
- Declarado: el gemelo se importa desde `frio/`; su caché vive en `frio/__pycache__/` (en `.gitignore`). Ningún archivo versionado fuera
  de `eco_sel_largo/` se tocó.

## Comandos
```
/root/venv-juaco/bin/python experimentos/organelos/eco_sel_largo/construye_eco_sel_largo.py --verifica
/root/venv-juaco/bin/python experimentos/organelos/eco_sel_largo/identidad_eco_sel_largo.py          # arnés, 1 proceso
/root/venv-juaco/bin/python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --humo       # 1 proceso, 45491, T 200 000
/root/venv-juaco/bin/python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --serie --desde 45401 --n 20 --pool 3
/root/venv-juaco/bin/python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --serie --desde 45421 --n 20 --pool 3   # réplica
/root/venv-juaco/bin/python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --serie --desde 45401 --n 20 --pool 3 --reanuda
/root/venv-juaco/bin/python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --lee experimentos/organelos/eco_sel_largo/datos/eco_sel_largo_serie_s45401-45420
```
