# PREREGISTRO — JUACO-ECO v3: LOS 7 ÓRGANOS DEL FRANKENSTEIN COMO GENES (24-sep-2026, coordinador de la nube; antes de cualquier serie)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/juaco_eco/`. Nivel: **10 (JUACO-ECO)**, frente 2. Dentro de lo que el
director aprobó a las ~11:35 (*"arranca ECO v2 con órganos como genes… réplica no construyas de 0"*): en vez de construir órganos nuevos,
se usan los del **Frankenstein del PC** (`experimentos/frankenstein/`, arnés 33/33), que ya tiene las 7 piezas con interruptor. Archivos
nuevos; el Frankenstein se IMPORTA sin tocarlo. Auditoría propia en §7.

## 0. Instrumento (sha a 16)
- `construye_eco_frank.py` (785b12130022c56b) construye por anclas `motor_eco3.py` (2eec9830792d9822) desde `motor_eco.py`
  (bca3033878b59622) y escribe `carros/FRANK_ECO.py` (92a22cbd1fe314c3), que importa `organismo_frankenstein.py` (baff124177d44e90) y
  aborta si su sha cambia.
- Arnés Python `identidad_eco_frank.py`: **9/9** — órganos apagados = FABRICA_ECO (eco=None y MUT0); los 7 prendidos = el Frankenstein
  TODO del PC; sólo `herencia` prendida = el Frankenstein con sólo herencia (y distinta de todo apagado); cada perilla sigue a su gen en
  cada cuerpo; la mutación prende órganos; checkpoint y reanudación iguales.
- Runner `corre_eco_v3.py` y su arnés `identidad_eco_v3.py` **13/13** (mundos, brazos, órganos; medidas calculadas a mano en los dos
  mundos; la letra por órgano en 8 casos; banderas). El sha del runner va en el log y en `RESUMEN.json`.
- Motor: **Python** (el Frankenstein no tiene gemelo).

## 1. Pregunta
¿La selección elige la ANATOMÍA? El Frankenstein del PC probó a mano: con los 6 órganos juntos vive ~3× más que FABRICA pero no cruza
H-1, y **quitar mapa, curiosidad, modelo o memoria lenta SUBE el R0** (se estorban); herencia e interruptor son los que pesan. Elegir a mano
qué órganos van no funcionó. Aquí cada órgano (y b5) es un gen con umbral que nace apagado; la mutación lo prende; la selección decide.

## 2. Diseño
- **Igual que ECO v2:** vivero con banco de 200 y 8 sombras, mutación (p 0.05, σ 0.15), corte en 60 000, T = 120 000, brazos VIDA
  (selección) y AZAR (deriva). Genoma de 25 genes: las 18 perillas de v1 + `b5, mapa, curiosidad, modelo, lenta, herencia, interruptor`
  (G0 0.9, se expresan si ≥ 1.0).
- **Dos mundos a la vez:** w9 (esc 9: el tamaño de la carrera, 9 fundadores) y w30 (esc 30, 30 fundadores); tope 3 000. En Python no
  caben mundos más grandes a este costo.
- **Nota del mundo (dicha antes):** en la pista v2 cada cuerpo es una instancia nueva del carro; lo que el Frankenstein guarda "del
  linaje" dentro del carro (la opción TD del modelo, Wc de la memoria lenta) vale aquí sólo durante una vida. La herencia (la tabla del
  padre en el parto) sí cruza entre cuerpos.
- **Semillas nuevas** (grep del 24-sep: sin usos 20110–20199): serie **20111–20130**, réplica **20131–20150**, práctica 20191–20199.

## 3. Medidas
Por órgano y por mundo, en el banco del corte: (+, −) contra sus 8 sombras en VIDA y en AZAR; fracción del banco con el órgano expresado
en VIDA y en AZAR (pareado por semilla). Descriptivo: perillas seleccionadas, persistencia en T.

## 4. Predicciones firmadas (coordinador, con las ablaciones del Frankenstein a la vista)
| órgano | lo que espero en w30 | en w9 |
|---|---|---|
| **herencia** | ELEGIDO (p 0.70) | ELEGIDO (p 0.50) |
| interruptor | ELEGIDO o sube (p 0.50) | sube (p 0.40) |
| mapa, curiosidad, modelo, lenta | neutros o DESCARTADOS (DESCARTADO p 0.25 cada uno) | neutros |
| b5 | neutro (p 0.80) | neutro |
Veredicto: FUNCIONA 0.45 · MODESTO 0.30 · NO 0.20 · NO EVALUABLE 0.05.

## 5. Qué refuta
- **H (la selección elige órganos):** ningún órgano queda ELEGIDO en los dos mundos.
- **El instrumento:** AZAR saca algún gen de sus sombras (> 8/20).

## 6. Criterio por la letra (`corre_eco_v3.veredicto`; se imprime al final)
Por órgano g y mundo m (20 semillas):
- **ELEGIDO:** en VIDA, g por ENCIMA de sus sombras en ≥ 15/20 (O1+) y el banco de VIDA lo lleva expresado en más que el de AZAR en
  ≥ 15/20 (O2+).
- **DESCARTADO:** por DEBAJO de sus sombras en ≥ 15/20 (O1−) y el banco de VIDA lo lleva en menos que el de AZAR en ≥ 15/20 (O2−).
- "sube" / "baja": sólo O1+ / O1−. "neutro": ninguno.
Veredicto de la serie:
- **NO EVALUABLE:** serie incompleta; bloqueados > 0; AZAR con > 8/20 en algún gen de algún mundo.
- **FUNCIONA — LA SELECCIÓN ELIGE ÓRGANOS:** algún órgano ELEGIDO en los dos mundos.
- **HAY ALGO MODESTO:** algún órgano ELEGIDO en un solo mundo, o que "sube" (o ELEGIDO) en los dos.
- **NO:** ningún caso anterior (sólo DESCARTADOS o neutros).
El bloque se declara sólo si serie y réplica dan el mismo veredicto; si no, vale el menor. La ANATOMÍA por mundo se imprime siempre.

