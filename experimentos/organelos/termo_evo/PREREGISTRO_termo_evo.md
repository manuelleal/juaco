# PREREGISTRO — bloque TERMO_EVO: ¿la selección encuentra el termostato sola? (nube, 28-sep-2026, escrito ANTES del humo y de la serie)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros.
Encargo: `ENCARGO_NUBE.md` (coordinador, aprobado por el director). Rama `nube/termo-evo-20260928`, base `organelos` 5bc646e.

## 0. Pregunta
Si el margen del termostato de boca deja de ser una constante de diseño y pasa a ser un **gen `g` por cuerpo, heredable con mutación**,
¿la selección lo lleva sola, desde la zona letal, a la banda que funciona (≈ 0.10–0.45) y con eso el linaje del bicho real cruza el R0
real de 0.90 en la pista de la carrera?

## 1. De dónde sale (EXPLORATORIO, `boca_buena/INFORME.md`, semillas 39001–39010)
Consigna S = rep_umbral + margen sobre lo bueno conocido: margen 0 → 0.000 (extinción 10/10); 0.10 → 0.921; 0.25 → 0.928; 0.40 → 0.951;
leer la otra necesidad → 0.000–0.106. V143 solo: 0.413. En el PC corre hoy la confirmatoria de TERMO (39101–39140): no se usan esas semillas.

## 2. Mecanismo y memoria nueva (`construye_evo.py`)
- **Pieza** (la del brazo m40 con el margen como gen): sobre la letra k con dS SENTIDO medio s (`_adS`, ya en v14.3) sin componentes
  negativas y con alguna positiva, **muerde ⇔ ∃ j: s_j > 0 ∧ nivel_j < rep_umbral + g**. Manda sobre boca de fábrica, FILTRO y APR
  sólo en esas letras; lo desconocido y lo malo sentido quedan como en v14.3. Sin rng nuevo en la boca.
- **Gen `g`: única memoria nueva, un float por cuerpo.**
  - Fundador (primer cuerpo del linaje y cada refundación de la ENMIENDA 5): g ~ U[G_INI].
  - `EVO = 1` (hereda): `al_parir` devuelve `{'g': clip(g_padre + N(0, σ), [−0.2, 1.0])}`; la pista lo guarda **opaco** en la cola con la
    dote y se lo entrega al hijo en `nace(info['memoria'])`. V143 no usaba esa memoria (su `al_parir` devolvía `None`).
  - `EVO = 2` (**SINHER**, control): la misma física; el hijo sortea g de nuevo de U[G_INI]. No hay selección acumulable.
  - rng del gen: `ctx['rng'].spawn(1)[0]` (el rng del CUERPO que la pista da al carro; `spawn` no avanza su estado, arnés (d)).
- **Perillas** (una línea): `EVO; G_INI; SIGMA; G_CLIP`. EVO 0 = V143 bit a bit.

| brazo | carro | EVO | G_INI | σ | papel |
|---|---|---|---|---|---|
| `v143` | V143 | – | – | – | base |
| `evo` | V143_EVO_BAJO | 1 | U[−0.10, 0.10] | 0.03 | **CANDIDATO** (arranca en la zona letal) |
| `sinher` | V143_EVO_SINHER | 2 | U[−0.10, 0.10] | – | **CONTROL** sin herencia |
| `ancho` | V143_EVO_ANCHO | 1 | U[−0.10, 0.60] | 0.03 | secundario, descriptivo |
| `m40` | V143_EVO_M40 | 1 | 0.40 fijo | 0 | techo DISEÑADO (== HIBB m40, arnés (b)) |
| `o1` | O1 | – | – | – | techo LLM, ANCLA de la pista |

## 3. Decisiones difíciles (tomadas por la sesión de nube, con su porqué)
- **D1 · Unidad heredable = el CUERPO, sin tocar la pista.** La pista ya lleva algo del padre al hijo: lo que devuelve `al_parir` viaja en la
  cola y llega a `nace`. El carro-objeto persiste entre cuerpos de un linaje (su memoria de letras es "del linaje"), pero `g` se guarda por
  cuerpo y sólo pasa por ese canal. Es selección y no diseño: un cuerpo con más hijos mete más copias de su `g` (mutadas) en la cola, y los
  cuerpos futuros salen de la cola. *Descartado:* heredar por linaje-carro (sería una sola "g" por linaje y el refundador la perdería igual).
