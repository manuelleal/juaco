# Nivel 7 — Composición

*17 sep 2026. Investigación exploratoria (no preregistro). Nivel 7 de la escalera del punto 6 del brief.
Fuentes: `CLAUDE.md` (Estado día 5, reglas 1–11), `BRIEF_ORIGINAL_y_estado.md` (puntos 6, 14, 15, 16),
`registro/HORIZONTE_frontera.md`, `registro/REFLEXION_agi.md`. Sin ejecutar código ni tocar el repo.*

**Estado medido.** Composición = rasgos (XOR/conjunciones) + secuencias de más de un paso + composición social.
Rasgos: NO (XOR 0.44; vía lenta lineal por diseño, vía rápida Kenyon separa pero no compone). Secuencias: 1 paso
SÍ (3T, `sep` 3.96), 2–3 pasos sin probar. Social: diseño N3 pendiente, sin correr. Nivel tocado, no cerrado.

## (1) Qué existe

- **Codificación dispersa/expansión aleatoria:** Litwin-Kumar, Harris, Axel, Sompolinsky y Abbott (2017),
  *Optimal Degrees of Synaptic Connectivity* (Neuron) — el grado de conectividad que maximiza la dimensión de la
  representación en células de Kenyon de *Drosophila* coincide con lo anatómico: es el circuito que v13 imita.
- **XOR/conjunciones, umbral:** Minsky y Papert (1969), *Perceptrons* — un umbral lineal no computa XOR; hace
  falta no linealidad oculta. Clásico.
- **XOR/conjunciones, dendritas:** Poirazi, Brannon y Mel (2003, Neuron, *Pyramidal Neuron as Two-Layer Neural
  Network*): dendritas activas = subunidades no lineales independientes, equivalen a dos capas. Gidon et al.
  (2020, *Science*): un potencial dendrítico de calcio dispara con la entrada X sola o Y sola, no con ambas —
  XOR medido en una sola dendrita.
- **Secuencias, trazas/reservorios:** trazas de elegibilidad/TD(λ) (Sutton y Barto) asignan crédito temporal con
  regla local. Jaeger (2001, *echo state networks*) y Maass, Natschläger y Markram (2002, *liquid state
  machines*): reservorio fijo y aleatorio + lectura entrenada — sólo la lectura aprende, estructuralmente lo que
  v13 ya hace (Kenyon fijo + valor entrenado).
- **Generalización sistemática:** Lake y Baroni (2018, SCAN, ICML) — seq2seq falla en composición sistemática sin
  ayuda. Lake y Baroni (2023, *Nature*) — con meta-aprendizaje explícito (MLC) sobre miles de episodios sí
  generalizan como humanos. **Límite que importa:** depende de gradiente global iterado, lo que la regla 1 excluye.
- **Composición en colectivos:** Deneubourg y colegas (1989–90 [verificar cita exacta]), puente doble — la
  colonia elige el camino más corto por refuerzo local de feromona, sin que ningún individuo compare longitudes.
  Coincide en forma con el criterio de emergencia del punto 14.

## (2) Qué falta para reglas locales sin gradiente global

- No linealidad de segundo orden **entrenable localmente**: Kenyon es expansión fija, el valor es lectura por
  celda sin término cruzado.
- Crédito temporal más allá de 1 paso con regla local: 3T llega a 1; sin traza de profundidad *k* probada.
- Canal social que **funda** dos observaciones simultáneas en una decisión: N1 es secuencial (cuerpo a cuerpo);
  N3 no tiene mecanismo de fusión, sólo diseño.
- Aplicar el criterio de emergencia del punto 14 a un resultado colectivo: **ninguno lo ha usado todavía**
  (textual del brief).
- Control de capacidad emparejado: todo candidato agrega parámetros o celdas; sin control no se distingue
  "compone" de "memoriza con más recursos".
- Ningún candidato corrido aún contra `bateria_v13.py` / `bateria_generaliza.py`: los cánjes cerrados (memoria
  20/20, capacidad, generalización lineal 0.80–0.90) no están verificados para XOR ni secuencias largas.

## (3) Mecanismo mínimo compatible con v13

Kenyon de segundo orden es plausible (Litwin-Kumar) pero agrega capa y celdas — caro, difícil de aislar de un
cambio de capacidad. División-que-cruza-rasgos toca el órgano evolucionado v11, con riesgo de reabrir el canje
memoria/capacidad recién cerrado. Social (N3) es válido en paralelo pero depende de un canal de fusión inexistente
(ver (2)). **Elegido — término cuadrático local en la vía lenta**, cambio más chico y más aislable (regla 2):

```
1.  Un solo cambio (regla 2): sólo vía lenta; Kenyon, división y memoria de trabajo intactos.
2.  Wq ∈ R^15 (pares i<j de los 6 píxeles), inicializado en 0.
3.  valor_lento = Wps·x − Wns·x + Σ_{i<j} Wq_ij·x_i·x_j
4.  δ = R − valor_lento   (Rescorla-Wagner, igual que hoy)
5.  Wq_ij += eta_q·δ·x_i·x_j   (local: pre×post×error, misma forma que Wps/Wns)
6.  eta_q = eta_s = 0.015 salvo que el piloto muestre inestabilidad.
7.  Puerta de familiaridad sin cambio (3 celdas Kenyon, |Wp−Wn|>0.2).
8.  Álgebra, no hipótesis (si x∈{0,1}; verificar en la retina real): XOR(x_i,x_j)=x_i+x_j−2x_i x_j exacto.
9.  Control (a): Wq congelado en 0 (= v13 actual).
10. Control (b): Wq al azar y congelado (¿alcanza con más parámetros sin aprender?).
11. Predicción: acierto en XOR nunca visto sube de 0.44 a ≥0.70 con (5) activo.
12. Refutación: si (5) no supera a (9) en ≥15/20 semillas, o no se distingue de (10).
13. Si se refuta: escalar a Kenyon de segundo orden, mismo criterio.
14. Si también: social (N3) queda como única vía abierta para XOR.
15. Regresión obligatoria antes de congelar: bateria_v13.py 6 + bateria_generaliza.py.
```

