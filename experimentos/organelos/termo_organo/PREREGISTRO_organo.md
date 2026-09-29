# SONDA EXPLORATORIA (no preregistro confirmatorio) — ORGANO de ECO sobre V143_TERMO en la pista de la carrera (28-sep-2026, 20:16)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Encargo del coordinador: sonda rápida (≤ 3 procesos, sin Pool) para decidir el plan de mañana.
Pregunta del director: "con lo que sabemos, ¿nos acercamos a romper el muro?"

Escrito DESPUÉS del arnés (sólo identidad y disparos por letra) y ANTES de mirar cualquier número de la sonda (las 20 corridas ya corren).

## 0. ¿Aplica? (paso 1 del encargo)
- La pista de la carrera (`carrera_escuderias/pista.py`, la que usan corre_termo/corre_muro2) y ECO (`generaciones/pista2.py`, la de
  motor_bloques) toman PAT, VAL_VIVO y EFECTO del MISMO `organismo_f9c` (F9C.PAT, vía `cfg_fabrica()`): A [1,1,0,1,0,0] comida,
  B [1,0,1,0,1,0] veneno, C [0,1,1,0,0,1] agua, D [0,0,1,0,1,1] sal. Ninguna de las dos baraja letras ni píxeles por semilla
  (`pat_shuf 0`, `nec_shuf 0`, `invertir_en None` en RAMAS; la pista sólo sortea QUÉ letra aparece, `TIPOS[rng]`).
- Por lo tanto el píxel 1 (ausente EXACTAMENTE en B y D) significa lo mismo en la pista. **APLICA.**

## 1. Hipótesis
El muro de la pista es el establecimiento (97–99 % de los fundadores mueren de veneno o sal antes de parir). Si cada cuerpo nace con el
instinto de rechazo que la selección fijó en ECO, el fundador deja de morir envenenado y el linaje se establece con menos fundadores.

## 2. Mecanismo y memoria nueva
- Órgano = el genoma evolucionado de BLOQ_V (FORZ2_V: linaje 66 de s48402): 2 × (píxel 1 del objeto en la celda < 0.06 → boca −2.97),
  peso total −5.94, sumado a Vb antes del sigmoide de la boca de fábrica (como `motor_bloques`: `Vb += _reglas_boca`), antes de FILTRO,
  APR y TERMO. Innato en todos los cuerpos (constante del carro). Cero memoria nueva (sólo contadores de telemetría). Sin rng.
- Control desfasado (ORGANO 2): la misma regla con el píxel 0 (ausente en C agua y D sal: una buena y una mala; no separa lo malo).

## 3. Instrumento y anclas
- `construye_organo.py` (5 anclas desde `termo/carros/V143_TERMO.py` sha 3db639cab75641fb) → V143_TERMO_ORG0 (dda120a17ab10bb5),
  V143_TERMO_ORG (900d9c1121430352), V143_TERMO_ORGDES (829de9a2b9e8bae5); `--verifica` IGUAL; revisa_carro PASA.
- `corre_organo.py` (998a822c4fa414f7): la corrida ES `corre_termo.tarea` importada (== corre_v143.tarea: 9 carros iguales, L 360,
  36 objetos, fundador limpio, T 100 000) y verifica los shas que fija corre_termo.
- Arnés `identidad_organo_salida.txt`: ORGANO 0 == V143_TERMO bit a bit (salida entera sin 'seg'); ORGANO 1 y 2 difieren; el órgano
  dispara sólo en B y D (687/391, A 0, C 0); el desfasado sólo en C y D. PASA en 174 s.

## 4. Brazos y semillas NUEVAS
termo (V143_TERMO) · org (V143_TERMO_ORG) · orgdes (V143_TERMO_ORGDES) · o1 (O1, ancla). Semillas 49851–49855 (grep: libres; 4985x
sólo aparece como números sueltos en JSON viejos), arnés/humo 49856. T 100 000. 3 procesos sin Pool.

## 5. Medidas
fundadores por linaje (mediana; y sólo linajes establecidos = sin fundador después de t 10 000); R0 real mediana; mayoría que cruza
(semillas con > 50 % de linajes que cruzan R0 real 0.9); causas de muerte de los fundadores (`corre_termo.cuerpos`, origen 0).