- **D2 · El refundador sortea de la distribución inicial.** ENMIENDA 5 (fundador limpio) dice que nada del objeto viejo pasa; por eso cada
  extinción devuelve al linaje a la zona letal. Consecuencia declarada: `cruza_real` (0 fundadores tras t = 10 000) exige que la selección
  saque al linaje de la zona letal **antes** de t = 10 000 y que no se vuelva a extinguir. P1 es muy difícil por construcción; no se ablanda.
- **D3 · σ = 0.03** (el ejemplo del encargo), fijado sin barrido. **D4 · m40 como carro EVO degenerado** (g 0.40, σ 0): el arnés (b) lo prueba
  == HIBB m40 en la física; así el techo diseñado corre por el mismo código que el candidato.
- **D5 · Sin SINHER del brazo ANCHO** (presupuesto): ANCHO es descriptivo, no entra en la letra.
- **D6 · Lo visto antes de escribir esto:** una prueba de funcionamiento de `evo` y `sinher` en la semilla de PRÁCTICA 41914, T 20 000
  (fuera de serie y réplica): R0 real por linaje evo [0.89, 0, 0, 0.60, 0.67, 0.25, 0.25, 0.14, 0.86], sinher [0.30, 0.03, 0, 0.33, 0.20,
  0, 0.06, 0, 0.75]; hijos por cuerpo con g < 0: 0.0; con g en [0, 0.10): 0.36–0.64. No cambió ningún parámetro; sí informa las p de abajo.
- **D7 · Telemetría del gen fuera del objeto:** como la ENMIENDA 5 reemplaza la instancia en cada refundación, `d['carro']` sólo ve la última.
  La historia de `g` se escribe en un dict de módulo `_TEL[indice]` (sólo escritura; ningún carro lo lee; el runner lo borra antes de cada
  `pista.run` y lo copia después; arnés (f)). No puntúa (ERR-96).

## 4. Instrumento, semillas, T y costo
- `construye_evo.py` (por anclas desde `tronco_v14_3/carros_v143/V143.py` 2a03048a7f1525e5, nueve anclas, cada una exacta una vez), carros en
  `carros/`, runner `corre_evo.py` (la corrida ES `corre_v143.tarea`, importada: regla 14), arnés `identidad_evo.py`. Shas en §10.
- Pista: monocultivo de 9 carros, L 360, 36 objetos, fundador limpio (ENMIENDA 5), T 100 000. Juez `cruza_real`, igual que el muro.
- **Semillas (grep del repo el 28-sep: sin choques):** serie 41001–41020 · réplica 41021–41040 · larga DESCRIPTIVA 41041–41050 · práctica
  (humo, arnés, prueba D6) 41911–41914.
- **Costo:** ~32 s por corrida a T 20 000 en un proceso → ~170 s a T 100 000; serie = 120 corridas ≈ 2 h con Pool 3; réplica igual; larga
  (20 corridas × T 300 000) ≈ 1 h. Python 3.13.12, numpy 2.4.3 (`/root/venv-juaco/bin/python`).

## 5. Medidas
- **Principal:** R0 real y `cruza_real` por linaje (juez); por semilla, mayoría de linajes que cruzan (ENMIENDA 5).
- **Trayectoria de g** (10 ventanas de T/10): g de los PADRES al parir, g de los VIVOS (muestra cada 1 000 pasos) y g de los muertos con sus
  hijos; media y cuantiles 10/50/90. **Paisaje:** hijos por cuerpo y edad por bin de g (ancho 0.05).
- **Pareados** por semilla (mediana del R0 real de los 9 linajes): evo–sinher, evo–v143, sinher–v143, ancho–sinher, ancho–v143, m40–v143,
  evo–m40, o1–v143.

