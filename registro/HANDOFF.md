# HANDOFF — Todo lo hecho, en orden, y por qué

Escrito el 16 sep 2026 para que cualquier persona o agente reconstruya el proyecto sin acceso a la conversación original.
Los números exactos están en `datos/` y en `REGISTRO_etapas_1_2.md`; aquí va la narrativa y la lógica.

## 0. Origen
Punto de partida: un documento de Christiam resumiendo 8 horas de simulación de neuronas artificiales (LIF estocástico,
engrama lento, Hebb → STDP, neuromodulador global, heterogeneidad E/I). Resultado: una red que distinguía dos ritmos
(+556% separación) y un organismo de 400 neuronas que NO encontraba comida (cableado aleatorio, sin topografía).
Pregunta de fondo: qué hace falta para que un sistema con reglas locales aprenda de su experiencia en un cuerpo.

## 1. Día 1 — exploración (carpeta `experimentos/dia1_exploracion/`)
Método: cada vez que algo fallaba, medir la causa antes de tocar parámetros.

| Archivo | Qué se probó | Qué se aprendió |
|---|---|---|
| sim.py (v0–v3) | Dos organismos simbióticos (A procesa, B digiere), neuromodulador ambiental, STDP | Red homogénea explota → inhibición + normalización por neurona. Bug: sensores desconectados (columna equivocada). Sensores simétricos no transmiten información → winner-take-all. Recompensa solo al comer → crédito ruidoso. La regla borraba la ruta en vez de construirla. |
| vida.py | Test mínimo 2×2 + interocepción (hambre), ruido y ganancia ∝ hambre, inhibición mutua de motores, error de predicción, costo metabólico, muerte | **Primer resultado limpio**: ruta sensor-motor emerge 6/6 en <1000 pasos. Sin hambre: 3/6 caen en el mínimo local "huir también sirve"; el hambre lo rompe. |
| retina*.py, calor.py | Retina 6px, dos patrones (comida/veneno), capa oculta | Come todo por igual. Capa oculta ciega (todas disparan) → k-WTA. Señal densa de "temperatura" no ayudó. |
| (política perfecta a mano) | ¿El mundo permite distinguir? | **NO**: la política perfecta comía 3 veces en 40k pasos (veneno bloquea el anillo). "Cómete todo" era óptimo. El mundo estaba mal, no el aprendiz. |
| morder*.py | Morder como decisión (tercer motor) | Test aislado retina→morder directo: 100%/3% perfecto. Con capa oculta: lotería. Con muerte: amnesia (borra 50%). Sin muerte: indefensión aprendida (nunca muerde, se deja morir). |
| organismo.py (v4) | Boca y patas separadas; curiosidad en patas, miedo solo en boca; miedo específico sin sesgo global; expansión Kenyon (30 celdas, 3 ganan) para decorrelacionar patrones; muerte sin olvido; **mundo con renovación** (objetos se pudren y nacen) | Discrimina 9/9. El bloqueo final era el mundo: se comió la última comida y quedó atrapado con solo veneno, negándose correctamente a comerlo. |
| poblacion*.py | 4 grupos de agentes, compartir pesos del mejor, selección | Sin individuo que aprenda, la población propaga ruido. Con v4: sobrevive 30% más pero oscila (renacer en blanco reinyecta ignorancia; el "mejor" por puntaje es un valiente descuidado). Los miedosos mueren de hambre; los valientes comen más. |

Ideas de Christiam que movieron algo: supervivencia como motor (rompe mínimos locales), sensación por paso, medir pendiente y no meta, tiempo del mundo (renovación).

## 2. Etapa 1 — baseline v4 (20 semillas)
19/20 aprenden; 1 se congela (miedo generalizado). Ratio comida/veneno mediana 32 vs 1.02 azar; muertes 148 vs 224.
El organismo come 6× menos que el azar: sobrevive por prudencia. Métrica correcta: muertes.

