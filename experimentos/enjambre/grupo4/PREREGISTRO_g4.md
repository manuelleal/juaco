# PREREGISTRO (borrador) -- grupo4 / M4, "oráculo de laboratorio" en versión en-organismo

**18 sep 2026, madrugada. Mini-equipo 4 (enjambre), diseñador+implementador en uno. Borrador -- falta la confirmatoria
del coordinador (20 semillas nuevas, con Pool) antes de que esto cuente como preregistro real.**

## Hipótesis
Una vía lenta que, en vez de un vector de pesos lineal (`Ws`, delta rule), mantiene una **tabla por grupos de
píxeles de grado `g`** (g=1: 6 canales elementales; g=2: 15 pares) con un **estadístico de competencia** por grupo
(evaluado *antes* de actualizar la celda, para no filtrar el dato consigo mismo) y una lectura **WTA dura o mezcla
softmax**, puede *construir* el rasgo conjuntivo de `xor01` (el par de píxeles (0,1)) con reglas puramente locales
-- cada grupo usa solo sus propios píxeles, su propia celda de tabla y el error de la mordida -- sin gradiente ni
señal global, y hacerlo en pocas exposiciones.

## Mecanismo y memoria
`organismo_g4.py` (por anclas desde `experimentos/creacion_A/organismo_v13q5.py`, `fae9c32b146fdbb4`, solo lectura)
agrega la perilla `tabla_g=None|dict(g,estad,modo,tau,eta,rho,alpha,clip)`. Con `tabla_g=None` es v13q5 exacto
(identidad 13/13, ≥9 exigidos, T=30000, comparación por las 50 claves originales -- ver `identidad_g4.py`). Con
`tabla_g` activo, la vía lenta lee y aprende por tabla+competencia en vez de `Ws`/`Wps`/`Wns`; el estado nuevo
(`_g4_tabla`, `_g4_ecomp`) vive solo dentro de esa corrida del organismo, no hay bucle externo en tiempo de
ejecución. `banco_g4.py` repite el mismo cálculo *fuera* del organismo sobre el flujo `(t,patrón,R,residuo)`
harvestado (`lab=True`); el residuo es exactamente la señal que la tabla consume in-loop, así que el replay es el
control positivo del mecanismo (ver resultados).

## Alcance declarado (para no inflar lo que no se corrió)
Implementado: g∈{1,2} (no 3), estimador SOLO 'tabla' (EMA; no tabla_binaria ni mínimos cuadrados recursivos por
celda), estadístico ∈{mse propio, desacuerdo de signo} (no cobertura ni primer-encuentro), lectura ∈{dura, mezcla
softmax con τ∈{0.5,2.0}}. Búsqueda externa (`meta_regla2_g4.py`) sobre esa rejilla reducida: 432 configuraciones,
no las ~15000 de la especificación completa del mecanismo.

## Predicción numérica
**Del jefe de investigación** (a reencontrar por la búsqueda, no dada por buena de antemano): g=2+tabla+error
propio+ganadora dura, mediana 1.000, n*≈8; ganadora de la búsqueda en 1-10 sobrevive a 11-20 con mediana ≥0.875; en
el organismo, ≥0.75 en ≥11/20 semillas nuevas con n*≤40; la búsqueda coloca g=2 en primer lugar y deja g=1 y g=3
fuera del top-10 (yo no puedo verificar la parte de g=3: no lo implementé).

**Mía, corregida con lo que de verdad corrió (ver `mini_g4.json` y `meta_regla2_g4.json`):**
- acc_lenta xor01 (in-organismo, semillas 1-3, T=100000): **0.8125, 0.75, 1.0** (mediana 0.8125) -- las 3/3 semillas
  cruzan el criterio ≥0.75. Baseline apagado (A-4 exacto, mismas semillas): 0.5, 0.3125, 0.5625 -- replica lo ya
  medido esta noche (0.50-0.63).
- px0: **1.0, 1.0, 1.0** -- cumple px0=1.000.
- azar: **0.5, 0.2, 0.5** (mediana 0.5, dentro de [0.35,0.65]) -- **pero la semilla 2 (0.2) queda FUERA de la banda**;
  con solo 3 semillas esto no es una lectura confiable todavía (ver riesgos).
- exposiciones hasta 0.75 (vía replay sobre el flujo harvestado, REJ del proyecto): n*=10, 20, 10 -- muy por debajo
  del n*≤40 que pedía el jefe, y del mismo orden que el n*≈8 que predijo.