## 6. LA LETRA (`corre_evo.lee_serie`; el arnés la prueba en 11 casos sintéticos)
**Validez (si una falla: NO SE LEE):**
- V1: serie completa (120 corridas, 0 abortos, contabilidad coherente en los 6 brazos).
- V2: el ancla O1 GANA (≥ 15/20 semillas con mayoría de linajes con `cruza_real`).
- V3: V143 en [0.40, 0.80] (mediana del R0 real; la ventana del muro y de TERMO).
- V4: la pieza ACTÚA (`a_no + a_si > 0`, última instancia) en `evo` y en `sinher`.

**Puertas:**
- **P1 (EVO cruza):** `evo` con mayoría de linajes con `cruza_real` en ≥ 15/20 semillas.
- **P2 (EVO le gana al control):** pareado `evo` vs `sinher`, gana en ≥ 15/20.
- **P3 (la selección mueve g a la banda):** en ≥ 15/20 semillas, la media de g de los padres que parieron en la ÚLTIMA ventana
  [90 000, 100 000) (9 linajes juntos) cae en [0.10, 0.60]. Semilla sin partos en esa ventana = no cumple. Como SINHER no puede salir de
  U[−0.10, 0.10], llegar a 0.10 exige acumulación (no basta el sesgo de supervivencia de los fundadores).

**Veredictos:**
- **FUNCIONA:** V1–V4 y P1, P2 y P3.
- **HAY ALGO MODESTO:** P3, más `evo` le gana a `sinher` en > 10/20 con diferencia mediana ≥ 0.10 (la selección encuentra la banda y
  mejora al linaje, aunque no cruce).
- **NO:** todo lo demás (en particular: si g no llega a la banda, aunque EVO le gane al control).
- **Bloque:** si serie y réplica coinciden, vale ese veredicto; si no, vale el menor. NO SE LEE manda.

## 7. Regla de parada
- La réplica (41021–41040) se corre **si la serie no da NO** (encargo). La larga (41041–41050) se corre después, si queda tiempo, y es
  DESCRIPTIVA: sin letra, sólo la curva de g con más generaciones.
- **FUNCIONA** (serie + réplica): "la selección construye el termostato" pasa a ser la vía para TERMO en v14.4 (decide el director).
- **HAY ALGO MODESTO:** se reporta la banda que encuentra y cuánto le falta; no se insiste con variaciones sin hipótesis nueva.
- **NO:** la línea se cierra; se registra si el cuello fue la zona letal (nadie pare) o el refundador (D2).

## 8. Predicciones firmadas (antes del humo)
| # | predicción | rango | p |
|---|---|---|---|
| E1 | V143: mediana del R0 real | [0.35, 0.70] | 0.80 |
| E2 | O1 gana (≥ 15/20) | 17–20/20 | 0.90 |
| E3 | M40: mediana del R0 real / semillas con mayoría que cruza | [0.85, 0.97] / 10–17 | 0.70 |
| E4 | EVO: mediana del R0 real | [0.55, 0.92] | 0.60 |
| E5 | EVO vs SINHER: semillas ganadas / diferencia mediana | ≥ 15/20 / [+0.15, +0.50] | 0.75 |
| E6 | P3: semillas con la media de g de los padres (última ventana) en [0.10, 0.60] | ≥ 15/20 | 0.55 |
| E7 | EVO: media pooled de g de los padres en la última ventana | [0.12, 0.35] | 0.50 |
| E8 | SINHER: mediana del R0 real | ≤ 0.45 | 0.70 |
| E9 | EVO: semillas con mayoría que cruza (P1 exige ≥ 15) | 3–12/20 | 0.60 |
| E10 | Paisaje de EVO: hijos por cuerpo ≤ 0.05 en los bins con g < 0, y el bin [0.10, 0.15) por encima del [0, 0.05) | | 0.80 |
| E11 | M40 le gana a EVO en ≥ 15/20 (la evolución no alcanza al diseño en 100 000 pasos porque cada refundación vuelve a la zona letal) | | 0.65 |
| E12 | ANCHO: media de g de los padres (última ventana) en [0.10, 0.60] y R0 > EVO en la mediana | | 0.65 |
| V | Veredicto de la SERIE: FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE | | 0.15 / 0.45 / 0.25 / 0.15 |
| VB | Veredicto del BLOQUE: FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE | | 0.08 / 0.40 / 0.27 / 0.25 |

