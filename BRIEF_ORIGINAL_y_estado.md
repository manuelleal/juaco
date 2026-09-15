# BRIEF ORIGINAL (plan de pruebas) — y estado de cada punto al 16 sep 2026

Documento de dirección redactado por Christiam (con apoyo de otro asistente) el 15 sep 2026. Es el marco de referencia
del proyecto; PLAN.md y PLAN_HORIZONTES.md lo desarrollan. Aquí, el contenido esencial de cada punto y su estado.

## Principio rector (punto 20)
"Primero demostrar que aprende. Después que recuerda. Después que generaliza. Después que transmite.
Después que la población acumula. Después preguntar qué puede emerger." — Se cumple en ese orden. Estamos en el tercero.

## Punto 6 — Regla fundamental
Nunca declarar AGI por aprender A/B, sobrevivir, evitar veneno, mejorar puntaje, memorizar o mostrar conducta compleja.
Distinguir: 1 conducta adaptativa · 2 aprendizaje · 3 memoria · 4 generalización · 5 transferencia · 6 planificación ·
7 composición · 8 aprendizaje abierto · 9 autonomía · 10 inteligencia general.
**Estado**: demostrados con criterio preregistrado: 1, 2, 3 (dentro de una vida; entre vidas pendiente). Indicios de 4
(2I/2J: transferencia por solapamiento, controlada). 5–10: nada.

## Punto 7 — Primera tarea: reconstruir, reproducir, buscar bugs y sesgos, baseline congelado
**Hecho**: v4 → v5 → v6 congelados con hash; baseline 20 semillas (v6: 20/20). Bugs encontrados: columna de sensores (día 1),
sincronía sensor-acción (v4–2I). Sesgos: parámetros a mano listados en el registro; tres errores de instrumento documentados.

## Punto 8 — Matriz experimental
A organismo sin aprendizaje — **hecho** (control en todos los baselines).
B con aprendizaje individual — **hecho** (baseline v6).
C población con aprendizaje sin transmisión — **hecho parcial** (control de poblacion2, día 1; rehacer con v6).
D población con transmisión de memoria — **hecho parcial** (compartir pesos, día 1; rehacer con v6).
E transmisión + selección — **hecho parcial** (oscila; renacer en blanco reinyecta ignorancia).
F transmisión + selección + memoria heredada — **pendiente** (primer experimento de Fase 2 en el repo).
Semillas: 12–20 hasta ahora; 100 pendiente (infraestructura paralela, Fase 1).
Métricas pedidas: supervivencia, vida, comida, veneno, energía, tasa/velocidad de aprendizaje, recuperación, memoria,
generalización, variabilidad, diversidad. **Cubiertas**: las 8 primeras. Variabilidad/diversidad entre organismos: pendiente.

## Punto 9 — Inversión del mundo y estímulo C
**Hecho y cerrado en valor**: 2A–2H (inversión: 12/12 en valor y extinción con 2G). 2I (C nuevo sin destruir A/B): 12/12.
Abierto: política bajo hambre (conducta ≠ valor).

## Punto 10 — Generalización (no memorizar píxeles)
**Pendiente** (Fase 3 del PLAN). Predicción distintiva ya formulada: con Kenyon, la generalización será proporcional al
solapamiento de códigos, no a la similitud visual. Falsable.

## Punto 11 — Memoria (borrar mundo, matar cuerpo, reproducir, cambiar entorno)
**Parcial**: memoria intacta tras muerte del cuerpo (v4+). Comparación cero/parcial/heredada: pendiente (Fase 4).

## Punto 12 — Transmisión cultural artificial
**Pendiente**. Diseño mínimo escrito (juego de señalización, PLAN_HORIZONTES H3).

## Punto 13 — Organismos como nodos
**Pendiente**. Rama 2M (pulpo) exploró distribución interna: refutada a 6 estímulos.

## Punto 14 — Criterio de emergencia
Propiedad: ausente en individuo, presente al conectar, no programada, reproducible, desaparece al romper la estructura.
**Estado**: 2L (plasticidad) cumple 3 de 5 a escala de organismo (no programada dónde/cuándo, reproducible, desaparece sin la
regla) — pero es intra-individuo, no colectiva. Ningún resultado colectivo aún.

## Punto 15 — Trampas a vigilar
Reward hacking, sesgo de selección, información filtrada, variables con la respuesta, memoria escondida, recompensas mal
diseñadas, correlaciones accidentales, overfitting, selección de conductas absurdas, explotar bugs del entorno, métricas falsas.
**Casos reales encontrados**: "cómete todo" era óptimo por diseño del mundo (recompensa mal diseñada); huir también servía en
el anillo (explotar geometría); mundo sin renovación (bug del entorno); bug de sincronía (información equivocada);
criterio por conteo vs tasa (métrica engañosa). Todos documentados.

## Punto 16 — Etapas
1 A/B reproducible — **CERRADA** (v6 20/20).
2 Inversión — **CERRADA en valor** (2G), abierta en política.
3 Generalización — pendiente.  4 Memoria persistente — parcial.  5 Transmisión — pendiente.
6 Acumulación cultural — pendiente.  7 Comunicación — pendiente.  8 Planificación — pendiente (H2).
9 Problemas nuevos — pendiente.  10 Múltiples dominios — pendiente.

## Punto 17 — Restricción computacional
**Cumplida**: todo en CPU, NumPy, portátil. 100k pasos ≈ segundos por semilla.

## Punto 18 — Objetivo profesional
Repo reproducible: **hecho**. Artículo: material listo para ~3 páginas (cadena 2A→2G + convergencia). IP: nada defendible
(todo con autor y fecha). Producto: nada aún. Oportunidad: credibilidad primero.

## Punto 19 — Papel de Claude y formato de propuestas
Hipótesis → experimento → código → resultados → interpretación. Cada modificación con: qué prueba, qué cambia, qué esperamos,
qué la refuta, qué métricas, qué controles. **Se ha seguido desde 2A**; los desvíos (2K fuera de orden) están registrados.