- abre el rasgo conjuntivo correcto (par (0,1)) en **3/3 semillas de xor01**, con DOS configuraciones de
  hiperparámetros distintas (la mía inicial y la ganadora de la búsqueda ciega) -- incluida en ambas.
- **Búsqueda ciega (`meta_regla2_g4.py`, semillas 1-10 de `lab_eventos_cuadratica_xor01.json`, reporta en 11-20
  retenidas, sin que yo tocara ese archivo ni lo generara):** el top-10 completo de 432 configuraciones es
  g=2+mse+dura (confirma la predicción del jefe en la parte que pude probar); ganadora búsqueda=1.000,
  retenidas mediana=1.000 (mín 0.625, máx 1.000) -- sobrevive el cambio de semillas. Mi hipótesis inicial
  (eta=.15,rho=.05,clip=10,alpha=1) quedó en el puesto 16/432 (retenidas mediana 1.0 pero mín 0.312: más variable
  que la ganadora real). Validé la ganadora de la búsqueda EN EL ORGANISMO (no solo en replay) en xor01,
  semillas 1-3: idéntica a mi hipótesis inicial en estas 3 semillas (0.8125, 0.75, 1.0; n*=10,20,10; abre (0,1)
  3/3) -- la elección exacta de eta/rho/clip/alpha pesa menos que la estructura (tabla g=2 + mse + dura).
- Tronco (delta lineal clásico, mismo flujo, semillas retenidas 11-20): nunca cruza 0.65 ni 0.75 hasta 600 eventos
  (mediana tope ~0.47-0.5). El contraste con M4 es limpio.

## Control que puede fallar (y lo que pasó)
1. **Cambio de semillas (búsqueda 1-10 → retenidas 11-20):** hecho, sobrevive (mediana 1.0→1.0).
2. **Cambio de mundo:** px0=1.000 en las 3 semillas in-organismo; azar mediana 0.5 pero con una semilla fuera de
   banda -- **no puedo declarar este control superado con solo 3 semillas**, queda abierto.
3. **El que puede matar el mecanismo entero (replay == organismo):** con `tabla_g` REALMENTE encendido durante el
   harvesting (`lab=True` + `tabla_g` activo a la vez, no por separado), `banco_g4.tabla_g_evalua` reprodujo
   `acc_lenta` del organismo en **9/9** corridas (3 mundos × 3 semillas), diferencia < 1e-9. Repetido también para
   la configuración ganadora de la búsqueda en xor01 (3/3). El mecanismo pasa este control con los datos que tengo.
4. **Rigging (¿la búsqueda mide lo que dice medir?):** NO lo corrí contra un objetivo cambiado (p.ej. buscar
   optimizando px0 en vez de xor01) por tiempo. Queda pendiente, y es un control real, no decorativo.
5. **Sesgo de selección WTA ("winner's curse"):** el ganador se elige por desempeño en los eventos vistos y se
   evalúa en el resto; con pocos eventos por celda de tabla (algunas combinaciones del grupo pueden no visitarse
   nunca en 200-350 mordidas pre-sonda) un grupo puede parecer bueno por azar. Es mi sospecha de por qué azar tiene
   ruido; no lo descarté con un control específico.

## Cláusula de refutación
Se refuta si, en la réplica confirmatoria del coordinador (Pool, 20 semillas VÍRGENES, p.ej. 121-140): la mediana
de acc_lenta en xor01 cae por debajo de 0.75, o azar sale sistemáticamente fuera de [0.35,0.65] en más de 1/20
semillas (regla EQUIPO #12), o el control de replay dejar de reproducir el organismo en cualquier semilla, o el
control de rigging (pendiente, #4 arriba) muestra que la búsqueda no distingue objetivos.

## Qué falta (honesto)
20 semillas nuevas in-organismo (yo solo hice 3, sin Pool, por regla del enjambre); g=3 y los otros dos
estimadores (tabla_binaria, MCR por celda) de la especificación completa; los dos estadísticos de competencia que
no implementé (cobertura, primer encuentro); el control de rigging (#4); una lectura de cuántos de los 20 patrones
XOR realmente se muerden antes de la sonda (posible sesgo de cobertura en la tabla). Nada de esto se corrió y no
se reporta como si se hubiera corrido.
