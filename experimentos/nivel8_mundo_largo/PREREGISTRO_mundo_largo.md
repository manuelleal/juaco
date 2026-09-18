# Niveles 8 + 9, experimento 4 del plan: mundo largo con novedad y con cambio de regla (v13 contra v13 + mapa)

**Escrito ANTES de construir el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Cuarto experimento del
plan del debate (`DEBATE_y_plan_5a10.md` §3, punto 4), condicionado a que el mapa sobreviviera: sobrevivió y se replicó
(`mapa_s1-20_20260917_192813`, `mapa_s21-40_20260917_193133`). Regla 12.

## 0. Qué se recorta de la propuesta del debate, y por qué (escrito antes de correr)

- **Cuatro brazos → dos** (v13 puro y v13 + `M`). Se dejan fuera "+`M`+energía" (nivel 9: una tabla de energía por
  posición añade poco sobre `M`, que ya lee el valor vivo; con la regla invertida las dos necesitan morder para
  actualizarse) y "+fusión" (nivel 8: el propio debate señaló que ignora la puerta, que es el cuello real de capacidad
  —35/60 con puerta, 50/60 sin ella—; fusionar celdas no toca la puerta). Si este experimento muestra que la caída es
  por celdas y no por puerta, se preregistra la fusión después.
- **"Cientos de estímulos nuevos" es imposible con esta retina:** 6 píxeles dan 63 patrones no nulos. Se usan **50**
  (los 20 de peso 3, 15 de peso 2 y 15 de peso 4), con valencias al azar por semilla (25/25). El límite de novedad es
  del cuerpo, no del organismo; queda registrado como cota del nivel 8 en este mundo.
- El mundo es el del mapa (`r_vis = 3`, sitios fijos que reaparecen a los 50 pasos), porque es donde `M` tiene sentido
  (con reaparición en posiciones al azar, un mapa posición→patrón no puede servir).

## 1. Mundo `mundo_largo.py` (desde `mundo_mapa.py` `207d6a1954336b18`, por anclas; perillas apagadas ≡ mapa ≡ v13)

- **8 sitios fijos**; al inicio 4 patrones (2 comida, 2 veneno), cada uno en dos sitios. Cada `T_nuevo = 4000` pasos
  entra un patrón **nuevo** (orden al azar por semilla) y reemplaza el tipo del sitio cuyo tipo lleva más tiempo sin
  renovarse. T = 200 000 → 46 inyecciones: los 50 patrones pasan por el mundo. **Novedad real**, no reciclaje.
- **Cambio de regla** (nivel 9): en t = 100 000, sin aviso, se **invierte la valencia de los 4 patrones iniciales** (los
  que más se han mordido) y de los presentes en ese momento.
- Medidas (todas por readout de `valor()`, sin tocar el organismo, más conducta): **adquisición** = fracción de los
  últimos 10 patrones inyectados con signo de valor correcto, medida en cada inyección (curva contra número de
  patrones vistos); **retención** = signo correcto de los 10 primeros al final; **recuperación** = pasos desde
  t = 100 000 hasta que la tasa de comida mordida por 1000 pasos vuelve a ≥ 80 % de la media de los 20 000 pasos
  previos; muertes en los 20 000 pasos posteriores al cambio; celdas activas.
- Brazos: **V13** (`usa_M = False`), **MAPA** (`usa_M = True`, `gamma_M = 0.6`); control de novedad **RECICLADO** (en
  cada inyección entra un patrón ya visto en vez de uno nuevo) para ambos. Identidad: `mundo_largo(T_nuevo = None,
  invertir_en = None)` ≡ `mundo_mapa` con las mismas perillas, todas las claves, semillas 1–3.

## 2. Predicciones y criterios (medianas, 20 semillas)

- **A1 (adquisición sostenida):** en ambos brazos, acierto en los últimos 10 inyectados ≥ **0.75** mientras los
  patrones vistos ≤ 30; **A2:** con 50 vistos cae a **0.55–0.70** (la capacidad conocida: 35/60). **A3:** RECICLADO
  ≥ 0.85 siempre (lo viejo se sabe). **R1 (retención):** los 10 primeros con signo correcto ≥ 0.70 al final en ambos.
- **C1 (recuperación):** V13 recupera el 80 % de la tasa de comida en ≤ 10 000 pasos en ≥ 15/20. **C2 (la pregunta de
  nivel 9 con mapa):** MAPA recupera en **menos** pasos que V13, pareado ≥ 15/20 (vuelve a los sitios recordados,
  muerde, relearn más rápido) **pero muere más** en la ventana (≥ 15/20 pareado): el mapa acelera la corrección a
  costa de comer lo que antes era comida. Si MAPA recupera más lento, la predicción se refuta tal cual.
- **Vocabulario si pasa:** "*sigue aprendiendo hasta el techo de capacidad de la retina y se recupera de un cambio de
  regla; el mapa acelera la recuperación y la cobra en muertes*". No "abierto", no "autónomo". Refutación: A1 o C1
  fallan (no sigue aprendiendo, o no se recupera). Nada se recalibra después.
- Coste: 3 brazos (V13, MAPA, RECICLADO-MAPA) × 20 semillas × 200 000 ≈ 4 min.


## Enmienda 1 (18 sep 2026, escrita ANTES de correr; semillas NUEVAS 21–40): separar olvido de inversión (R1)

R1 mezclaba dos cosas: los 4 patrones iniciales se **invierten en ausencia** (t = 100 000, ya desplazados; no pueden
enterarse) y los 6 siguientes de los 10 primeros **nunca se invierten**. Se guarda `W` por patrón y se miden por separado:
**R1a** = fracción con signo correcto, al final, de los patrones 5–10 vistos (nunca invertidos, ausentes desde hace
≥ 150 000 pasos): predicción ≥ **0.70** en V13 y MAPA (retención real). **R1b** = la misma fracción para los 4 iniciales
(invertidos en ausencia): predicción ≤ **0.25** (por construcción: conservan el signo viejo). Todo lo demás igual
(A1–A3, C1–C2 se reportan como réplica en 21–40; A2 se deja como estaba escrita: predije 0.55–0.70 y salió 0.80).