## (4) Cómo acortar la línea

- **Con 7:** el experimento único más informativo no es XOR — es **repetir 3T con k=2 (y k=3)**, reusando
  `experimentos/3T_confirmatorio/`. Barato, aísla una sola variable (profundidad), y si sobrevive entrega la
  traza de *k* pasos que pide (2).
- **Con 6 (planificación):** nunca se probó planificación propiamente (elegir con un modelo de "qué pasaría si");
  lo más cercano es la memoria de trabajo de rechazo (v9, reactiva) y 3T (compone historia, no decide con ella).
  El mismo experimento de k≥2, leído por la política de hambre en vez de por el examen, sirve para 6 y 7 a la vez.
- **Con 5 — cuidado con el nombre:** el punto 16 llama "Etapa 5" a la *transmisión* entre cuerpos (N1/N2/N3); la
  escalera del punto 6 llama "nivel 5" a *transferencia* (reusar valor sobre un dominio nuevo relacionado). No es
  lo mismo pese al número compartido. Lo más cercano a transferencia-nivel-5 hoy: 4c (herencia de valor por
  identidad de código) y, en sentido amplio, N1. El mecanismo de (3), si funciona, es evidencia de transferencia
  además de composición: reutiliza Wps/Wns del régimen lineal sobre una combinación nunca vista.

## (5) Romper la frontera

**Idea sin probar:** la expansión de Kenyon (30→90, top-3) ya vuelve XOR linealmente separable en el espacio
expandido; el 0.44 sería un límite de **lectura**, no de representación. Fundamento: Cover (1965), *Geometrical
and Statistical Properties of Systems of Linear Inequalities*: una proyección no lineal aleatoria a dimensión
suficiente separa linealmente casi cualquier partición del espacio de entrada — base teórica de reservorios y
máquinas de aprendizaje extremo.

**Refutación barata:** congelar la misma expansión/códigos de Kenyon de v13 (cero cambio de arquitectura) y
cambiar sólo la lectura (top-k en vez de top-3, o la lectura cuadrática de (3) sobre el código Kenyon). Si el
acierto sube sin tocar la expansión, el cuello de botella era la lectura. Si no sube, es la expansión/dispersión
misma: (3) queda descartado como única vía y hay que ir a Kenyon de segundo orden o a lo social.

## (6) Trampas

- Mundo XOR con los 4 píxeles "irrelevantes" correlacionados por construcción → acierto por atajo, no por
  composición (regla 5: primero el instrumento).
- Wq o Kenyon de segundo orden memorizan en vez de componer → por eso los controles (a)/(b) de (3) no son
  opcionales (patrón K4, día 4: "memoria escondida").
- Selección por criterio de parada, no por dirección (hallazgo histórico de 3T, día 3): verificar que la mejora
  no sea un artefacto de cuándo deja de actualizarse Wq.
- Señal social que regala la respuesta: toda prueba de N3 exige el control ya construido en N1 (señal barajada).
- Etapa cerrada sin batería (ERR-20): nada se congela sin `bateria_v13.py` y `bateria_generaliza.py` — ganar XOR
  y perder retención o generalización lineal es el mismo canje con otro nombre.
- Aprender ≠ representar mejor (rama 3K, día 3): medir Wq contra el control (b) (azar, congelado), no contra
  "aprendió vs. no aprendió".

## (7) Propuesta en formato del proyecto

- **Hipótesis:** un término cuadrático local en la vía lenta (Wq sobre pares de píxeles, regla tipo
  Rescorla-Wagner) basta para generalizar sobre combinaciones XOR nunca vistas, sin tocar Kenyon ni división.
- **Mundo:** el mismo mundo XOR usado para medir 0.44 (localizar el script antes de correr); si no es
  reutilizable, construir uno con 2 de los 6 píxeles bajo regla XOR y 4 de ruido i.i.d., preregistrado antes de
  correr (regla 2).
- **Medidas:** acierto en XOR nunca visto (mediana y rango por semilla, regla 6); retención (`bateria_v13.py`);
  generalización lineal (`bateria_generaliza.py`).
- **Predicción numérica:** con Wq activo y plástico, acierto ≥0.70 en nunca vistos (frente a 0.44 medido);
  controles (a) y (b) en 0.44–0.50.
- **Refutación:** si Wq activo no supera al control (a) en ≥15/20 semillas, o no se distingue del control (b).
- **Controles:** (a) Wq congelado en 0; (b) Wq al azar y congelado; (c) regresión completa (memoria +
  generalización lineal) para descartar canje oculto.
- **Coste en corridas:** piloto 20 + réplica 20 + controles 20×2 ≈ 80 corridas de T=100000; a razón de segundos
  por semilla (punto 17 del brief), del orden de minutos en CPU — mismo orden que `bateria_generaliza.py 20`.
