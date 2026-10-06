# Entrega 1 — El Reactor (1-oct-2026)

Autor: juaco-investigador (solo lectura; no corrió series; leyó JSON ya guardados de o1_libre), revisado por la sesión "Investigación y exploración".
Revisión: comprobé en `o1libre` `PREREGISTRO_o1_libre.md:63,241,244,286`, `carros/O1_LIB.py:203-205` (los 14 genes mutan en cada parto), `CIERRE_o1_libre.md:22` y `corre_o1_libre.py:80,178-186`: coinciden. Lo demás NO lo recalculé. Las citas de literatura van de memoria del investigador: ninguna se abrió hoy.

**Correcciones posteriores (1-oct, trazabilidad pedida al investigador):**
- "Ne por linaje 8.1–8.5" es `fila.siembra_info.Ne_linajes` de los `pasaje_i*_{lib|neu}_p*.json` (fórmula en `corre_o1_libre.py:191`): es Ne de LINAJES (máximo 9), no de cuerpos. El "Ne·s ≈ 0.5" hereda esa definición.
- "Colonia 116–162 por pasaje" NO es un rango: son dos medianas de `fund_colonia` en la serie, pasajes p01–p02 (neu 116, lib 162). Con los tres pasajes: serie lib 215.5, neu 132; réplica lib 273, neu 175.
- "fund_de_siembra mediana 9" es sólo de la serie, p01–p02.
- F0 medido aparte por la sesión "JUACO 5" (neutro, siembra_final): mediana 11.5 en serie (8.7–16.2; 2 de 10 índices pasan de 15) y 12.0 en réplica (9.3–13.4). La predicción n ≤ 15 se cumple por mediana; nada cerca de 100.

**Veredicto: EN PARTE, tirando a SÍ.** La literatura explica el NO de o1-libre sin recurrir a "la selección no inventa": el montaje tiene 9 cuerpos, un cuello de 9 genomas por pasaje, todos los genes mutando en cada parto y pocas generaciones efectivas. No explica por sí sola por qué "los tres juntos" no suman; eso es diseño, no selección.

Marcas: [V] = leído en repo o datos; [I] = inferencia; [L] = literatura citada de memoria, sin abrir la fuente hoy.

## 1. Condiciones de la literatura frente a nuestro montaje (o1_libre)