## 3. Etapa 2 — inversión del mundo (A↔B en t=50k), 12 semillas, un cambio por vez
- **2 (v4)**: 1/12 reaprende. Dos fallos: (a) hábitos confiados no reciben castigo, factor (mordió−pb)≈0; (b) miedo no se extingue sin exposición.
- **2A**: quitar factor de sorpresa → reversa de A 12/12 (~4.800 pasos). Extinción 0/12. Regla aprende más fuerte (W_A pre-inversión +6..+9).
- **2B**: hambre no lineal 2h+4h⁴ → más exposición (9/12 muerden B) pero triplica la deuda (W_B −8). 0/12.
- **2C**: aversión 3→1 → extinción incipiente en 2 semillas; reversa 2× más lenta. 0/12.
- **2D (=v5)**: Kenyon sin celdas compartidas A/B → elimina desplome de W_B en Q3 (castigo a A se filtraba). Correlación 7/7 vs 5/5. 0/12, pero tasa medida: 0.08/mordida, exposición solo al borde de la muerte.
- **2E**: 2D+hambre no lineal → hasta 25 mordidas de B, W_B sube 1.9; deuda inicial triplicada. 0/12.
- **2F**: canales apetitivo/aversivo separados (Wp, Wn ≥0, decisión = resta) → **primera extinción real** 2/12 (404 y 319 mordidas, aversivo intacto). Reversa de A rota: ambos canales saturan en 9 (sin freno al apetitivo).
- **2G**: error de predicción por estímulo, delta = R − (Wp−Wn)·kc (Rescorla-Wagner) → **extinción 12/12 en 600–2.200 pasos; W_A→−3.00, W_B→+1.00 exactos**. Muertes mínimas (145). Conducta: sigue mordiendo A 33–52/cuarto porque la política (+0.5, 2·h, T=.3) deja al hambre superar un valor de −3.
- **2H**: α=1.2 en la decisión, derivado de restricciones preregistradas (P≤5% a h=.9; P≥1% a h=1.0 → α∈[1.06,1.29]). Refutada por conteo (A veneno Q4 12–22, criterio ≤5) pero la tasa por visita coincide con la analítica (0.1%→4% según hambre). Error: α derivado en tasas, criterio en conteos, 4.000 visitas/cuarto. Decisión: criterio = tasa por visita condicionada al hambre; α=1.2 provisional.

Tres capas separadas empíricamente: representación / valor / política. En 2G el valor es exacto y la conducta no es óptima respecto a él.

## 4. Día 2 — bug, continuidad, interferencia
- **Bug de sincronía**: la boca decidía con el patrón del objeto más cercano ANTES de moverse. 25% de decisiones sobre comida usaban código de veneno. Descubierto porque la tasa observada (65%) ≠ predicha (99.7%). Corregido; 2H no cambió de conclusión.
- **2I** (C veneno nuevo en t=50k): aprende C sin degradar A/B, 12/12. Interferencia sistemática: ΔW_B −0.55 con C∩B>0 vs −0.02 sin. Misma valencia = deriva no corregida (B no se re-muestrea).
- **ANOM-01**: caída de W_A en "semilla 1" era aliasing de listas (era la semilla 12, con C∩A=1). Resuelta. No hay mecanismo no identificado.
- **2J** (D comida con D∩B=1): predicción +0.5 refutada (+0.05). Mecanismo: canales inflados (D 2.22/1.22, B 0.74/3.67) para valores netos correctos. Valencia opuesta → re-muestreo → RW corrige. Costo: miedo transitorio a comida.
- **2K** (D∩B=2, corrido fuera de orden): valores aguantan con degradación graduada (W_B −2.78, W_D 0.95); canales 5.1/4.1 y 3.4/6.2; techo real = 9 por canal, no 3 (error aritmético mío). **2K-bis abierta**: capacidad (3 celdas / clip).
- **v6**: consolidación en un archivo con escenarios como parámetros; batería de regresión (E1, E2, 2I, 2J, 2K) toda PASA; baseline 20/20.

## 5. Mecanismos del organismo v6 y por qué cada uno existe
| Mecanismo | Falla que lo pidió |
|---|---|
| Inhibición + normalización homeostática | avalancha de red homogénea |
| Sensores winner-take-all | actividad pareja no transmite información |
| Traza de elegibilidad + error de predicción | crédito ruidoso con recompensa tardía |
| Hambre → ruido y ganancia; inhibición mutua de motores | mínimo local "huir también sirve"; motores simultáneos = quieto |
| Boca separada de patas | morder competía con moverse |
| Curiosidad en patas, castigo solo en boca | castigo en piernas → deja de caminar |
| Miedo específico al patrón, sin sesgo global | "morder es malo" → indefensión aprendida |
| Expansión Kenyon dispersa | miedo a B contaminaba A por un píxel compartido |
| Muerte sin olvido | amnesia por muertes frecuentes |
| Mundo con renovación | atrapado en mundo de solo veneno |
| Regla sin factor de sorpresa | hábitos confiados no reciben castigo |
| Canales apetitivo/aversivo | extinguir = borrar, demasiado lento |
| Error de predicción por estímulo (RW) | apetitivo crecía sin freno hasta saturar |
| α=1.2 en la decisión | valor −3 no dominaba al hambre |
| Percepción sincronizada | boca decidía con la imagen previa |

## 6. Errores del proceso (para que no se repitan)
Unidades (2H), disponibilidad (2I), aliasing (ANOM-01), orden de ejecución (2K), aritmética del techo (2K), columna de sensores (día 1). Patrón: cuando algo se ve raro, primero el instrumento.

## 7. Limitación metodológica
Las soluciones fueron elegidas conociendo la literatura (Hebb, STDP, Schultz, Rescorla-Wagner, cuerpo fungiforme).
Lo que el organismo dictó fue la NECESIDAD de cada mecanismo (quitarlo rompe algo medible). Defendible: necesidad; no: descubrimiento a ciegas.

## 8. Qué NO hemos demostrado
Generalización a patrones no vistos, transferencia, planificación, memoria más allá de una vida, acumulación poblacional, comunicación. Nada de esto se afirma.