### Vocabulario
- Permitido: «la selección elige/descarta el órgano», «anatomía elegida en el mundo X», «linaje», «cuerpos vivos (N = …)».
- Prohibido: «evoluciona», «especie», «cultura», «vida artificial abierta».

## 7. Auditoría propia (antes de correr)
1. **Siete órganos, dos mundos:** con p = 1/9 por gen bajo neutralidad, P(≥ 15/20) es ~1e−10: no hay riesgo de un ELEGIDO por azar.
   La guardia de AZAR sobre 25 genes × 2 mundos × 2 signos da ~3 % de NO EVALUABLE espurio; se acepta.
2. **Epistasis:** un órgano puede servir sólo con otro (p. ej. el mapa sin el interruptor). El veredicto no la mide; la anatomía impresa
   sí la deja ver. Se lee, no se declara.
3. **Órganos de linaje que aquí son de una vida** (modelo, lenta): si salen DESCARTADOS, puede ser por el mundo (§2), no por el órgano.
   Se dirá así.
4. **Mundo chico (w9):** 9 fundadores y pocos nacimientos; la deriva manda más. Por eso MODESTO acepta un solo mundo.
5. **Arrastre:** un órgano puede subir pegado a buenas perillas; O2 contra AZAR lo acota (en AZAR no hay herencia del genoma).

6. **(hallado en el humo, antes de la serie) Bancos de composición distinta:** en AZAR cada genoma nuevo es una copia mutada de una
   entrada al azar, así que los órganos se prenden por pura deriva y su fracción en el banco sube con el tiempo (humo: `herencia` 27 %,
   `mapa` 29 %); en VIDA el banco son pocos padres exitosos (humo: ~0 %). O2+ ("VIDA lleva más el órgano que AZAR") queda así sesgado
   EN CONTRA de VIDA: es conservador para ELEGIDO. O2− queda sesgado A FAVOR de DESCARTADO, y por eso DESCARTADO exige también O1− contra
   las sombras, que comparten la genealogía y controlan esa composición. La letra no cambia; se escribe para leer bien el resultado.

## 8. Costo (medido: el Frankenstein cuesta ~1.9× FABRICA en Python)
Estimado ~1 min (w9) y ~3–5 min (w30) por corrida → ~3 h de CPU por serie, ~1 h con Pool 3.

## 10. ENMIENDA 1 (24-sep, ~13:00 UTC, ANTES de cualquier serie de v3) — candidato nube-8
- **Qué pasó:** la serie de ECO v2 (otro paquete, mismo tipo de gen) mostró que comparar la MEDIA del gen en el banco con la de sus 8
  sombras (O1 de §6) no detecta bien la selección de un rasgo con umbral: la selección sólo empuja el gen a pasar 1.0 y las sombras neutrales
  derivan libres (en v2, w90 y w270: 98–99 % del banco expresando `ensena` y aun así O1 = 12 y 13/20).
- **Qué cambia en v3 (instrumento, no mecanismo):** el runner toma del checkpoint del corte (t = 60 000; es el estado completo, con el banco
  de pares genoma–8 sombras) la fracción del banco que EXPRESA cada órgano en el genoma real y en cada sombra. La letra de ELEGIDO pasa a:
  - **O1\*:** en VIDA, la fracción que expresa el órgano supera a la MEDIA de las fracciones de sus 8 sombras (estricto) en ≥ 15/20.
    Bajo la nula (sombras e real intercambiables; humo: ~38 % de sombras prendidas por deriva) esto pasa con p ≈ 0.4 por semilla:
    P(≥ 15/20) ≈ 1e−3.
  - **O2** sin cambios. **ELEGIDO = O1\* + O2.** "sube" = uno de los dos. **DESCARTADO pasa a descriptivo** ("baja"): con órganos que
    nacen apagados y sombras que se prenden por deriva, "el real por debajo de la media de sus sombras" pasa ~60 % de las veces bajo la nula.
  - Guardia nueva: si AZAR expresa por encima de sus sombras en ≥ 15/20 en algún órgano, NO EVALUABLE.
  - El O1 original (media contra sombras) se sigue imprimiendo como descriptivo.
- Runner `corre_eco_v3.py` **7bb44da802508b37**; arnés `identidad_eco_v3.py` **375bf7644a557118**: **14/14** (nuevo (S): el real del checkpoint coincide con el banco
  del motor en los 7 órganos, con 8 sombras cada uno).

## 9. Humo (24-sep, 12:18 UTC, Python; números sin valor)
`corre_eco_v3.py --humo` (20196, w30, T 20 000, corte 10 000): 74 s (36–38 s por brazo). VIDA persiste (1 vivo, máximo 37); banco con
órganos ~0 (modelo 0.012, interruptor 0.006); ningún órgano sale de sus sombras. AZAR se extingue; banco con `mapa` 0.29, `herencia` 0.27,
`modelo` 0.16, `curiosidad` 0.11; `herencia` +1 contra sombras en esa semilla. Carpeta `datos/humo/eco_v3_humo_python_20260924_121847`.
Enmiendas tras el humo: ninguna a la letra; el punto 6 de §7 es una nota de lectura.