Rutas: `OL` = `C:\Users\User\Documents\PROYECTOS\JUACO\o1libre\experimentos\organelos\o1_libre\`; `ORG` = `C:\Users\User\Documents\PROYECTOS\JUACO\organelos\`.

| Condición | Fuente [L] | ¿La tenemos? | Número a cambiar |
|---|---|---|---|
| La selección sólo ve s > 1/Ne | Kimura 1962 (Genetics 47:713); Ohta 1973 | **No.** Censo de 9 cuerpos (`OL\PREREGISTRO_o1_libre.md:63`). Ne por linaje medido 8.1–8.5 [V, JSON de pasajes]. Ventaja de MEM: mix − mixA ≈ +2.7 nacimientos sobre ~50, s ≈ 0.05 [I] (`OL\CIERRE_o1_libre.md:22`). Ne·s ≈ 0.5: casi neutro. | N de 9 a ≥ 300–500 cuerpos (Ne·s ≥ 10 para s = 0.03) |
| Sin cuello estrecho entre rondas | Avida, N = 3600 continuo (Lenski et al. 2003, Nature 423:139) | **No.** Se sortean 90 partos (`OL\corre_o1_libre.py:80,178-186`), con 18–30 padres distintos (mediana 24) [V]; el preregistro extrapolaba 40–65 (`:286`). De los 90 sólo 9 fundan (fund_de_siembra mediana 9); el resto entra por colonia (116–162 por pasaje) [V]. | Quitar los pasajes: una corrida continua |
| Muchas generaciones | Avida ~10⁴; LTEE Cit+ a ~31 500, 1 de 12 (Blount 2008, PNAS 105:7899) | **No.** Declarado ≈ 150 en 3 pasajes (`:241`). El neutro acaba en 0.055–0.088 por poder (`OL\serie_pool2.log:107`). Con σ 0.03 y paseo recortado en 0, eso equivale a **≈ 5–13 pasos mutacionales** [I]. | ≥ 10³ generaciones reales; medir profundidad, no nacimientos |
| Tasa de mutación bajo el umbral de error (L·μ < ln de la ventaja) | Eigen 1971 (Naturwiss. 58:465); Drake 1991; Avida ≈ 0.2 por genoma | **No.** Los 14 genes mutan en cada parto (`OL\carros\O1_LIB.py:203-205`). Carga ≈ 4.6 % de R0 por generación, con R0 ≈ 0.9–0.98 (`:288-291`). | Un gen por parto (p = 1/L ≈ 0.07), U ≈ 0.1–0.3; conservar el tamaño del paso con cola larga |
| Escalones intermedios pagados | Lenski et al. 2003: EQU 23/50 con 9 funciones pagadas, 0/50 pagando sólo EQU | **A medias.** La moneda es sólo partos (`corre_o1_libre.py:11-13`). Cada poder es una pendiente sin valle (`:14-17`), pero con visión total MEM paga poco (`:101-102`). El caso con valle (llave→nuez) dio NO (`ORG\experimentos\organelos\escalera\ESCALERA.md:18`). | Pagar el paso A solo (≥ 0.1–0.2 del pago final) |
| Mutantes deletéreos tolerados como escalón | Covert et al. 2013 (PNAS 110:E3171) | **No se sabe.** La moneda de 25k purga y la de 100k con establecidos conserva (`ORG\registro\REGISTRO_etapas_1_2.md:7435-7441`). | N grande y sin cuello dejan vivir al intermedio |
| Duplicación y divergencia | Ohno 1970; Bergthorsson 2007 (PNAS 104:17004); Blount 2012 (Nature 489:513) | **No en o1_libre** (14 floats fijos, sin recombinación). **Sí en BLOQUES** (dup 0.02, borrar 0.05, insertar 0.02, HGT 0.01, mutar 0.10 por regla: `ORG\experimentos\organelos\bloques\opusM\PREREGISTRO_bloques.md:25-27`). BQ2 quedó clavado en 2 reglas (`REGISTRO:7438`). | Genoma de largo variable con sesgo neto ≥ 0 y reglas silenciosas |
| Redes neutrales | Wagner 2008 (Proc. R. Soc. B 275:91) | **No.** Perillas continuas: casi todo cambio es visible o es carga. | Igual que arriba |
| Cruce de valles; la recombinación ayuda sólo con N grande | Weissman 2009 (TPB 75:286) y 2010 (Genetics 186:1389) | **No.** Con 2–5 cuerpos vivos la recombinación resta (nietos 578 vs 772: `REGISTRO:7423-7424`). | Sexo sólo después de N ≥ 300 |
| Selección de grupo que pague | Ratcliff 2012 (PNAS 109:1595); Maynard Smith y Szathmáry 1995 | **No.** P2 cerrado en 5 humos (`ESCALERA.md:225`). | Esperar al Reactor |
| Diversidad mantenida, objetivos engañosos | Lehman y Stanley 2011; Mouret y Clune 2015; Wang et al. 2019 (POET) | **No.** 9 nichos idénticos. | Islas con migración baja |

**BLOQUES sí fijó un órgano con N ≈ 37** (`REGISTRO:7119-7131,7141`). No fue por tamaño. Fue porque el 96–99 % de las muertes eran veneno y sal (s enorme, `PREREGISTRO_bloques.md:42`) y el órgano está a una sola inserción de distancia. Ningún experimento del repo ha mostrado una innovación de dos pasos: la doble regla salió 0/45 (`REGISTRO:7437`). Ése es el hueco que el Reactor debe atacar.

## 2. El Reactor, con números

- **Motor: ECO compilado, no la pista v1.** El gemelo numba hace 1.4–1.9 µs por cuerpo y paso con 75–100 cuerpos, ×38–48 (`ORG\experimentos\juaco_eco\datos\identidad_eco_rapido_salida_20260924_1025.txt:167-169`). BLOQUES midió 63.5 s por 500k pasos (`PREREGISTRO_bloques.md:157`).
- **Por qué no v1:** O1 en Python cuesta 2.1–2.3 ms por paso con 9 cuerpos (`OL\PREREGISTRO_o1_libre.md:244`), unos 250 µs por cuerpo y paso. El gemelo no admite O1 (`ORG\experimentos\juaco_eco\motor_eco_rapido.py:40-42`) y O1 no vive en v2 (`ESCALERA.md:171`). La v1 tiene un cuerpo por linaje (`ORG\experimentos\juaco_eco\motor_eco.py:9-10`). La única vía a "cientos" en v1 es la ficha F4.
- **Población:** 400–500 cuerpos vivos. Hace falta esc ≈ 900–1200 y subir `tope_cuerpos` de 300 (`motor_eco.py:32`). Corrida continua con vivero finito; sin pasajes.
- **Mutación:** las tasas de BLOQUES (U ≈ 0.2–0.4 por parto con 2–4 reglas), con p_dup + p_ins ≥ p_del.
- **Moneda:** descendencia dentro del mundo (K, persistencia, nietos de `individuos`, `motor_eco.py:59`). Ningún juez en el bucle.
- **Recombinación:** apagada al inicio; se conserva el HGT de una regla. `mundo_familia.py` queda para después.
- **Escalones:** cada subfunción paga sola (ficha F3).
- **Cómputo:** 500 cuerpos × 2M pasos × 2–4 µs ≈ 35–65 min por corrida y núcleo. 80 corridas con 14 procesos ≈ 4–6 h. **Supone costo lineal en esc, no verificado.**

**Qué falta construir:**
- ECO a esc ~1000 con el tope subido.
- En `ORG\experimentos\carrera_escuderias\pista_pob.py:9-18` el depósito es por índice de linaje: K copias dan 9 acervos de tamaño K, no uno de 9K.
- `ORG\experimentos\organelos\condiciones\entre_linajes\camara_linajes.py:8-14` coloniza sólo dentro de una pista.
- `ORG\experimentos\organelos\o1_evo\grande\pista_grande.py:8` alarga el anillo; no se vio que añada linajes.

## 3. Fichas, por valor/costo

**F0. Reloj y Ne·s reales de o1_libre (0 CPU).**
- Hipótesis: el NO salió de ≤ 15 generaciones efectivas y Ne·s < 1.
- Mecanismo: ninguno nuevo. En el brazo neutro, E[(g − fábrica)²] = σ²·n sobre los 10 genes sin recorte da n directo.
- Predicción: n ≤ 15 en 3 pasajes, en serie y réplica.
- Control que puede ganar: n ≥ 100; entonces esta lectura cae y el NO pesa más.
- Instrumento: `OL\datos\serie_*\pasaje_*.json`. Costo: minutos.
- Nivel: ninguno; decide si F1–F4 valen. Probabilidad 0.7.

**F1. Barrido de tamaño en BLOQUES (esc 90 frente a 900).**
- Hipótesis: con N ×10 se fijan más formas de regla funcionales distintas.
- Mecanismo: motor de BLOQUES sin cambios; memoria nueva: ninguna.
- Predicción: ≥ 2 formas fijadas (≥ 50 % de los vivos) en ≥ 12/20 semillas a esc 900, contra ≤ 5/20 a esc 90.
- Control que puede ganar: esc 90 iguala (N no es el límite); BLOQ_AZA sin herencia.
- Instrumento: `ORG\experimentos\organelos\bloques\opusM\corre_bloques.py`. Sirve además de humo de costo.
- Costo: 60 corridas, ~3–5 h con 14 procesos.
- Nivel: punto 14 (criterio de emergencia). Probabilidad 0.45.

**F2. Mutación de un gen por parto en el montaje de pasajes.**
- Hipótesis: la carga, no la selección, tapa la subida.
- Mecanismo: cada parto muta un gen al azar (σ igual); nada más.
- Predicción: R0 del neutro ≥ 0.90 (hoy 0.62–0.80) y lib ≥ o1 en la suma de cruces.
- Control que puede ganar: el montaje actual; además "÷10 = PURGA" sugiere que con menos carga la selección borra antes de sumar.
- Instrumento: `OL\construye_o1_lib.py` y `OL\corre_o1_libre.py`.
- Costo: ~4 h con pool 2 por serie. Probabilidad 0.3 de conquista, 0.7 de que el neutro deje de degradarse.

**F3. Escalón pagado en llave→nuez (la prueba de Avida).**
- Hipótesis nueva sobre línea cerrada: la secuencia no se armó porque el primer paso valía 0.
- Mecanismo: K sola da +0.1 o +0.2; genoma de BLOQUES; N ≈ 400.
- Predicción: secuencia K→nuez en ≥ 50 % de los vivos en ≥ 10/20 semillas con K pagada, contra ≤ 2/20 con K = 0.
- Control que puede ganar: K = 0 a N grande; si empata, bastaba N y sobra el escalón.
- Instrumento: gemelo ECO más el mundo `enriquecido` (ruta no localizada).
- Costo: 3 brazos × 20 semillas × ~1 h, ~5 h con 14 procesos, más construcción.
- Nivel: etapa 8 del punto 16 y punto 14. Probabilidad 0.35.

**F4. Reactor v1 para una perilla de la Escalera.**
- Hipótesis: en el mundo de P1 (s grande: 79 vs 7) la selección sube LUGAR_W desde 0 si el acervo es de cientos.
- Mecanismo: `pista_pob` con K = 32 (288 cuerpos), depósito cruzado entre índices, colonización de `camara_linajes`, corrida continua de 300k.
- Predicción: LUGAR_W sel − neutro ≥ 0.15 en ≥ 8/10; con K = 1, no.
- Control que puede ganar: K = 1 y PS_LEE 0.
- Costo: 32 × 2.2 ms ≈ 70 ms por paso, ~6 h por corrida; 30 corridas con 15 procesos ≈ 12 h.
- Nivel: plan de la mañana punto 3 (`ORG\registro\ESTADO.md:57`). Probabilidad 0.4.

## 4. Lo que no vale la pena (libre)

- Más cadenas de 3 × 100k con 9 cuerpos, o más poderes como perillas: mismo Ne·s.
- Bajar σ sin subir N: ya dio PURGA.
- Novelty search, MAP-Elites o POET como motor: exigen archivo y descriptor externos, que no son reglas locales; sirven como medida.
- Sexo antes de N ≥ 300, y P2 antes del Reactor.
- Esperar un evento tipo Cit+: fue 1 de 12 con N ~10⁷ y 31 500 generaciones.

## No verificado

- Ninguna cita se abrió hoy; van de memoria, incluidos DOI y cifras.
- s ≈ 0.05 de MEM y las 5–13 generaciones efectivas son inferencias; F0 las mide.
- No se sabe si el costo del gemelo escala lineal a esc ~1000.
- No se sabe si `pista.run` acepta más de 9 carros.
- No se conoce el K ni la causa del NO de pista_pob del 29-sep.
- No se leyeron `BITACORA.md`, `HORIZONTE_frontera.md`, `INDICE.md` ni `LABORATORIO.md`.