## 9. Trampas y riesgos
- **Canal simétrico / acierto sin balancear / sitios fijos:** no aplican (sin pizarra; la medida es el R0 real del juez; posiciones de los rng
  de la pista). **Mundo que se come la comida:** parte del mecanismo; A+C y B+D por linaje como descriptivo.
- **V3:** V143 dio 0.413 en 39001–39010, en el borde. Si cae bajo 0.40 la serie es NO SE LEE aunque EVO cruce. No se cambia la ventana.
- **Riesgo de lectura de P3:** la media de padres es un promedio de pocos partos en semillas con linajes que se extinguen; sin partos, no
  cumple. Es la lectura estricta; se reporta también n por semilla.
- **Vocabulario:** "evoluciona" sólo con la curva de g al lado; nada de "especie" ni "entiende".

## 10. Shas (fijados antes del humo; `corre_evo.SHAS`)
| archivo | sha16 |
|---|---|
| `construye_evo.py` | 6cdd7dd10e9a0594 |
| `carros/V143_EVO_BAJO.py` | 3187b373654e119f |
| `carros/V143_EVO_SINHER.py` | a11989a3b04d13d6 |
| `carros/V143_EVO_ANCHO.py` | 1ff17bf4c6e32382 |
| `carros/V143_EVO_M40.py` | 713cd55ed465cc82 |
| `corre_evo.py` (runner y letra) | 7d8e660a1b0e1a71 |
| `identidad_evo.py` (arnés) | 7e3f6fa48f83c387 |
| origen `tronco_v14_3/carros_v143/V143.py` | 2a03048a7f1525e5 |
| `tronco_v14_3/corre_v143.py` · `pista.py` · `juez.py` · `O1.py` · `revisa_carro.py` | 24100621c450da22 · 9f47c65e438e0ff4 · 6a68f640a7832f12 · 99436afa2715f028 · 1c8a789f7427ab96 |
| `boca_buena/carros/HIBB.py` (ancla del arnés) | 3ca86aed6c409a11 |

- **Arnés** `identidad_evo.py` → **ARNES PASA** (todas las comprobaciones, 388 s; `identidad_evo_salida.txt`): (K) construcción; (a) los 4 con
  EVO 0 == V143 salida entera ×2; (b) M40 == HIBB m40 en la física ×2 y BAJO/SINHER degenerados == HIBB m40; (c) SINHER == EVO hasta el
  primer nacimiento (t 2088) y se separan después; (d) spawn no toca el rng del cuerpo; (e) herencia exacta con σ 0, SINHER no copia,
  G_CLIP y U[−0.10, 0.10]; (f) pieza actúa, determinismo, `_TEL` se borra; (g) verifica, valida, ERR-115, letra 11/11.
- **Humo** (`corre_evo.py --humo`, 41911–41912, T 20 000, un proceso): 6 corridas, 0 abortos, regla 14 OK, ~31 s por corrida
  (`humo_salida.txt`; resumen sha 8dc98dd7bfad1247). Humo NO cuenta.

## 11. Comandos
```
/root/venv-juaco/bin/python experimentos/organelos/termo_evo/construye_evo.py --verifica
/root/venv-juaco/bin/python experimentos/organelos/termo_evo/identidad_evo.py
/root/venv-juaco/bin/python experimentos/organelos/termo_evo/corre_evo.py --humo
/root/venv-juaco/bin/python experimentos/organelos/termo_evo/corre_evo.py --serie --desde 41001 --n 20 --pool 3
/root/venv-juaco/bin/python experimentos/organelos/termo_evo/corre_evo.py --serie --desde 41021 --n 20 --pool 3   # si la serie no da NO
/root/venv-juaco/bin/python experimentos/organelos/termo_evo/corre_evo.py --serie --desde 41041 --n 10 --pool 3   # larga, descriptiva
/root/venv-juaco/bin/python experimentos/organelos/termo_evo/corre_evo.py --bloque <resumen serie>,<resumen replica>
```