## 6. Predicciones firmadas (antes de mirar)
| # | cantidad | predicción | p |
|---|---|---|---|
| S1 | fracción de muertes de fundadores por veneno+sal, org | < 0.30 (termo > 0.80) | 0.75 |
| S2 | fundadores por linaje, mediana, org | ≤ 1/3 de la de termo | 0.60 |
| S3 | R0 real mediana org > termo pareado | ≥ 4/5 semillas | 0.45 |
| S4 | mayoría que cruza, org | ≥ 4/5 (termo 3/5 esperado) | 0.40 |
| S5 | orgdes: R0 real mediana < termo, más muertes por sed | ≥ 3/5 | 0.65 |
| S6 | riesgo: org muere de hambre/sed porque el anillo se llena de B/D (lo visto en ECO) | fracción hambre+sed de todos los cuerpos org > termo | 0.55 |

## 7. Qué refuta / control que puede fallar
- El trasplante no acerca si fundadores por linaje no baja o si R0 real org ≤ termo. Si orgdes iguala a org, lo que actúa no es separar
  lo malo sino morder menos.
- Trampas: (1) org y orgdes difieren sólo en el píxel; (2) sin clasificación, conteos pareados; (3) mundo que se come la comida: se mira
  la composición/causas (S6); (4) sitios fijos: las letras tienen significado fijo en ambos mundos — es un INSTINTO, no aprendizaje, y
  el órgano lo trasplantamos a mano (la evolución lo armó en ECO, no en la pista).

## 8. EXTRA POST HOC (escrito a las 20:32, DESPUÉS de ver 11 corridas de la sonda y ANTES de correr este brazo)
- Visto: org (órgano tal cual) R0 real ~0.13, ~74 fundadores por linaje, fundadores mueren de HAMBRE/SED (vida 600 = la dote); el anillo
  es ~90 % B+D en todos los brazos (también termo y O1 en la serie TERMO): morder veneno LIMPIA y es la vía a la comida.
- Brazo post hoc `orgcond` (V143_TERMO_ORGCOND, `construye_organo_cond.py`, desde ORG0 dda120a17ab10bb5; diseño NUESTRO, no evolución):
  el mismo órgano sólo actúa si la necesidad activa del carro > 0.5; saciado, V143_TERMO (limpia). 3 semillas 49851–49853, pareadas con termo.
  Arnés: ORGANO 0 de este constructor == V143_TERMO bit a bit (`identidad_cond_salida.txt`).
- Predicción: R0 real orgcond > termo pareado en ≥ 2/3 (p 0.35); fracción de fundadores muertos por veneno+sal < termo (p 0.70).

## 9. Números (20:47; `datos/sonda_T100000/`, `datos/lee_sonda.txt`, `datos/sonda_T100000/RESUMEN.json`)
| brazo | R0 real med | mayoría cruza | refundaciones/linaje med (establecidos) | fundadores muertos por veneno+sal | A+C en el anillo (de 36) |
|---|---|---|---|---|---|
| termo | 0.872 | 1/5 | 4 (1; 36 linajes est.) | 0.99 | 3.2 |
| org | 0.135 | 0/5 | 74 (0 establecidos) | 0.00 (hambre 0.61, sed 0.39) | 1.4 |
| orgdes | 0.000 | 0/5 | 204 (0) | 0.37 (sed 0.42, hambre 0.21) | 18 (C acumulada) |
| o1 | 0.941 | 5/5 | 0 (0; 38) | 0.97 | 2.1 |
| orgcond (post hoc, 3 sem.) | 0.168 | 0/3 | 104 (3 est.) | 0.81 | 2.2 |
Predicciones: S1 acierta (trivial) · **S2 REFUTADA** (74 vs 4) · **S3 REFUTADA** (0/5) · **S4 REFUTADA** (0/5) · S5 acierta (5/5) · S6 acierta ·
post hoc: R0 orgcond > termo **REFUTADA** (0/3); veneno+sal de fundadores < termo acierta (0.81 vs 0.99).
Errores de instrumento: E1 `limpia()` reemplazaba nombres en orden y 'V143_TERMO_ORG' se comía 'V143_TERMO_ORGC0' → falso False en el arnés
del constructor cond (`identidad_cond_salida_E1_falso.txt`); arreglado (nombres largos primero) y repetido: True. E2 los disparos del órgano
son de la ÚLTIMA instancia de cada linaje (sólo signo). E3 "fundadores por linaje" = campo `fundadores` del juez = refundaciones (cuerpos
fundadores − 1).
