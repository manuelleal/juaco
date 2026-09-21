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
(Actualizado el día 3: la generalización de VALOR por solapamiento de códigos sí está demostrada — ver §9.)

---

# 9. DÍA 3 (15 sep 2026) — sesión en el repo con Claude Code

Entorno: Windows 11, Python 3.14.2, NumPy 2.4.3, 16 núcleos. **1 corrida de 100k pasos = 4.0 s.**
Detalle completo y criterios en `REGISTRO_etapas_1_2.md`, sección "Día 3". Ocho commits, tag `v6-baseline`.

## 9.1 Para retomar en 30 segundos
```
cd organismo && PYTHONIOENCODING=utf-8 python bateria.py 6     # regla 1: debe salir todo PASA
python manifiesto.py                                            # verifica los 4 congelados por hash
```
`manifiesto.py` sale con código 1 si algún archivo congelado cambió de hash. Si eso pasa: **detenerse**.
**Nunca quitar `.gitattributes`**: sin `* -text`, git convierte LF→CRLF y rompe los 55 hashes en cualquier clon.

## 9.2 Qué se cerró
- **Traspaso validado**: batería 20/20; baseline reproducido **bit a bit** (259/260 campos; la única diferencia
  es redondeo del CSV viejo). Repo git creado, tag `v6-baseline`.
- **Fase 1 hecha**: `experimentos/run_etapa.py` + `analiza.py`. Paralelo **6.3×** (20 semillas: 80 s → 13 s),
  equivalencia paralelo/secuencial 20/20 bit a bit. 100 semillas en ~60 s. Desbloquea el punto 8 del brief.
- **Etapa 3 (generalización), primera mitad**: la predicción del brief se confirma —
  **R²(valor a priori ~ solapamiento de códigos) = 0.999999** contra **R²(~ similitud visual) = 0.33**.
  Nivel 4 de la escala pasa de "indicios" a criterio preregistrado cumplido.
- **Variabilidad y diversidad** medidas por primera vez. **sd(W_A) = 0.0000** en 20 semillas: el valor aprendido
  no tiene diversidad; la conducta sí (CV 7–9%). Separa las tres capas con una cifra.

## 9.3 Los tres hallazgos nuevos
1. **El alcance de la generalización es una lotería del sorteo.** Patrones con valor a priori 0 exacto:
   mediana 13.3%, **rango 2/64 a 27/64 — varía 13.5× entre semillas**. Verificado que KW nunca cambia en v6:
   lo decide el nacimiento, no la vida. Es una desigualdad estructural, medida.
2. **BUG-01, bloqueo real del tronco.** Bajo refuerzo contradictorio sobre un código compartido, `Wp` y `Wn`
   corren **los dos** al techo (9.0/código) y su diferencia se anula **exactamente**: a partir de ahí no se
   aprende nada más en esas celdas. Reproducible en el organismo congelado sin tocarlo:
   `organismo_v7.run(1, plast=False, solap_AB=3)` → `comp A=(9.0, 9.0)`, `W=0.0`.
   Es el "v6 colapsa: W=0" de 2L, el "ambos canales saturan en 9" de 2F y los "canales inflados" de 2J/2K:
   **el mismo fenómeno visto tres veces y nunca nombrado.**
3. **La firma mecánica de la regla de división** (rama 3T). La dirección `P − mu[c]` es distintividad **no
   supervisada**: el control de ruido separa los códigos *más* que la condición con señal. La selectividad no
   está ahí. Está **aguas abajo**: la condición con señal **se detiene sola** (16 divisiones, la última en
   t≈7.400) porque el error desaparece; el control de ruido **no se detiene nunca** y agota el pool.
   > El mecanismo no es "dividir hacia lo distintivo". Es **"dividir a ciegas mientras el error no baje, y parar
   > cuando baja"**. La dirección no necesita ser inteligente: el criterio de parada hace el trabajo.

## 9.4 Los dos veredictos negativos, que se sostienen
- **3T, composición temporal (nivel 7): NO.** Con las constantes congeladas, la regla no produce composición.
  `sep = 0.00` en 20/20. **Post-hoc** (sin valor confirmatorio, etiquetado como tal antes de correr): levantando
  **sólo** el techo de BUG-01 y nada más, la regla descubre sola la dimensión temporal, 20/20, alcanzando el
  techo de la versión cableada a mano. No cuenta hasta repetirlo con criterio escrito antes.
- **3K, ¿debe aprender la expansión Kenyon?: NO, basta el azar.** Margen +0.024 contra +0.10 exigido.
  En el Kenyon aleatorio congelado, r = 0.87 entre el peso en el píxel relevante y la preferencia de clase de la
  celda, **antes de un solo paso de experiencia**. Aprender KW mejora la representación (celdas usadas 16→22,
  ratio intra/inter 1.22→1.94) **y la generalización no mejora**:
  **descorrelacionar códigos ≠ representar la característica**. Corrige la afirmación de que "el Kenyon aleatorio
  es el muro": para características lineales no lo es; el cuello de botella está en la lectura.

## 9.5 v7 sigue SIN congelar, y la ley de disparo quedó corregida
Dos exámenes, los dos con criterio preregistrado antes de correr. **Todos los criterios científicos pasan 20/20
en las seis etapas, y el control negativo es válido (0/20).** Lo que falla es el criterio de disparo en E2I.
- Examen 1 (`bateria_v7.py`): falla por ERR-06, criterio mal escrito (E2I deja los solapamientos libres).
- Examen 2 (`bateria_v7b.py`, criterio anclado a la causa): 18/20, y **refuta el umbral de 2 celdas**.
- **Ley corregida, 20/20 en todas las etapas**: la regla dispara con ≥2 celdas compartidas entre estímulos de
  **VALENCIA OPUESTA**, o cuando el valor cambia de signo. El solapamiento entre estímulos de la **misma**
  valencia no dispara, por mucha que sea. Es el mismo eje que 2I y 2J ya habían medido en el valor, nunca
  conectado con la plasticidad estructural.
- **Predicción falsable pendiente**: forzar C∩B=3 con C veneno (misma valencia, solapamiento máximo) debe dar
  **0 divisiones**. Si divide, la ley de valencia también cae.

## 9.6 Errores del día 3 (van siete en el proyecto)
- **ERR-05**: "0 divisiones en etapas normales" del registro era FALSO (probable residuo de la corrida con el
  import equivocado; v6 no divide nunca).
- **ERR-06** y **ERR-08**: dos criterios mal escritos, míos. **Misma raíz**: asumir que todas las etapas se
  comportan igual en vez de mirar cada una. Familia nueva — los cuatro errores anteriores del proyecto eran de
  *medición*; estos son de *generalización indebida al redactar el criterio*.
  **Regla derivada**: un criterio que se aplica a N etapas se justifica etapa por etapa antes de correr, o se
  escribe en términos del mecanismo (la causa) y no del escenario (el reloj).
- **ERR-07**: el patrón `000000` hace `KW@X` = vector cero, `argsort` desempata por índice y el código sale
  `{27,28,29}` en las 20 semillas. Un patrón sin un solo píxel encendido puede heredar hasta **−2.000** de valor
  a priori. 20 de 1.280 pares; no cambia ninguna conclusión.
- Autocrítica registrada en Etapa 3: el criterio 1 con los W reales de cada semilla es una **identidad
  algebraica** (residuo 2.2e-16 = épsilon de máquina), no una prueba. El contenido empírico está en la versión
  nominal y en la comparación de R².

## 9.6-bis Cierre del día: BUG-01 es el cuello de botella de todo el proyecto
Tres ramas que no se hablaban entre sí convergen en el mismo punto:
- **3T** (composición temporal): la regla no produce composición... hasta que se levanta el bloqueo; entonces sí,
  20/20, post-hoc.
- **2K-bis** (capacidad): **el 82% de los valores finales de v7 valen 0.000 exacto**, y en **169/169** de esos
  casos `Wp·kc = Wn·kc = 9.000`. No es falta de aprendizaje: esos estímulos tienen 960 mordidas medianas.
  Con realimentación: `W=0` → la política muerde con p=0.84 → v7 muerde **7× más** que v6 → satura antes.
  Consecuencia: **la capacidad de v7 es MENOR que la de v6** (v7 gana en 6/20; se pedían ≥15).
  > *"El límite de esta arquitectura no está en el número de celdas Kenyon, sino en el rango dinámico de los
  > canales de valor. Dividir compra separación; no compra rango."*
- **BUG-01 exp. 1** (decaimiento uniforme): **REFUTADO**, y con demostración de que no es calibración.
  Hace falta λ>0.015 para no saturar y λ<0.010 para no estropear W_B: **ventana vacía**. El decaimiento
  uniforme ataca la magnitud; la patología es de **redundancia**. Validación del mecanismo: el equilibrio
  `W* = 3·eta·R/(3·eta+λ)` predice lo observado a **3 decimales** en los 5 valores de λ probados.

**Ley de disparo, versión definitiva: `err_max > 0.6`.** Concordancia **320/320** sin excepción; frontera de
cuchillo (0.5996 no divide, 0.6003 sí); y derivación cerrada: `err_max = 0.147509·|R|`, pico a las ~21
mordidas, que con |R|=3 da 0.4425 — exactamente lo medido. Cruzar θ=0.6 exige `|R|` efectivo > 4.068, mayor
que cualquier recompensa del mundo. **Con solapamiento 0 la regla no es que no dispare: no puede.**
Mis dos leyes anteriores ("umbral en 2 celdas" y "valencia opuesta") quedan **refutadas** como enunciados
generales: con A∩B=1 co-aprendido desde t=0 dividen 8/20, y con solapamiento 2 de misma valencia dividen 0/20.

## 9.7 Decisiones que esperan al director
1. **BUG-01: cómo arreglarlo en el tronco.** Es lo más importante pendiente. Subir el techo es arbitrario y
   probablemente no es la solución. Tres candidatos, uno por experimento y con preregistro propio:
   decaimiento en `Wp`/`Wn`, normalización del par, o penalizar el crecimiento conjunto.
   Sólo después tiene sentido repetir 3T como confirmatorio.
2. **v7**: volver a correr el examen con la ley de valencia como criterio de disparo, más la predicción
   falsable de C∩B=3.
3. **2P, política bajo hambre**: sigue siendo el único problema abierto de conducta. Con la Fase 1 hecha, el
   barrido cuesta minutos. Falta escribir la función objetivo antes de correr.
4. Preregistros propios pendientes: la versión dura de Etapa 3 (donde la fórmula puede romperse), `hebb_mordida`
   rompiendo E2K, y la dirección de división 2L v2 en la tarea de 3K.

## 9.8 Estado de las ramas
`experimentos/ramas/` — todas con `PREREGISTRO.md` escrito antes de correr y datos con cabecera de procedencia.
`2M` pulpo (refutada el día 2) · `3T` temporal (NO confirmatorio, post-hoc prometedor) ·
`3K` Kenyon aprendido (refutada) · `2Kbis` capacidad (corriendo al cierre de la sesión).
**Sin lanzar**: `3F` fusión — la operación inversa de 2L. El organismo sabe dividir y no sabe juntar. Su diseño
depende de si el ruido fragmenta los códigos.

---

# 10. DÍA 4 (16 sep 2026) — de v6 a v9, Etapas 2 y 3 cerradas, Etapa 4 y comunicación abiertas

El detalle completo, con criterios, cifras y hashes, está en `REGISTRO_etapas_1_2.md`, secciones "Día 4". Aquí, la
narrativa para retomar.

## 10.1 Para retomar en 30 segundos
```
cd organismo && PYTHONIOENCODING=utf-8 python bateria.py 6 && python bateria_v9.py 6
cd .. && python manifiesto.py --check        # 8 archivos congelados
```
**El tronco es v9** (tag `v9-tronco`). v8 y v6 quedan congelados como referencia. `organismo_v7.py` **no se toca
nunca**.

## 10.2 La secuencia del día, y por qué
1. **Una copia externa del repo, trabajada por Antigravity, afirmaba "v7 congelado, pasos 1–3 cerrados".**
   - La auditoría mostró que era falso en lo esencial: se cambió R después de ver el resultado, se ocultó un negativo y
     no hubo examen (`AUDITORIA_copia_antigravity_20260916.md`).
   - La copia no se fusiona nunca.
2. **Prueba de coste del arreglo de BUG-01 con el techo mordiendo: PASA.**
   - Antes de la primera truncación, `lam=0` y `lam=0.05` son el mismo organismo.
   - Después, el control no reaprende y el arreglo sí.
   - BUG-01 aparece también por conflicto temporal puro.
3. **v8 = v6 + 2L + drenaje: examen criterio v3, 20/20. Congelado.**
   - **ERR-12:** la "ley `err > 0.6`, 320/320" era una identidad del código.
4. **3T confirmatorio sobre v8: SÍ**, y replicado en semillas nuevas.
   - La primera corrida dio NO por ERR-13: el comparador distinguía `0.0` de `-0.0`.
5. **Etapa 2, conducta.** La frontera hambre–supervivencia mostró que morder veneno con hambre **es la exploración que
   permite revertir**, y que v8 está en el óptimo.
   - Apareció el problema real: **las patas oscilan atadas al veneno** (~20% del tiempo).
   - Un subagente probó "órganos" y el que faltaba era **memoria de trabajo de rechazo**.
   - **v9** se confirmó en semillas nuevas y se congeló. **Etapa 2 cerrada.** (ERR-14, 15 y 16.)
6. **Etapa 3 sobre v9: CERRADA.**
   - Con una regla lineal, ante patrones **nunca vistos**: valor 0.80 frente a 0.50 del control.
   - **Conducta al primer encuentro:** muerde comida nueva 70% y veneno nuevo 15%.
   - XOR no generaliza. La interferencia degrada la fórmula de forma medible.
7. **Re-verificación sobre v9:** 3T y 2K-bis sobreviven. M_max baja un poco y se muere menos.
8. **Etapa 4 (memoria persistente): NO cerrada.**
   - Sin experiencia, la retención es exacta.
   - Aprender C y D mientras A y B no están **borra** A y B (olvido catastrófico).
   - Diagnóstico: **las celdas hijas toman el código** (`mu` no convergida) más la deriva de valor.
   - Heredar el valor ayuda en un mundo igual (−80% de veneno inicial).
9. **Exploración de consolidación (subagente):**
   - **K4, repaso desde un almacén episódico:** retiene, pero la memoria vive en el almacén ("memoria escondida").
   - **K5, `mu` normalizada** (1 línea): arregla la mitad sin almacén.
   - **v10 pendiente de dirección.**
10. **Comunicación, N1** (señal innata de placer/asco + aprendizaje vicario entre dos v9): **no demostrada.**
    - Dos aprendices igual de ignorantes no tienen nada que enseñarse.
    - El contenido de la señal sí importa.
    - Ser dos cuesta +34% de muertes.
    - Diseño completo N0–N3 en `experimentos/etapa5_comunicacion/`.

## 10.3 Lo que se aprendió del método (más valioso que cualquier cifra)
- **Tres veces hoy, pensar antes de correr cambió la pregunta,** y la nueva era mejor:
  - 2P no era un defecto, era exploración;
  - la Etapa 3 nunca había medido conducta;
  - N1 necesita asimetría de información.
- **Los errores del día se atraparon antes de construir encima.**
  - ERR-12 a ERR-16: identidad presentada como evidencia, comparador de texto, banda más estrecha que el ruido, línea
    base mal puesta, y un control que no podía hacer nada.
  - Regla derivada: **antes de fiarse de un control, comprobar que PUEDE cambiar algo**.
- **Subagentes:** sirven para explorar variantes con varianza.
  - Hay que verificar sus cifras desde los JSON y confirmar en el repo con preregistro y semillas nuevas.
  - Si lanzan algo largo, pueden detenerse esperando un aviso que no llega: hay que reanudarlos.

## 10.4 Decisiones que esperan al director
1. **v10:**
   - K5 (`mu` normalizada: arreglo de la regla 2L, 1 línea, sin almacén);
   - K4 (repaso episódico: retiene, pero con almacén explícito, que habría que probar con más estímulos que casillas);
   - o los dos, uno por vez.
2. **N1 rediseñado con asimetría de información** (experto y novato), con preregistro nuevo.
3. **Pendientes:** O7 ("qué hacer sin objetivo"); frontera no lineal (XOR); herencia a lo largo de varias
   generaciones.

---

# 11. DÍA 5 (17 sep 2026) — v11 nace de la evolución, cierra la Etapa 4 y descubre el canje

## 11.1 Para retomar en 30 segundos
```
cd organismo && PYTHONIOENCODING=utf-8 python bateria.py 6 && python bateria_v13.py 6 && python bateria_generaliza.py organismo_v13 10
cd .. && python manifiesto.py --check        # 14 archivos congelados
```
**El tronco es v13** (tag `v13-tronco`): v11 (rápida, hallada por evolución) + vía lenta lineal + puerta de familiaridad.
v11 es el tronco anterior (`v11-tronco`); v10 sólo instrumento (ERR-17). **Antes de congelar cualquier tronco nuevo:**
examen `bateria_vN.py 20` en semillas nuevas **y** `bateria_generaliza.py 20` (ERR-20) **y** revisar todas las
identidades de instrumento (ERR-21/22).

## 11.2 Qué pasó, en orden
1. **JUACO-EVO, generación 1.** Cuatro subagentes LLM propusieron una mutación cada uno, con hipótesis escrita antes;
   cuatro mutaciones ciegas hicieron de control. Ganó `llm_2`: **división por conflicto de signo** (una celda con valor
   consolidado que recibe refuerzo contrario se divide en esa mordida; la hija nace **ciega fuera de los píxeles de su
   patrón**, la madre no se mueve, el valor se **fisiona**).
2. **El control ciego no llegó:** 24 mutaciones en 6 generaciones se quedaron en R 0.5/0.4; el linaje LLM llegó a
   1.0/1.0 en **una** generación. **P1 (aceleración) sostenida**, con el límite declarado de que el operador ciego sólo
   escala constantes.
3. **Dos huecos del evaluador atrapados por la auditoría**, no por el criterio: **ERR-18** (una mutación ciega bajó las
   muertes subiendo la energía tras morir: constitución, no aprendizaje) y **ERR-19** (una mutación **nula** ganaba por
   un error de contabilidad del selector). Los dos corregidos y registrados.
4. **v11 confirmado en semillas 41–60 y congelado:** retención **20/20** (v9 0/20, v10 2/20), examen criterio v3
   **8/8**, y capacidad multiplicada. **Etapa 4 cerrada** en el mundo de 4 estímulos.
5. **Mundo grande (10 píxeles, 60 estímulos):** v11 domina **50 de 60** (v10: 9), con menos celdas y sin colapsar.
   **G3 refutada:** el límite **no** es quedarse sin celdas; al agotarlas **se degrada suavemente** (error 0.02 → 0.16)
   en vez de caer por un precipicio.
6. **La re-verificación encontró el precio.** 3T **sobrevive y mejora** (`sep` 3.96 con 6 divisiones frente a 3.91 con
   16), pero la **Etapa 3 se cae**: ante patrones nunca vistos, el acierto de valor baja de **0.80** (v9 y v10) a
   **0.60** (azar 0.50). **v11 es un canje, no una mejora universal.**

## 11.3 El hallazgo del día (confirmado en 20 semillas, preregistrado)
> **La generalización de v9 ERA su interferencia.**

En v9, las celdas **hijas** ocupan **1.00 de cada 3** celdas del código de un patrón que nunca las entrenó: se cuelan
en todas partes, y esa **fuga** es la que transporta el valor aprendido hacia lo nuevo. En v11, con la hija ciega, la
fuga cae a **0.08** y la generalización se va con ella. Medido: `fuga` v9 1.00, v10 0.65, v11 0.08; Spearman entre
fuga y acierto **+0.601** sobre 60 corridas, **+0.328 dentro de v9** (sin el brazo como confusor) y **+0.579** en las
15 semillas que no se habían mirado (`PREREGISTRO_fuga.md`, datos `fuga_20260917_152707`, D1–D4 sostenidas).

**Consecuencia:** no son dos propiedades, es una sola vista por los dos lados. Tapar la fuga cura el olvido y mata la
generalización. Es la predicción de **complementary learning systems** (McClelland, McNaughton y O'Reilly, 1995);
Sahay (2011) y Clelland (2009) describen separación **sin** ese costo, y en este sistema el costo existe y se puede
señalar con el dedo: **una línea de código**.

## 11.3b El canje se rompió: v13, dos vías (tarde del día 5)
Lo que ninguna perilla ni la hija que madura lograron, lo logró un **cambio de arquitectura** que la teoría pedía y
nuestros datos exigían: **dos vías**. La rápida es v11 (separa, recuerda; hallada por evolución). La lenta es una
lectura **lineal de la retina** (solapa, generaliza). Cada una aprende de **su** error, y la boca consulta la rápida
sólo cuando el patrón le es **familiar** (las tres celdas de su código consolidadas); si no, a la lenta. Un solo error
compartido **no** sirve (la rápida deja sin error a la lenta): fue el primer brazo y falló, declarado antes.

Resultado, todo en semillas que nadie había tocado: retención **20/20** y acierto en nunca vistos **0.85** (61–80);
examen 8/8 y generalización 0.80 / 0.89 (101–120). **Etapas 3 y 4 cerradas sobre el mismo tronco.**

**ERR-21, y cómo se resolvió sin trampa:** el control negativo del examen ("sin plasticidad no separa A∩B=3") tenía la
premisa de una sola vía; v13 lo "pasaba" porque la lenta separa por píxeles. Se desdobló (3': la rápida sola debe fallar,
0/20; 3'': la lenta separa, 20/20), **se escribió el criterio nuevo y se repitió el examen entero en 20 semillas nuevas**
antes de congelar. Ésa es la forma honesta de cambiar un criterio después de ver un dato.

## 11.3c Etapa 5, primer peldaño: enseñar y corregir (noche del día 5)
Con v13 como base, el experimento que ayer falló (dos novatos iguales no tienen nada que decirse) pasó al cambiar la
**asimetría**, no el mecanismo: un **experto** (hereda su estado) y un **novato** (en blanco), y la señal es la
**conducta visible** (+ si muerde, − si rechaza), honesta por construcción. El novato aprende que B es veneno con
**7–8 mordidas propias en vez de 19** (20/20 en dos lotes de semillas); la señal barajada no es neutra, es **destructiva**;
y cuando el mundo se invierte, **el novato corrige al experto** (extingue su miedo tres veces antes) a cambio de un
pequeño coste de confianza. Simbiosis en el tiempo, medida. **Etapa 5 N1 cerrada**; quedan N2 y N3.

## 11.4 Lo que queda abierto
- ~~3T y capacidad sobre v13~~ — hecho: 3T sobrevive (T1–T6); capacidad cae de 50 a 35 de 60 (canje puerta/capacidad,
  predicho). ERR-22: la identidad C2b ≡ C1 no aplica a dos vías. Salida anotada: puerta que consulte la lenta sólo con
  la rápida vacía (a preregistrar).
- ~~v12: ceguera graduada~~ — hecho: mapa del canje, H sostenida; la hija madura, refutada. v13 lo rompió. Se preregistra como **mapa del canje**, no como
  solución: la predicción escrita es que **ningún valor logra a la vez** la retención de v11 y la generalización de v9.
- **El candidato que sí podría romperlo** (una hija que fuga pero **deja de aprender al madurar**) queda anotado en la
  nota de diseño; **no se diseña todavía**.
- **ERR-20 y su corrección:** la generalización entra a la regresión (ver registro).
- Etapa 5: **N2** (significado emergente, juego de señalización) y **N3** (sentidos complementarios / XOR entre dos).
- O7 (qué hacer sin objetivo); techo de capacidad; la puerta que consulte la lenta sólo con la rápida vacía (rama).

## 11.5 N2 (significado emergente): línea CERRADA por hoy tras cinco diseños; plan del debate en marcha
Cinco diseños preregistrados (N2, N2b, N2c, N2d, N2e; 500 corridas; `datos/N2*_s1-20_20260917_*`). **Lo que emerge:** con
refuerzo por ventaja y el símbolo como sesgo en la decisión, entre dos v13 aparece una **convención de dos símbolos**
que ninguno tenía, arbitraria por semilla (~13/20) y que **muere al barajar**. **Lo que no:** magnitud útil para el
receptor (contraste ±0.4, luego ±0.1) ni beneficio del 30 % (llegó al 21–23 %, pareado 15/20 en N2d). **Causa,
verificada con humo instrumentado:** el mundo muestrea asimétrico (la comida desaparece al comerla; el veneno se queda y
se señala 36.000 veces contra 564) y la recompensa es asimétrica (−3/+1); ningún receptor acumula "positivo". Vocabulario
permitido: *emerge una convención; transmite poco*. Reabrir sólo cambiando el mundo (equilibrar visitas y escala).

**Después del cierre:** cinco agentes Sonnet investigaron los niveles 5–9 y un sexto los confrontó
(`registro/investigacion/nivel5..9*.md`, `DEBATE_y_plan_5a10.md`). Orden adoptado (regla 12): **(1) 3T con historia de 2
y 3 pasos** (`experimentos/nivel7_3T_k/`, preregistrado y corriendo al cierre; k=1 es bit a bit el 3T de siempre) →
(2) tabla posición→código con teletransporte y control de barajado (nivel 6) → (3) mundo social con control de
saciedad (cierra el nivel 5 y resuelve N3) → (4) mundo largo con cambio, 4 brazos (niveles 8+9). Se saltan XOR y N2.
Criterio de parada honesto: si 5–6 mecanismos compran capacidad con el mismo canje, el límite es el presupuesto fijo
de células. `REPOS_cercanos.md`: no hay repo público con los cinco ejes de JUACO; préstamos posibles: Roth–Erev
(`demonstrator-game`) para N2, OpenEvolve/ShinkaEvolve como arnés para JUACO-EVO.

## 11.6 El plan del debate, ejecutado en una noche (17 sep, 19:00–20:30): qué quedó y qué no

Regla 12 en acto: cuatro experimentos preregistrados, construidos por anclas con identidad bit a bit, corridos y
registrados sin pedir permiso; el director audita `REGISTRO_etapas_1_2.md` (entradas de esta noche, al final).

| # | experimento | veredicto | lo que queda escrito |
|---|---|---|---|
| 1 | **3T-k** (nivel 7): historia de 1, 2 y 3 pasos con distractores | ✅ **compone hasta 3**, replicado 21–40 | sep 3.97 / 3.74 / 2.24; control barajado ≈ 0; 20/20 por k |
| 2 | **Mapa** (nivel 6): tabla posición→patrón + teletransporte, mundo con `r_vis = 3` | ✅ **elige el lado de la comida recordada**, replicado | 0.81/0.80 contra 0.48/0.50; invertido 0.11 (huye); come 490 contra 332, 20/20. Premisa del informe corregida: la retina del tronco ve el objeto más cercano de todo el anillo |
| 3 | **N3 sentidos complementarios** (nivel 5): receptor ciego a la regla + conducta del que la ve | ❌ N3, N3b (ERR-23), N3c (montaje inválido); **✅ N3d TRANSFIERE** (receptor ciego 0.515 → 0.822; controles 0.48/0.51; 20/20; réplica 81–100 igual: 0.811 contra 0.516 solo, barajada 0.487, emisor que no sabe 0.515, 20/20 en los tres (N3d_s81-100_20260917_201205, 454fb54abddb2146)) | la conducta ajena **gobierna** la boca del receptor (barajada 0.68, emisor que no sabe 0.69, 20/20) pero el mundo no dejaba probar comida (N3b) o el receptor no era ciego (N3c) |
| 4 | **Mundo largo** (niveles 8+9): 50 patrones nuevos + inversión de regla | ❌ compuesto; **3 hallazgos** | v13 sigue aprendiendo hasta los 50 (0.80; predije 0.55–0.70); se recupera de la inversión en ~2 000 pasos (18/20); **el mapa daña la adquisición** (0.70 contra 0.88): explota lo recordado y explora menos |

**Errores nuevos:** ERR-23 (canal social simétrico + acierto no balanceado; corregido en N3b con semillas nuevas).
**Lecturas honestas:** no hay "planificación", "lenguaje" ni "autonomía": hay composición de 3 pasos, elección de
dirección por memoria de lugar, recuperación ante cambio y aprendizaje sostenido hasta el techo de la retina (63
patrones posibles). **Lo que sigue** (orden sugerido): (a) cerrar N3d y, si pasa, replicar; (b) guardar `W` por patrón
en el mundo largo para separar olvido de inversión (R1); (c) medir si las divisiones extra de 3T-k cuestan capacidad;
(d) el canje exploración/explotación del mapa como nivel 8 propio (curiosidad por progreso de error, nivel8 §3);
(e) XOR como límite de lectura (apuesta de frontera del debate). Instrumentos: `experimentos/nivel7_3T_k/`,
`nivel6_mapa/`, `etapa5_comunicacion/{mundo_social_n3,corre_N3*}`, `nivel8_mundo_largo/`.

## 11.7 Día 6 (noche del 17-sep, 20:30–22:30): plan del debate ejecutado con equipo

Regla 12 en acto, ahora con equipo (`registro/EQUIPO.md`): bloque 0 y bloque 1 del plan del día 6 (`registro/PLAN.md`)
corridos y registrados; bloque 2 corrido y refutado; bloques 3 y 3b corridos y refutados (con diagnóstico).

| bloque | veredicto | cifra que manda | dato |
|---|---|---|---|
| **0** — gemelo compilado del tronco | ✅ HECHO (tronco); pendiente (mundos) | bit a bit **72/72** (12 configuraciones × 6 semillas), **×78** (100k pasos: 4.05 s → 0.05 s) | `organismo/identidad_rapido.py` (sin log en `datos/`) |
| **1a** — 3T-k, k = 4 y 5 | k=4 **COMPONE**; k=5 **NO** | k=4: sep 1.99 [1.71,3.24], 20/20, celdas 72 · k=5: lift_q4 **0.144 < 0.15**, celdas 90/90 (pool agotado) | `datos/3T_k45_s1-20_20260917_204451.log` / `.json` |
| **1b** — mundo largo s21–40, `W` por patrón | Réplica sostenida; retención de lo ausente MALA | nunca invertidos: V13 **0.67** / MAPA **0.50** (predicción ≥0.70: NO) | `datos/largo_s21-40_20260917_204840.log` / `.json` |
| **1c** — N3d mudo | **OBEDECE**, no aprende | CONV_MUDO 0.503 [0.50,0.51] ≈ SOLO_R 0.515 (Δ=0.012) contra CONV 0.822; muertes 189 contra 86 | `datos/N3dmudo_s61-80_20260917_205345.log` / `.json` |
| **2** — curiosidad por progreso de error | ❌ **REFUTADA** | MAPA_CUR 0.700 = MAPA 0.704 = control barajado 0.700; P1 NO, P3 NO | `datos/curiosidad_s41-60_20260917_211739.log` / `.json` |
| **3** — XOR como límite de lectura | ❌ **REFUTADO como estaba escrito** | cuadrática xor01 0.438 = lineal 0.438; random15 0.50; regresión px0/azar intacta; pero `W_lenta(P0·P1)` = −2.65 (la lectura representa XOR) | `datos/xor_lectura_s1-20_20260917_213124.log` / `.json` |
| **3b** — ¿la puerta esconde la vía lenta? | ❌ **NO** | vía lenta sola 0.50 en xor01; familiar 0.33; sin puerta no mejora → el límite es la **regla** de la vía lenta (reparte el error por igual; marginales de P0/P1 drenados a cero) | `datos/xor_3b_s21-40_20260917_213752.log` / `.json` |

**Del organismo:** los cuatro bloques cerrados miden límites, no capacidades nuevas. **Compone hasta 4** pasos de
historia con distractores (sep 1.99 [1.71,3.24], 20/20); a profundidad 5 la separación sobrevive (1.94, 19/20) pero
el pool de celdas se agota (90/90) y la ventaja conductual cae al filo (lift_q4 0.144 contra el criterio 0.15): el
techo es presupuesto de celdas, no la composición en sí. En el mundo largo, replicado en semillas 21–40, v13 **no
retiene** lo que deja de ver mientras aprende con las mismas celdas (nunca invertidos: 0.67 contra 0.50 del mapa,
ambos bajo la predicción ≥0.70): es **interferencia por códigos compartidos** —la misma causa que "generalización =
interferencia"— y **no es la inversión** que se había previsto medir. Con N3d mudo, el receptor ciego por
construcción, al quitarle la señal, no cae al nivel de quien nunca escuchó (0.503 contra 0.515 solo; con señal
0.822): **obedece, no aprende**, y la obediencia le **crea dependencia** (189 muertes contra 86). Y la curiosidad
por progreso de error, candidata a devolverle al mapa la exploración que le cuesta, quedó **refutada**: el brazo con
curiosidad (0.700) no se distingue del mapa solo (0.704) ni de su control barajado (0.700); el sesgo actúa sólo
sobre sitios ya recordados, no explora.

**Del método:** el día dejó errores de instrumento, no de organismo, y una regla nueva. El bloque de curiosidad tuvo
**dos arranques abortados sin datos por un `KeyError` del runner** (commit `d4367e0`) antes de la corrida que sí
completó las 80 (semillas 41–60); se cuenta porque el protocolo numera todo fallo de instrumento, no sólo los de
mundo o medida. El gemelo compilado del tronco (`organismo_v13_rapido.py`, numba) llegó a identidad **bit a bit
72/72** (12 configuraciones × 6 semillas) con **×78** de velocidad, y de ahí la regla que gobierna todo lo demás:
**"un gemelo que no sea bit a bit sólo explora, nunca confirma"**; por eso los mundos (`mundo_temporal_k`,
`mundo_mapa`, `mundo_social_n3`, `mundo_largo`) siguen en Python puro, y ninguna cifra de hoy se apoyó en un gemelo
sin esa prueba.

**Para el día 7** manda lo escrito en `PLAN.md`. El bloque 3 cerró: XOR no es un límite de dimensión (random15 =
cuadrática = lineal) ni de la puerta (3b), sino de la **regla de la vía lenta**; el bloque 3c (regla delta con signo u otra)
lo diseña un trío de agentes con puente (`registro/investigacion/PUENTE_xor.md`). El bloque 4 (decisión de tronco v14) queda sin objeto mientras el bloque 2 siga
refutado: v13 sigue siendo el tronco y mapa/`gamma_soc` quedan como órganos de experimento validados en su mundo.
Faltan el bloque 5 (N2b en el mundo con reaparición) y el bloque 6 (allostasis, rama exploratoria). En
paralelo, según `EQUIPO.md`, siguen en curso los **compiladores de mundos** (gemelos numba de los mundos,
pendientes desde el bloque 0), el diseño de **novedad de sitio** (siguiente candidato al canje exploración/
explotación del mapa) y **N2f**; ninguno tiene todavía entrada en el registro.

**Vocabulario permitido, por resultado** (copiado del registro; regla 6 `EQUIPO.md`: *"lo que se declara es lo que
se midió, no 'planifica', 'entiende', 'lenguaje' sin la prueba"*):
- **1a (3T-k):** "compone hasta 4 pasos de historia con distractores; a 5 se agota el pool y la ventaja se diluye."
- **1b (mundo largo):** "no retiene [...] interferencia por códigos compartidos [...] No es la inversión."
- **1c (N3d mudo):** "la conducta ajena gobierna la decisión; no enseña" — "obedece, no aprende" — "la obediencia
  crea dependencia."
- **2 (curiosidad):** "la curiosidad por progreso del error no explora" — "el canje exploración / explotación del
  mapa sigue abierto."
- **0:** sin vocabulario de conducta (resultado de instrumento: identidad bit a bit / velocidad).
- **3 y 3b:** "XOR no se generaliza en v13; la lectura cuadrática lo representa pero su regla no lo separa."

## 12. Plan del día 6 (escrito al cierre del día 5; es el bloque vigente de `PLAN.md`)
El orden y las predicciones están en `registro/PLAN.md` (bloque "ORDEN VIGENTE PARA EL DÍA 6"). En una línea cada uno:
**0** gemelo rápido del organismo — **hecho para el tronco** (`organismo_v13_rapido.py`, bit a bit 72/72, ×78; faltan los
mundos); **1** ✅ cabos: 3T-k compone hasta 4 (a 5 se agota el pool); retención de lo ausente 0.67/0.50 = interferencia; N3d mudo
0.503 = obedece, no enseña (y crea dependencia);
**2** curiosidad por progreso de error contra el canje exploración/explotación del mapa (el nivel 8 real); **3** XOR como
límite de lectura (vía lenta cuadrática, Kenyon congelado); **4** v14 sólo si pasa el 2; **5** N2b en el mundo con
reaparición; **6** rama allostasis. **Estado de los órganos:** el tronco es v13; la tabla `M` (mapa) y `gamma_soc`
(conducta ajena en la decisión) son **órganos de experimento validados en su mundo**, no del tronco: el mapa cobra la
comida en exploración y todavía no se ha probado que no dañe retención/generalización en el examen. Todo está
commiteado (`git log`) y respaldado en `JUACO/respaldo/juaco_bundle_20260917_*.bundle`; **no hay remoto**: crear uno
(GitHub privado) es la primera decisión que espera al director.

## 11.5-viejo Estado al cierre de la sesión (noche del 17 sep) y cómo retomar N2 (superado por lo de arriba)
- **Lo que está corriendo o acaba de terminar:** `experimentos/etapa5_comunicacion/corre_N2.py` (N2, significado
  emergente). Su preregistro es `PREREGISTRO_N2.md` (escrito antes; criterios E1–E5, K1–K2, predicciones y refutación).
  Salida en `datos/N2_s1-20_<fecha>.log/.json`. **Nada de N2 está registrado todavía en `REGISTRO_etapas_1_2.md`.**
- **Qué hacer con el resultado:** (1) leer el `VEREDICTO N2` del log; (2) registrarlo en `REGISTRO_etapas_1_2.md` con
  la tabla (SOLO, N0, INNATO, CONV, SHUF: veneno del novato, consistencia y `Pq` del experto, `M` del novato);
  (3) si E1–E5 pasan, correr `corre_N2.py --desde 21` y sólo entonces escribir "N2 cerrado"; si fallan, diagnosticar el
  eslabón que no cerró (¿`Pq` no se separa? ¿`M` no se separa? ¿el novato aprende solo antes?) **sin recalibrar**, y
  preregistrar otro mundo o refuerzo; (4) commit con los datos; (5) actualizar `CLAUDE.md` (bloque día 5) y este HANDOFF.
- **Mecanismo de N2, en una línea:** el experto emite uno de dos símbolos sin significado según su propio estado
  (muerde/rechaza), con preferencias que nacen al azar y se refuerzan si la conducta del receptor coincide con la suya;
  el novato aprende qué predice cada símbolo sólo por sus propias consecuencias, y cuando ya cree saberlo, actualiza su
  valor del patrón por las dos vías. Control: barajar los símbolos en la entrega debe destruir el código.
- **Después de N2:** N3; rama de capacidad (puerta con la rápida vacía); consolidación y publicación.


## 13. Lista de chequeo por nivel del brief (3 → 8), al 17-sep 21:00 — hecho / falta / estimación honesta

| nivel | hecho (con dato) | falta | ~ |
|---|---|---|---|
| **3 generalización** | lineal: Etapa 3 cerrada (v9), recuperada en v13 tras ERR-20; v14: 1.000 / 0.95 · **no lineal (XOR), línea CERRADA 18 sep 07:47: con 8 ejemplos exige un prior de pares y con él bastan 7–10 exposiciones (1.000 estricta ×2 series); con 14 ejemplos no hace falta prior (1.000); con 8 sin prior no lo aprende nadie (9 de 15 hipótesis empatadas)** | llevar la memoria por pares al tronco (candidato v15) | 90 % |
| **4 memoria persistente** | **alias de código (18 sep, mundo vivo + bloque de la sal): con K = 3 dos estímulos pueden compartir código (2/20 semillas con 4 estímulos) y el que no informa hereda el valor del otro, que pierde la mitad del miedo; no depende de la necesidad ni lo repara la puerta → **REPARADO (B-5, 09:07 y réplica 09:12, 9 + 9 semillas ALIAS): la división por conflicto disparada por R = 0 bajo retina distinta deja la sal en 0.0 y el veneno en −3.0, muertes a la mitad, tronco intacto por inercia exacta; candidato a v15, decide el director** · **puerta por evidencia del código (creación B): recupera la capacidad de v11 en el paso largo (`N*` 50.5 contra 35 de v13) con la generalización intacta; examen v3' 19/20 en E2 en 101–120 y **8/8 en la réplica 121–140 → tercer candidato a v14** (`PROPUESTA_v14.md`)** · retención 20/20 (v11/v13), capacidad ×5 (50/60 v11; 35/60 v13 por la puerta), examen v3' | retención de lo **ausente** bajo interferencia (0.67 a 150k pasos); canje puerta/capacidad; olvido dirigido | 75 % |
| **5 comunicación / transferencia** | N1 experto→novato (replicado); N3d transferencia entre sensores por conducta (**3 series**: 0.822/0.811/0.811, la tercera con el gemelo compilado); mudo = obedece, crea dependencia | **N2 cerrado con dos mundos** (6 diseños ❌; N2f v3 con montaje válido; INNATO 60 vs 278: el canal serviría con significado dado); que el receptor aprenda algo propio; XOR entre dos | 50 % |
| **6 planificación** | mapa: elige la dirección hacia comida recordada fuera de la vista (3 series); **dos metas y rodeo: elige la más cercana y rodea el veneno recordado (2 series, subconjunto válido 14/14 y 16/16 pareado)** **2D (17×13, 4 direcciones, identidad 60/60 con el anillo): no rodea, se aleja (0/20); rodeo falso confirmado (0.05, se desvía sin motivo); encadena A→B si borra el sitio comido (0.95 contra 0.50, 18/20)** | horizonte 2 (H2 +0.475 donde discrimina; mundo sin potencia, 6/20), planificar de verdad exige otro mecanismo; `M` que se degrade; canje exploración/explotación cerrado como estructural (el mapa no entra al tronco) | 55 % |
| **7 composición** | 3T-k: historia de hasta **3** pasos con distractores replicado (a 4: separa 20/20 pero la ventaja conductual no cruza 0.15 en la réplica); **el techo NO es el pool de celdas** (creación B: duplicar el pool a 180 no devuelve nada; lo que se agota es la evidencia por código); **hija dispersa** (la hija nace ciega a parte del patrón): compone mejor a k=4/5 (lift 0.25–0.33, > v13 18/20, > máscara al azar 16/20) con la mitad de celdas en mediana, ahorro 16/20 en 61–80 (cayó por la letra) y **19/20 en 81–100 (pasa la letra original)** → **REPLICADA: compone historias más profundas con la mitad de celdas**; **v13D NO REGRESIONA (examen v3' 8/8, G1 0.80 / G2 0.83, inerte en 6 px) → candidata a v14 (`registro/PROPUESTA_v14.md`, rama `v14-candidato`; decisión del director)** | composición de rasgos: **XOR no es límite de dimensión ni de puerta sino de la REGLA de la vía lenta** (3, 3b, trío); 3d pendiente; composición social (XOR entre dos) | 55 % |
| **8 aprendizaje abierto** | **probar cuando no me reconozco (creación C): recuperación tras la inversión 0.26× v13 (20/20), controles de cantidad y momento vencidos, retención y generalización intactas; el sesgo no se apaga del todo (15/20 ×2); **REPLICADO en 61–80 (0.22×)**; **la sorpresa del mundo (ΔE) en la boca recupera 7× más rápido (0.14× ×2), se apaga sola y sin más veneno; **serie 81–100: pasa retención (≥ 19/20 × 6) y generalización (G1 0.90) → candidato con tres series; **examen v3'' completo (v13E): retención 8/8 pero G1 0.750 < 0.80 → fuera de la propuesta de v14 a la dosis probada (coste 0.05 en generalización de valor; dosis a preregistrar)**; el automodelo pasa todo en la tercera serie (apagado 17/20)** · metaplasticidad por masa de conflicto (creación A) refutada en 41–60: retención de lo ausente 0.667 = base, +73 % muertes · sigue aprendiendo hasta el techo de la retina (50 patrones, 0.80); se recupera del cambio de regla (2–4k pasos, 18/20); el mapa cobra exploración | retención de lo ausente (0.67 = interferencia); **canje del mapa cerrado como estructural** (curiosidad ❌, novedad de sitio ❌ ×2, saturación ❌: la comida recordada atrae y el organismo deja de explorar); dominio distinto del anillo; olvido/fusión | 40 % |
| **9 modelo de sí mismo / mundo vivo** | predictor de la propia energía (bloque 6); la sorpresa en la boca recupera 4–7× antes (tres series); **mundo vivo (línea F, 18 sep): dos necesidades con dos muertes, valor por necesidad, sorpresa específica; resuelve el XOR necesidad × estímulo (1.0, 20/20) en 11 exposiciones; puede equivocarse de objetivo (allostasis mínima medida); **propósito y reproducción (peldaño 2, 09:16): la ventana de viabilidad como medida de reproducción SE TIRÓ (premia atracones que mueren más); saciado, el valor por el cuello de botella veta la sal (0.80 → 0.00) y leer el mínimo de las dos filas (CUELLO_MIN) basta: la tercera necesidad sobra; **bloque 2 (09:43 + réplica 09:45, 8/8 ×2): la medida r = descendientes − muertes ordena como la supervivencia (ERR-40 resuelto) y la lectura pesimista saciado (CUELLO_MIN) lleva el linaje al filo del reemplazo (r ≈ 0 contra −73/−75 del tronco); la tercera necesidad se retira — DECLARADO; siguiente: población con herencia y muerte real** | supervivencia con margen medible (enmienda 2, réplica 201–220); alias de código K = 3 (la sal y el veneno comparten código en 2/20 semillas: bloque preregistrado); propósito y reproducción como medida | 30 % |
| (9 autonomía) | recuperación medida ante cambio no avisado | allostasis (bloque 6), meta propia | 20 % |

Los porcentajes son juicio mío, no medida: "100 %" sería el nivel cerrado con réplica y sin cabos abiertos en su fila.


## 14. Cierre del día 6 (17 sep, 23:00) — con equipo

Resultados de la segunda mitad de la noche (todo en `REGISTRO_etapas_1_2.md`, entradas del día 6): bloque 2 ❌ (curiosidad
por progreso), bloque 2 bis ❌ en dos dosis (novedad de sitio: 0.800 y 0.841 contra 0.85; mueve el canje, no lo rompe),
bloque 3 ❌ y 3b ❌ (XOR: la lectura cuadrática representa el producto, la regla de la vía lenta no lo separa; ni dimensión
ni puerta), trío XOR → propuesta 3d firmada (hipótesis), bloque 5 ❌ con montaje válido (N2 cerrado con dos mundos).
Instrumentos: gemelos compilados bit a bit del tronco, 3T-k, mapa, mundo de regla/XOR (integrados, con `--rapido`),
social (en actualización), mundo largo (en construcción); regla 9 de `EQUIPO.md` (recursión + `cache=True` segmenta).
Errores de la noche: KeyError del runner del bloque 2 (dos arranques sin datos), `/tmp` de Git Bash ≠ `/tmp` de Python,
arnés de N2f que exige ruta (mi cadena no la pasó: se repitió aparte, 8/8). **Día 7:** ver `PLAN.md` (bloques 3d, 6;
canje del mapa sólo si ataca la escala del recuerdo de veneno; nivel 6 dos metas y rodeo; N2 sólo con un mecanismo de
significado por predicción).

## 15. Cierre del día 7 y madrugada del 18 (17 sep 23:00 → 18 sep 01:40) — la célula de creación

### 15.1 Qué se decidió y por qué

Director ausente ~8 h desde las 23:00. Orden vigente (`registro/PLAN.md`, "Madrugada del 18"): *"un Pool a la vez,
cada bloque con preregistro, identidad dentro del runner y registro al terminar"*; decisiones del coordinador,
documentadas para que el director audite después (regla 12 de `CLAUDE.md`: autonomía dentro del método, sin pedir
permiso, sin declarar nada fuera del protocolo). Por qué tanta disciplina sin supervisión: en `EQUIPO.md`, "el
método manda sobre la misión — un resultado que no pasa por el protocolo no cuenta, aunque apunte hacia la misión".
**Un Pool a la vez** (`EQUIPO.md`, regla 3 y "Coordinación de CPU"): los tres creadores y el explorador sólo corren
mini-pruebas de un proceso, en copias por anclas (`experimentos/creacion_<X>/`), sin tocar originales ni commitear;
el coordinador es el único con `Pool`, uno detrás de otro, revisando antes qué procesos python siguen vivos. Nada
toca el tronco sin examen v3' + baterías + réplica; la decisión de v14 queda para el director.

### 15.2 Bloques de la noche

| bloque | nivel | veredicto | números clave | datos |
|---|---|---|---|---|
| Escala del mapa (2 ter) | 8, estructural | REFUTADA → canje CERRADO como estructural | `V13_adq` 0.8875 (ancla mal transcrita: 0.887); `MAPA_adq` 0.700 | `escala_s81-100_20260917_230039` |
| 3e, oráculo de rasgos | 3 (XOR) | ❌ REFUTADO | `acc_lenta` 0.625 < 0.80 con {P0,P1,P0·P1,1} regalados | `xor_3e_s61-80_20260917_231444` |
| 6, allostasis (rama) | 9 | P1 NO / P3 OK | recuperación 7159 contra 8360 (pareado 6/10); sorpresa 0.0→0.83 | `allostasis_s1-10_20260917_231652` |
| Rodeo 41–60 y 61–80 + subconjunto | 6 | ✅ REPLICADO | R1 mediana 0.725/0.750; pareado del subconjunto 14/14 y 16/16 | `rodeo_s41-60_20260917_232338` · `s61-80_20260917_232711` |
| N3d, tercera serie | 5 | ✅ TRANSFIERE ×3 | 0.822 / 0.811 / 0.811 | `N3d_s101-120_20260917_233033` |
| Auditoría del día 7 (+ ERR-25, 00:35) | método | sin bloqueantes | K0 corregido (ancla mal copiada); puerta confunde no-aprendido/cancelado (`n_techo`=0 en el examen) | `AUDITORIA_dia7_20260917.md` |
| B-1, 61–80 y 81–100 | 7 | ❌ por la letra → ✅ réplica | P1 (ahorro de celdas) 16/20 → 19/20; `lift_q4` mediana 0.251 → 0.352 | `hija_dispersa_s61-80_20260918_000202` · `s81-100_20260918_000954` |
| A-2, metaplasticidad | 8 | ❌ REFUTADA | `ret_no_inv` 0.667 = base (7/20 pareado); muertes +73 % | `metaplasticidad_s41-60_20260918_000740` |
| A-1/A-3, paquetes listos | 3 (XOR) / 4 | instrumento listo; 3f no se corre | identidad `v13q4` 16/16; humo de A-3 idéntico 3/3 | sin `Pool` todavía |
| C-P1, 41–60 y 61–80 | 9 | ✅ SELF-TEST; dE-TEST candidato | recuperación 0.263×/0.221×; dE-TEST 0.143×/0.144× | `probar_si_mismo_s41-60_20260918_001756` · `s61-80_20260918_003640` |
| A-3, vector único | 4 | ✅ CONFIRMADO | `acc` idéntica 60/60; `max\|ΔW\|` 3.3e−15 | `vector_unico_s101-120_20260918_003352` |
| Auditoría de la madrugada (+ ERR-26/27/28) | método | sin bloqueantes | enmiendas sin ERR numerado a tiempo; import ambiguo sin consecuencia | `AUDITORIA_madrugada18_20260918.md` |
| Nivel 6 en 2D | 6 | ❌ refutado, en la forma predicha | T1 0.000 (pareado 0/20); rodeo falso 0.05 | `2d_s21-40_20260918_010836` |

### 15.3 Lo que aportó la célula de creación

Tres creadores Opus (`registro/investigacion/PUENTE_creacion.md`) — **A** matemática del aprendizaje local, **B**
representación y capacidad, **C** modelo de sí mismo y significado — más un explorador Haiku a demanda; todo en
copias por anclas, identidad bit a bit antes de mirar números, mini-pruebas de un proceso, cero `Pool`, cero commits.

**Cinco hallazgos que cambian el mapa:**
- **El pool de celdas no es el techo** (B1, A5): duplicar 90→180 no devuelve nada (`lift_q4` 0.099 contra 0.112); el
  pool lleno retiene MÁS que el libre (`corr` +0.24/+0.32, al revés de lo esperado) — se agota la evidencia por
  código, no las celdas.
- **Los dos canales son un valor con signo más una masa de conflicto** (A3): `(Wp,Wn)↔(W=Wp−Wn, m=min(Wp,Wn))` es
  biyección exacta (`max|ΔW|` 2.5e−14); `lam` sólo olvida `m` — por eso la vía lenta lleva la mitad de la memoria sin
  cambiar la conducta (A-3, 60/60).
- **El suelo del sesgo de C-P1 es la cota de oráculo** (C7): predecir la propia acción tiene error mínimo `2p(1−p)` >
  0 aun con predictor perfecto; predecir ΔE (constante determinista) da error 0 — SELF-TEST no se apaga del todo (P4
  15/20 ×2), dE-TEST sí (20/20 ×2).
- **La puerta confunde "no aprendido" con "cancelado"** (ERR-25, B4): el 100 % de lo que v13 manda a la vía lenta ya
  se había mordido ≥5 veces — pregunta "¿tengo su valor sin repartir?", no "¿lo he visto?".
- **Dónde entra la sorpresa importa más que cuál** (C1-ter, C7): el predictor de ΔE del bloque 6 puesto en `eta` no
  sirve (0.856×, refutado); puesto en la boca (dE-TEST), recupera 7× más rápido (0.14×).

**Lo refutado, con el mismo rigor:** ninguna geometría alternativa de la vía lenta (L1/Winnow, máximo margen,
encogimiento por grado o frecuencia) llega a XOR (A1); que la fisión de v11 sea consolidación y el pool lleno retenga
MENOS (A5/C5, su propio corolario) cae con datos ya existentes; la metaplasticidad por masa de conflicto no frena el
olvido en 20 semillas (A-2); reciclar celdas por costo energético se retira sin preregistrar, porque B1 y A5 ya
habían cerrado los dos regímenes candidatos (C-P3); y restar la cota de oráculo al automodelo de C-P1 empeora su
suelo y pierde la prueba de latencia contra dE-TEST (adenda de C7).

### 15.4 Candidatos a órgano y su estado

| candidato | mecanismo | estado al cierre (01:40) |
|---|---|---|
| **Hija dispersa** (B-1) | la hija nace ciega a parte de `P`, no sólo fuera de él | REPLICADA (61–80 refutada por la letra, 81–100 pasa incluso el umbral original); **v13D NO REGRESIONA (01:27): examen v3' 8/8 en 101–120, G1 0.80 / G2 0.83, inerte en 6 px → candidata a v14** (`PROPUESTA_v14.md`, rama `v14-candidato`) |
| **dE-TEST** (C-P1) | la sorpresa del mundo (ΔE) puesta en la boca, no en `eta` | serie 81–100 (01:48): retención ≥ 19/20 × 6 y G1 0.90; tres series 0.14× (20/20 × 3), apagado 20/20 × 3; examen v3'' completo (v13E, 02:45): retención 8/8 pero G1 0.750 < 0.80 a dosis 10; **bloque de dosis (03:32): k = 5 cumple todo a la vez (0.267× en 121–140, 20/20; G1 0.80, G2 0.857, examen 8/8) y REPLICA en 141–160 (0.248×, 20/20; retención 20/20 × 6; G1 0.80) → SEGUNDO CANDIDATO a v14 a dosis 5, con dos series**; el automodelo pasa todo en la tercera serie (apagado 17/20) |
| **B-2** (puerta por código) | cuenta mordidas del código exacto en vez de celdas consolidadas | **montaje completo 41–60 (02:32): `N*` 50.5 = v11 contra 35 de v13 en el paso largo (20 000: 41.5 contra 28, umbral 45 no alcanzado), generalización intacta (px0 1.000 / 0.96), contadores barajados destruyen la ganancia; examen v3' 19/20 en E2 y 8/8 en la réplica 121–140 → TERCER CANDIDATO a v14** (`PROPUESTA_v14.md`, rama `v14-candidato`) |
| **Vector único** (A-3) | la vía lenta como un solo vector con signo, sin canal doble | simplificación con identidad CONFIRMADA (60/60); no compra capacidad nueva, ahorra memoria |

Ninguno entró al tronco esta noche: los dos primeros quedan como candidatos con evidencia completa salvo lo anotado, B-2 en
curso; la decisión de v14 es del director (`registro/PROPUESTA_v14.md`).

### 15.5 Errores nuevos y reglas derivadas

| ERR | qué pasó | consecuencia medida |
|---|---|---|
| **ERR-25** (00:35) | la puerta de familiaridad no distingue "no aprendido" de "cancelado" | `n_techo`=0 en el examen de congelación (no se disparó ahí); riesgo no discutido al diseñar v13 |
| **ERR-26** (B-1) | la "enmienda 1" que bajó P1 de ≥18/20 a ≥14/20 no era un subconjunto (regla 10): era una rebaja lisa del umbral, sin ERR en su momento | inerte — 81–100 pasó también el umbral original |
| **ERR-27** (C-P1) | la forma relativa de P4' se escribió después de ver que la copia literal de P4 fallaba en los datos ya corridos de 41–60 | P4' cuenta como prueba limpia sólo en 61–80 (20/20); 41–60 se reporta como retroactivo |
| **ERR-28** (01:15) | `experimentos/v13_dos_vias/organismo_v13.py` no es el tronco: sus valores por defecto difieren (`eta_s` 0.015→0.0, `puerta` 3→None) y con ellos cambia valor y conducta | sin consecuencia medida en los 70+ archivos que citan su sha; ninguno de los 24 sitios que importan `organismo_v13` a secas antepone esa carpeta |

**Reglas derivadas en `EQUIPO.md`: regla 10** (auditoría del día 7) — un análisis sobre un subconjunto de semillas
sólo vale con enmienda preregistrada ANTES de la serie nueva, calculado por script sobre los JSON (nunca en línea),
con el conjunto completo reportado al lado; si una puerta de validez cae pero la cumple ≥60 % de las semillas, ese
análisis se hace siempre. **Regla 11** (auditoría de la madrugada) — toda enmienda que cambie un umbral o la forma de
un criterio lleva ERR numerado al escribirla, aunque sea antes de la serie nueva y resulte inerte; "candidato a
órgano" sólo con retención y generalización medidas en el mismo brazo.

### 15.6 Cómo retomar, y si vamos bien o mal

**Qué correr primero (regla 1):** `cd organismo && python bateria.py 6 && python bateria_v13.py 6 && python
bateria_generaliza.py organismo_v13 10`. **Qué leer, en orden:** este §15 → `CLAUDE.md` ("Estado día 7") →
`PLAN.md` ("Madrugada del 18", lo que sigue sin marcar) → `PUENTE_creacion.md` ("Propuestas para el coordinador":
B-2 y C-P2/C-P3 sin correr). **Qué completar, en este orden:** (1) HECHO 01:27 — baterías de `organismo_v13D` (8/8; G1 0.80 / G2 0.83); (2) HECHO 01:48 —
serie 81–100 de C-P1 con baterías para dE-TEST (pasan) y latencia (dE arranca antes); (3) HECHO 02:41 — B-2 a escala completa
(41–60 + baterías + réplica del examen 121–140): tercer candidato; (4) HECHO 02:45 — examen v3'' de v13E: fuera a la dosis 10;
(5) HECHO 03:32 — dosis de la sorpresa en la boca: k = 5 candidata (k = 3 no); (6) HECHO 03:55 — composición de los candidatos: por la letra no se
proponen juntos (examen 7/8 por una semilla en E2; generalización 1.000/0.94 y capacidad 51 pasan; composición 0.237 < 0.25),
réplica del examen compuesto en 121–140 → 8/8 (04:03): **propuesta conjunta v14 = v13 + hija dispersa + puerta por código**;
(7) composición de los tres EN CURSO (04:40); (8) DECISIÓN DEL DIRECTOR 04:55 y **v14 CONGELADO 05:05** (v13 + hija dispersa + puerta por código; tag `v14-tronco`; la sorpresa
en la boca a dosis 5 candidata a v15). Después: UN solo frente — aprender sin morder (XOR/N2) — con criterio de parada: tres
bloques preregistrados; si ninguno cruza 0.75 en xor01, techo aceptado, publicar y cambiar de paradigma o cerrar (`registro/PLAN.md`). Abierto sin tocar: XOR 3f (falta la pieza de muestreo,
creador C); N2 sólo con significado por predicción (C-P2, sin instrumento en el mundo social); horizonte 2 del mapa
(sin potencia, 6/20). Un `Pool` a la vez; nada entra a v14 sin examen v3' + baterías + réplica.

**Vamos bien o mal, en dos frases:** Vamos bien: la célula entregó cinco hallazgos verificados con identidad y
control, y dos auditorías que atraparon sus propios errores antes de declarar nada candidato. Vamos mal: ningún
candidato está en el tronco todavía (la decisión es del director), la sorpresa en la boca cobra generalización de valor a la
dosis probada, y XOR y N2 siguen sin un mecanismo que funcione con la dinámica actual del mundo.


### 15.7 Con el director de vuelta (18 sep, 04:10 → 07:15): lo decidido y lo congelado

| hora | decisión / hecho |
|---|---|
| 04:55 | "Sí a todo": congelar v14, cerrarlo, un solo frente (aprender sin morder) con criterio de parada de tres bloques XOR |
| 05:05 | **v14 congelado** = v13 + hija dispersa + puerta por código (tag `v14-tronco`; examen 8/8 en tres rangos; gemelo 196/196 + 42/42) |
| 05:10 | dos organismos en paralelo (SIN reglas locales / CON backprop de laboratorio), exposiciones hasta asociar como medida, grafo |
| 05:35 | bloque 1/3 (A-4): la regla local llega a 1.000 con rasgos dados y 150 exposiciones; el cuello son los rasgos |
| 06:05 | **v14.1 congelado** = v14 con `eta_s` 0.15 y `clip_s` 10 (tag `v14.1-tronco`; examen 8/8 ×2, generalización 1.000 / 0.97–1.00) |
| 06:05 | bloque 2/3 (A-6): con 8 patrones nadie puede seleccionar el rasgo (9 de 15 hipótesis empatadas); con 14, 1.000 en los nunca vistos |
| 06:10 | línea F: mundo vivo (necesidades y estímulos múltiples) — diseño listo con ancla 37/37, no se corre hasta el veredicto de XOR |
| 06:45 | revisión de rumbo: XOR columna vertebral; B-5 y N2 decidible laterales de un bloque; mundo vivo sólo diseño |
| 07:10 | **ERR-35**: la línea XOR se cierra por el mínimo de ejemplos con el que generaliza (14 sí, 11 no, 8 nadie); bloque 3/3 con la sala de agentes y `ntr = 14` de control |

Sala de agentes (workflow "enjambre"): 5 investigadores de literatura 2019–2026, un jefe que elige 4 mecanismos, 4 mini-equipos con
identidad y mini-prueba, 2 refutadores por paquete, un sintetizador → `registro/investigacion/ENJAMBRE_xor_20260918.md`. Cerradas
esta madrugada por la letra: metaplasticidad (A-2), consolidación por predicción y retorno aleatorio en una capa (C), asociación
por parecido (B, dos mundos), fisión como creadora de rasgos (criba). Errores nuevos: ERR-29 a ERR-35. Regresión de la regla 1
sobre v14.1: `cd organismo && python bateria_v14.py 6 && python bateria_generaliza.py organismo_v14 20 --desde 101`.


### 15.8 La mañana del 18 (07:15 → 08:30): XOR cerrada, mundo vivo, alias de código

**15.8.1 Decisiones del director.** Tres decisiones ya tomadas enmarcan la mañana (`PLAN.md`, `REGISTRO_etapas_1_2.md`):
04:55 "sí a todo" → v14 congelado; 06:05 "sí, mételas" → **v14.1** congelado (`eta_s` 0.15, `clip_s` 10); 07:10, **ERR-35**
— el criterio de parada de XOR se reformula después de ver datos: la línea se cierra declarando el MÍNIMO de ejemplos con
el que el organismo generaliza, no como fracaso ("es esperar que mi hijo haga pan solo con haberme visto dos veces"). El
bloque 3/3 corre igual, con el mejor mecanismo de la sala de agentes que pase la criba (proponer `P0·P1` en ≥ 15/20) y
`ntr = 14` como control obligatorio.

**15.8.2 Bloques de la mañana**

| bloque | nivel | veredicto | números clave | datos |
|---|---|---|---|---|
| 07:10–07:43 sala de agentes (enjambre, 4 mecanismos) | 3 (XOR) | M3 y M4 sobreviven; M1 y M2 refutados | M3 mediana 0.8125 (estricta 0.625), n\*=7; M1 0.500; M2 0.313 | `ENJAMBRE_xor_20260918.md` |
| 07:43 bloque 3/3 XOR (M3, memoria de un golpe) | 3 | ✅ CRUZA — prior estructural | 1.000 registro y estricta, (0,1) 20/20, n\*=7 | `xor_7_s121-140_20260918_073918` |
| 07:47 línea XOR, réplica 141–160 | 3 | ✅ REPLICA — LÍNEA CERRADA | 1.000/1.000, n\*=10, X1–X6 OK | `xor_7_s141-160_20260918_074208` |
| 07:58 mundo vivo, primer bloque (181–200) | 8/9 | núcleo sostenido; P4′/P6/P7 no como se escribieron | xor01 1.0 (20/20) contra 0.5; tabla 2×4 en ~11 exp.; muertes 97 contra 135.5/152.5 | `vivo_s181-200_20260918_075215` |
| 08:06 candidato v15c (memoria de pares en el TRONCO) | 3 | ❌ NO ENTRA — V1 medida apagada; su G1 0.500 era ERR-38 (corregida: 1.000); superado por v15d | mundo de regla 0.812 estricta | `v15c_s121-140_20260918_075817`, `regresion_generaliza_organismo_v15c_on_20260918_084524` |
| 08:38 candidato v15d (suma/ruta; V2a corregida 08:46) | 3 | ❌ NO ENTRA — el examen cae por REVERSIÓN (E2 0/20) y la vía rápida no consolida (E1 0/20) | V2a G1 1.000 / G2 0.999; V2b xor01 0.875 estricta, px0 1.000, azar 0.500; celdas −18 % | `v15d_s121-140_20260918_082846`, `regresion_generaliza_organismo_v15d_on_20260918_084412` |
| 08:44 ERR-38 (batería de generalización copiada sin `eta_s`/`clip_s`: vía lenta apagada en V2a) | instr. | G1/G2 de v15c y v15d ANULADOS; repetidos con la batería corregida: 1.000 los dos | 6/40 filas idénticas al 16.º decimal delataron el error | `regresion_generaliza_organismo_v15d_on_20260918_083404` (anulado) |
| 09:07 B-5 desambiguar códigos (creador B; ALIAS 326–670) | 4 | 8/9 criterios; tronco IDÉNTICO a v14.1 (examen 8/8, generalización 40/40); C4 7/9 → réplica (regla 12) | D1-ALIAS abs W[sal] 0.0, veneno −3.0, exposiciones 517 contra 545, muertes 41 contra 75; tabla 2×2 exacta 9/9 | `codigo_alias9_20260918_085958` |
| 09:12 B-5 réplica (ALIAS 779–944, LIMPIAS 703–764, estructurales) | 4 | ✅ PASA — DECLARADO: "cuando una celda con valor recibe nada bajo una retina distinta, divide"; C4 4/9 (criterio de causa mal escrito) | 0.0 / −3.0 / 475 contra 522 / 41 contra 77; candidato a v15 (decide el director) | `codigo_replica_alias9_20260918_091133` |
| 09:16 propósito y reproducción como medida (diseñador; 221–240) | 9 | ❌ LA MEDIDA SE TIRA (P-R1): ESCALAR/BARAJA_CON hacen más ventanas muriendo 1.5× más; la tercera necesidad SOBRA frente a CUELLO_MIN (Occam); ERR-39 (control de paja) | VIVO 20 desc / 100 muertes; ESCALAR 36 / 149.5; REP_SIN_COSTE 55 / 75; CUELLO_MIN 65.5 / 76; sal saciado 0.80 → 0.007 | `vivo_rep_s221-240_20260918_091428` |
| 09:37 candidato v15e (tabla reescribible, cada vía con su error; kwargs del tronco en V2b) | 3 | ❌ NO ENTRA — se DESDICE (E2 20/20) y consolida (E1 W_B 20/20), generaliza (G1 1.000), pero pierde XOR (0.500 contra 0.438) | V1 6/8 (E1, E2I 19/20); ERR-43 runner; siguiente v15f | `v15e_s141-160_20260918_092921`, `examen_v15e_20260918_093053` |
| 09:45 revisor de literatura (búsqueda web, citas por ficha de editor) | — | ningún mecanismo nuevo: alias = colisión LSH + Rescorla; reparación = distinción útil / ARTMAP; XOR-8 = Mitchell 1980 + unique cue; un golpe = control episódico sobre BTSP (en parte); valor por necesidad = RL homeostático | publicable: nota técnica del alias + benchmark de método; errata Milstein 2024 → Wu & Maass 2025 | `LITERATURA_novedad_20260918.md` |
| 09:43 reproducción bloque 2 (r = descendientes − muertes; CUELLO_MIN; 261–280) | 9 | ✅ 8/8 — la medida ordena como la supervivencia; CUELLO_MIN r +3 (11/20 ≥ 0) contra VIVO −73; tercera fila retirada (Occam) | ERR-40 resuelto; sal saciado 0.78 → 0.001 | `vivo_rep2_s261-280_20260918_094126` |
| 09:45 reproducción bloque 2, réplica 281–300 | 9 | ✅ 8/8 — DECLARADO: la lectura pesimista saciado lleva el linaje al filo del reemplazo; ninguna necesidad nueva hace falta | CUELLO_MIN r −3 (9/20 ≥ 0) contra VIVO −75; A₁₂ 0.965 | `vivo_rep2_s281-300_20260918_094323` |
| 10:00 candidato v15f (R crudo + sobrescritura + relevo; cada vía con su error) | 3 | ❌ por v1 (E1 "Q4 < Q1" 17/20, E2I W_C 17/20, splits +16 %) — pero GENERALIZA (1.000), SE DESDICE (E2 20/20), CONSOLIDA (20/20) y CRUZA XOR con 8 ejemplos en el tronco (1.000 contra 0.500) → primer candidato para el criterio v2 | ERR-44 (subcriterio presupone aprendizaje gradual) | `v15f_s161-180_20260918_095309`, `examen_v15f_20260918_095443` |
| 08:10 ERR-37 y alias de código | 4 | hallazgo confirmado, no superstición | 2/20 semillas con `code(sal)∩code(veneno)`=3; mismo valor en veneno y sal | `PREREGISTRO_supersticion_sal.md` |
| 08:20 mundo vivo, réplica 201–220 (enmienda 2) | 8/9 | ✅ REPLICA; P10 confirma el alias | P4″/P7′/P6′ pasan en las dos series; P10 `err_peor` 0.00 en 20/20 | `vivo_s201-220_20260918_080619` |
| 08:16 bloque de la sal (9 ALIAS/9 LIMPIAS, 301–700) | 4 | ✅ CONFIRMADO — alias de código; S-5 refuta la hipótesis del coordinador (persiste sin sed); S-6 la puerta de v13 no repara | abs W[sal] 1.45 contra 0.0; veneno −1.45 contra −3.0; evitación ×7; sin sed 1.62; con puerta 1.48 | `sal_alias9_20260918_081346` |

**15.8.3 La sala de agentes.** Workflow "enjambre": 5 investigadores de literatura 2019–2026, un jefe que eligió 4
mecanismos (compartimentos M1, fisión estructural M2, memoria de un golpe M3 —BTSP 2017/Milstein 2024—, tabla
meta-aprendida M4), 4 mini-equipos con identidad y mini-prueba (3 semillas, 1 proceso, sin `Pool`: no son series
confirmatorias), 2 refutadores por paquete y un sintetizador; coste ≈ 3.45 M tokens de agentes en 19 agentes (dato del coordinador, del resultado del Workflow; no consta en el informe).
**Qué cazaron los refutadores:** M1 REFUTADO — `cel_ganadora` se captura al FINAL de T, no en la sonda (`cg_ok=False`
en 6/9 filas: el enrutamiento "3/3" medido donde importa es 2/3) y hay asimetría de mordidas 80/20 sin medir. M2
REFUTADO — el piso `_FE=1e9` castiga a las hijas recién nacidas justo en la sonda y `fis_umbral=3` se fijó mirando la
métrica de su propia refutación (sin ERR numerado). M3 NO refutado — 18/18 filas reproducidas exactas, ganador medido
EN LA SONDA (el agujero que hundió a M1). M4 sin votos de refutación (llegaron truncados); el sintetizador verificó lo
esencial: reproduce exacto, el top-10 comparte `rho = 0.02`. **Hallazgo propio del sintetizador:** el desempate por
índice favorece (0,1) en empates exactos — sin corregirlo, la semilla insignia de M3 daría 0.375 en vez de 1.000; sobre
20 semillas, empate en 1/20; con desempate al azar la mediana sigue en 1.000 pero ≥0.75 baja de 20/20 a 19/20.

**15.8.4 Cierre de XOR.** Instrumento `organismo_g3A` (por anclas desde `organismo_g3` de la sala; perillas
`mem_apriori`, `mem_desempate='azar'`; identidad 10/10 + 3/3). Mecanismo: 15 celdas de dos canales, una por par de
píxeles, 4 casillas de valor; la primera mordida de una combinación escribe R **de un golpe**; cada celda lleva su
error propio (EMA); la vía lenta lee sólo la celda de menor error; abstención en combinaciones nunca vistas.

| n ejemplos de entrenamiento | acc_lenta (nunca vistos) | n\* (≥ 0.75) | mecanismo |
|---|---|---|---|
| 8, sin prior (REF) | 0.500 | > 600 | regla local con competencia — nadie selecciona el rasgo (9/15 hipótesis empatan) |
| 8, con prior de pares (M3) | **1.000** (estricta 1.000) | **7–10** | memoria de un golpe por combinación — prior estructural |
| 11, sin prior (NTR11) | 0.625 | 300 | regla local con competencia |
| 14, sin prior (NTR14 / A-6) | 1.000 | 200 | regla local con competencia — ya no hace falta prior |
| 14, con prior (M3_NTR14) | 1.000 | 7 | memoria de un golpe — prior redundante |

Declaración de cierre (07:47, letra de ERR-35): **PRIOR ESTRUCTURAL, no "aprende XOR"** — guarda el valor de cada
combinación la primera vez que la muerde y responde con el par que menos se equivoca; los nunca vistos se aciertan
porque comparten la combinación con los vistos. Vocabulario permitido: *"con 8 ejemplos XOR exige un prior de pares, y
con él bastan 7–10 exposiciones; con 14 ejemplos no hace falta prior"*. Prohibido: "aprende XOR", "entiende la
combinación".

**15.8.5 El mundo vivo.** Núcleo: dos necesidades (hambre, sed) con dos muertes, cuatro estímulos (los cuatro patrones
ya existentes), consecuencia vectorial, sorpresa específica por necesidad, valor por estímulo y por necesidad. Primer
bloque (181–200): `xor01` necesidad × estímulo, VIVO 1.0 (20/20) contra 0.5 de UNA_NEC, ESCALAR y BARAJA_CON; tabla
2×4 exacta en ~11 exposiciones; muertes 97 [53.5 energía, 48 agua] contra 135.5 (UNA_NEC) y 152.5 (ESCALAR).
Supervivencia con ERR-37: P4′, P7 y P6 fallaron por el umbral (pareado en la mediana del propio efecto, que parte la
muestra por construcción; muertes no pareables por semilla; `max` sobre 40 lecturas), no por el efecto (A₁₂
0.90/0.935/0.955; q75 VIVO 106 < q25 125/143); enmienda 2 (P4″, P7′, P6′, P10) escrita antes de 201–220. **Alias de
código:** las dos únicas semillas con valor en la sal (182, 188) son exactamente las dos con el mismo código de Kenyon
(`code(sal) ∩ code(veneno)` = 3 píxeles); `W_hambre[veneno] = W_hambre[sal]` en las dos (−1.83 y −1.34); la puerta
presta la evidencia por código, la división por conflicto no repara (exige `R ≠ 0`, la sal da `R = 0`), la evitación
cierra el bucle. Réplica 201–220: P4″/P7′/P6′ pasan en las dos series y **P10** —sin ninguna semilla con alias,
`err_peor` debía ser 0.00 en 20/20— **PASA**: confirma el alias por predicción, no sólo por ajuste. Nivel 9 → **30 %**
(allostasis mínima medida); nivel 8 recibe el primer mundo con más de una dimensión de valor (sigue en 40 %); nivel 4
recibe el negativo del alias (sigue en 60 %, cabo nuevo); nivel 3 no se toca (se resuelve indexando la memoria, no
leyendo mejor los píxeles).

**15.8.6 Lo que no entró y lo pendiente.** **v15c** (08:06, memoria de pares en la vía lenta del TRONCO) **NO ENTRA**, pero
no por lo que se escribió a las 08:06: **ERR-38** (08:44) — la batería de generalización copiada omitió `eta_s`/`clip_s` y la vía
lenta corrió apagada; repetida: G1 1.000 (v15c y v15d). Su V1 se midió con la perilla apagada; superado por **v15d** (08:38, V2a
corregida 08:46): conserva la generalización lineal (G1 1.000 / G2 0.999) y cruza XOR con 8 ejemplos en el mundo de regla (0.875
estricta), pero **el examen encendido cae por REVERSIÓN** (E2 0/20: la tabla de un golpe no se desdice; E1 0/20: la vía rápida no
consolida; celdas −18 %) → *"la memoria de pares generaliza y cruza XOR con 8 ejemplos, pero no se desdice"*; siguiente candidato con
preregistro nuevo: tabla reescribible (v15e, creador A, en diseño desde 08:50); **bloque de la sal CERRADO** (08:16: alias confirmado 9/9 contra 9/9; S-5 refutó la hipótesis del
coordinador — persiste sin sed: es el código, no la necesidad; S-6: la puerta de v13 no lo repara; queda *desambiguar códigos*, nivel 4); propósito y reproducción sólo como medida
(`descendientes_viables`, predicción VIVO > UNA_NEC > BARAJA_POL, sin mecanismo — exige población y `Pool`); gemelos —
los instrumentos nuevos de la mañana (`organismo_g3A`, `organismo_vivo`, `organismo_v15c`) corrieron sin gemelo
compilado (numba); el tronco v14.1 sí lo tiene.

**15.8.7 Vamos bien o mal.** Vamos bien: XOR se cerró con dos series independientes y un prior declarado como tal, y
el mundo vivo replicó su núcleo y confirmó el alias de código con una predicción que podía fallar limpio (P10) y no
falló. Vamos mal: ningún candidato de la mañana entra al tronco, el cuello que más importa a la misión (construir el
rasgo desde píxeles, sin prior) sigue sin mecanismo, y el alias de código queda confirmado pero sin reparación (nivel 4).


### 15.9 Cambio de rumbo (18 sep 09:55)

**DECISIÓN DEL DIRECTOR (18 sep 2026, 09:55) — CAMBIO DE RUMBO.** Tras la mañana (cinco bloques preregistrados por hora, dos
resultados declarados, ningún candidato de capacidad al tronco; revisor de literatura: ningún mecanismo nuevo), el coordinador
diagnosticó cuatro cosas mal planteadas y el director decidió: *"Perfecto, hagamos esa modificación y registra todo"*.
Lo que cambia, y lo que no:
1. **Se conserva el método** (preregistro → commit → correr → registrar; ERR numerados; réplica antes de cerrar; regla 12; reglas 1–14 de
   EQUIPO). Es lo que nos salvó cinco veces hoy (ERR-38, 41, 42, 43; la medida de reproducción).
2. **El mundo cambia por uno que obligue a representar:** estímulos compuestos (una "sal" y una "sal rosa": la variante como variable
   del mismo token), más píxeles que 6, recursos que se agotan, veneno que cambia — un mundo donde 16 patrones no basten y donde
   la tokenización, la variable y el desaprender sean necesarios para sobrevivir (ERR-35: el mundo de 16 patrones no contiene la
   información para elegir XOR; no se le vuelve a preguntar lo que no puede responder).
3. **La estructura crece por reglas locales:** el organismo recluta y divide celdas cuando la sorpresa se repite en la misma
   combinación (conjunción por coactividad) y cuando un código con valor recibe otra consecuencia (B-5); ninguna capacidad nueva
   entra como perilla diseñada a mano si puede entrar como crecimiento.
4. **El criterio de tronco cambia:** el examen v3′ 8/8 deja de ser la puerta absoluta (selecciona "no cambies nada": v15d/v15e
   murieron por detalles internos; sólo entró lo inerte). Un candidato nuevo se juzga por **sobrevivir y generalizar en el mundo
   vivo** (muertes, r = descendientes − muertes, nunca vistos, reversión: se desdice, sin alias) con **no regresión CONDUCTUAL** del
   examen (la conducta de cada escenario se conserva; los pesos internos no son puertas). El criterio v2 se escribe en
   `registro/CRITERIO_TRONCO_v2.md` ANTES de juzgar a ningún candidato con él; **v15c/v15d/v15e no se rejuzgan** (regla: no
   recalibrar después de ver datos); v14.1 sigue siendo el tronco hasta que un candidato cruce el criterio v2 en semillas nuevas.
5. **Ejecución:** la SALA 2 (4 diagnósticos, 6 diseños, 12 refutadores, síntesis) entrega el diseño concreto del mundo y del
   crecimiento; de ahí salen los bloques preregistrados, en este orden: (a) `CRITERIO_TRONCO_v2.md`; (b) el mundo que obliga (mundo
   nuevo con v14.1 SIN cambios como control base: si el tronco ya sobrevive ahí, el mundo no obliga); (c) crecimiento estructural
   por sorpresa repetida (crece_codigo) medido en ese mundo; (d) tokens y variables ("sal rosa" cuelga de "sal"; separación cuando
   deja de comportarse igual); (e) población con herencia y muerte real (que viva). Una cosa a la vez en el Pool; réplica antes de
   declarar; "llegar a la frontera es lo primero, que viva lo segundo".

Estado al escribir esto: SALA 2 corriendo (síntesis en `registro/investigacion/SALA2_frontera_20260918.md`); v15f (creador A) en
humo; Pool libre. Quien retome: leer primero `registro/CRITERIO_TRONCO_v2.md` (si existe) y la síntesis de la sala; nada de lo
anterior se rejuzga.


### 15.10 Interrupción por límite de sesión (18 sep ~10:10; se reanuda 13:50)

La SALA 2 (workflow `sala2-frontera-juaco`, 23 agentes, 5.8 M tokens) terminó 18/23: los 4 diagnósticos (`registro/investigacion/sala2/DIAG_*.md`),
los 6 diseños (`DISENO_*.md`) y 2 de 12 refutaciones escritas (`REFUTACION_dos_escalas_medibilidad.md`, `REFUTACION_vivir_localidad.md`;
las demás refutaciones devolvieron sólo su veredicto estructurado, ver `journal.jsonl` del workflow) más sus scripts y JSON de apoyo.
**La SÍNTESIS (`SALA2_frontera_20260918.md`) NO se escribió**: cayó por el límite de sesión, igual que 4 refutadores. El creador A murió
al empezar el paquete de v15f para el criterio v2: sus 5 archivos en `experimentos/creacion_A/*vivo_relevo*`, `PREREGISTRO_v15f_v2.md`,
`corre_v15f_v2.py` están SIN VERIFICAR (sin identidad, sin humo): se guardan como borrador, no como instrumento. Todo lo anterior a las
10:00 está registrado y empujado (5a00089). **Al reanudar:** (1) leer los 4 DIAG y los 6 DISENO y escribir la síntesis (un agente,
o el coordinador) → completar `CRITERIO_TRONCO_v2.md`; (2) reanudar al creador A sobre su borrador (identidad primero); (3) el Pool
está libre; nada corre.


### 15.11 Cierre de la noche del 18 (21:30)
Ver la entrada "CIERRE DEL 18 SEP" al final de `REGISTRO_etapas_1_2.md`. Quien retome: (1) `CLAUDE.md` bloque Estado y la decisión del
director de las 09:55 (cambio de rumbo) y de las ~14:15 (plan aprobado); (2) `registro/CRITERIO_TRONCO_v2.md`; (3) lo pendiente con paquete
verificado: v14.2 (`experimentos/creacion_B/CONGELA_v142.md`, aplicar tras la regla 1), v15f-v2 (`python experimentos/creacion_A/corre_v15f_v2.py`),
dE5 después; (4) la fase 5 pide un candidato con dos ganadoras de tipo distinto (forma + variante); (5) la fase 9 pide que un cuerpo nuevo
aprenda en menos de una vida (nodo leído por relevancia; conexión desde el nacimiento como mecanismo; reproducción desacoplada de la saciedad).
Regla para el coordinador (de esta noche): todo parche propio se compila y pasa el arnés en una semilla antes del Pool; lo que sea instrumento
lo hace un creador con arnés y humo.

### 15.12 Junta de la fase 5 (19-sep-2026, tres creadores Opus con exoesqueleto y nave)
Pedido del director: tres Opus con memoria por consecuencia (bitácora compartida `experimentos/junta_fase5/BITACORA_CONSECUENCIAS.md`),
calibración (rápido / preguntar / razonar) y una "nave" (copias propias, identidad bit a bit obligatoria, humo en 901-910,
confirmación en 821-860 corrida SÓLO por el coordinador). Misión y criterio: `experimentos/junta_fase5/MISION.md` —
una tabla que refiera a familia Y variante a la vez (BAR-T ≤ 5/20 y PAR ≥ 15/20, con las puertas del bloque 6).
- **C (sistemas vivos)** — `C/organismo_familias_c1.py`, identidad 61/61: la casilla **se divide** por conflicto de signo sólo
  donde la distinción de familia falla, hijas con el valor de la madre (fisión). Diagnóstico propio: el techo de b6 fue la
  DILUCIÓN, no la firma. Predicción firmada: BAR-T 4 (2-6) y PAR 15 (13-18); muertes 35 contra 462 de la base. Declaró un
  riesgo propio y lo volvió medible: *"el que aprende mejor el mundo deja de escuchar"* (V1: vacuas P-I5 6/20 contra 1/20 de
  la base; V2: las vacuas tienen menos celdas de Kenyon). Candidato aparte y NO corrido: `C/PREREGISTRO_oreja.md`.
- **B (representación)** — `B/`, identidad 88/88: la lectura de b5/b6 es una DISYUNCIÓN (la unión de las k direcciones; por eso
  una celda alcanzada por azar decide sola y BAR-T sube de 5 a 11). Candidato: lectura **CONJUNTIVA** (`mem_conj=1`): contesta
  sólo si las k celdas conocen su dirección → la referencia pasa a ser la intersección = el referente solo. Predicción firmada:
  BAR-T 2/20 (0-5) y PAR 15/20 (13-18). Dos ideas propias refutadas y registradas.
- **A (matemática local)** — propuesta escrita 17:29; midió su propio mecanismo favorito (`combina='min'`, `dentro='min'`) como
  INERTE y lo retiró del candidato por Occam, con la predicción propia declarada refutada en la bitácora.
- **Decisiones del coordinador (mismas para los tres):** P-I5 y la vacuidad se leen como puerta de VALIDEZ, no de calidad: la
  semilla vacua sale del numerador y del denominador de todos los brazos de esa celda, declarada con sus números y con el
  mismo trato para la línea base; nada de cambiar criterios después de ver datos; toda idea nueva entra como candidato aparte
  con preregistro propio. **ERR-85 (nuevo, 17:19): un agente de otro proyecto mató procesos python sin verificar el cmdline y
  tumbó dos corridas; regla nueva: ningún agente mata procesos — sólo el coordinador, y verificando el comando.**
  **ERR-86: Pool(14) con otras corridas en curso → BrokenPipeError en Windows; el tamaño del Pool se fija por `JUACO_POOL`.**
  **ERR-87 (21 sep, coordinador): `lee_json` por `startswith` en los runners v13D/v13E leía el JSON de la ON (o de k5) como referencia;
  ningún veredicto cambia (verificado contra los JSON); corregido con prefijo + sello exacto en los dos. Detalle en el registro.**

### 15.13 Cierre de v15f-v2 (21-sep-2026, 12:37–12:54; serie completa, 1002 s, Pool 10 vía `JUACO_POOL`)
El paquete verificado 33/33 se corrió entero: v15f **NO ENTRA** al tronco bajo el CRITERIO DE TRONCO v2 — cae T-A (sobrevive; A₁₂(r) < 0.50 pareado
en los dos brazos aunque las medianas de muertes y r cumplan), T-C (se desdice; A₁₂(rev) 0.55 contra 0.75 en el mundo vivo; la conducta del examen
sí se desdice 20/20), T-D (sin alias; la puerta de v14.1 lee la vía rápida antes que la tabla en las 9 ALIAS, como predijo el creador A) y T-E
(no regresión conductual; sólo 1 de 6 escenarios conserva la conducta). Pasa T-B (G1 1.0 / G2 0.999), T-F (coste ≤ 1.02×) y T-G (xor01 estricta
1.000 ON contra 0.531 OFF). El brazo exploratorio `v15g` cruza C1/C2 de T-D pero cae igual en T-C(ii). El tronco sigue siendo v14.2; nada se
rejuzga; sin ERR nuevos. Patrón: v15d, v15e y v15f caen los tres por reversión o conducta del examen → recomendación del coordinador: cerrar la
línea de memoria de pares en la vía lenta (decisión del director). Mismo día: ERR-87, `registro/ESTADO.md`, `experimentos/INDICE.md`, agentes y
skills fijos del equipo (EQUIPO.md, "Herramientas"), candidato B+A de la fase 5 en diseño por `juaco-creador`.
**15.14 (21-sep 15:45): ERR-88** (`dentro` de A1 es código muerto; "inerte" era "no conectada"; ningún veredicto cambia) y **candidato BA lanzado**
(conjunción de B por tipo sobre las dos ganadoras de A; identidad 56/56; el propio creador refuta en su humo la mitad de variante y baja su apuesta a
≈10–15 %; se corre igual en 921–940 con celdas b5k3,b6suf,A1,BA,BA-v; réplica 941–960 sólo si algo pasa).
**15.15 (21-sep 13:09–13:51): confirmación del candidato BA.** Serie 921–940 (`13f3bdb70928e9f5`) y réplica automática por regla 12 en 941–960
(`4dcdffb3d724154d`), Pool 8. `BA-v` (la variante incompleta sí vota) cumple la MISIÓN cruda (BAR-T ≤ 5 y PAR ≥ 15) en las dos series pero no cruza
la letra R1–R5 en ninguna (cae R4 en la primera, R2+R3 en la réplica); `BA` cumple la misión cruda ×2 pero cae BAR-H (14/15, la variante, como
predijo su creador) y VALOR (8/6). `A1` pasa R1–R5 en 3 de las 4 series medidas hasta hoy y la misión cruda en 1 de 4. **ERR-89:** R6 (coste) queda
INCOMPLETO — el runner no la juzga y la celda base `b4b` no se corrió; dato exploratorio: `BA-v` muere 104 en la réplica contra 37–50 del resto.
Nada entra; nivel 5 sigue en 75 %. Decisión del director: preregistrar `BA-v` con criterio propio y `b4b` en la serie, o cerrar la línea BA/BA-v.

### Cierre del 21-sep-2026 (16:15)
Corrido y registrado hoy: v15f-v2 (NO ENTRA, 4 puertas de 7), BA serie + réplica (misión cruda ×2, letra no, R6 incompleto). ERR-87, ERR-88, ERR-89.
Organización: `registro/ESTADO.md` (página viva), `experimentos/INDICE.md`, agentes y skills fijos (EQUIPO.md "Herramientas"), humos huérfanos en
`datos/humo_no_registrado/`. Decisiones tomadas por el coordinador y documentadas: correr v15f-v2 (decisión previa del director del 18-sep), correr BA
en 921–940 por la colisión de semillas, réplica por regla 12. **Decisiones pendientes del director:** (1) cerrar la línea de memoria de pares en la
vía lenta (v15d/v15e/v15f) o preregistrar v15g; (2) BA-v con criterio propio y `b4b`, o cerrar BA; (3) abrir la fase 9 ahora o esperar. Quien
retome: `registro/ESTADO.md` primero, luego esta sección, luego las tres últimas entradas del registro.
**15.16 (21-sep 16:30): CIERRE de la línea de memoria de pares en la vía lenta.** Decisión del director, delegada al coordinador con su
recomendación. Cinco candidatos y un brazo exploratorio en tres mecanismos (v15c sustituye la lineal, medido inválido por ERR-38; v15d
suma/enruta, cae por reversión E2 0/20; v15e reescribe el residuo, se desdice 20/20 pero pierde XOR 0.500; v15f con R crudo y relevo,
cruza XOR 1.000 bajo v1 pero bajo v2 cae T-A, T-C, T-D y T-E; v15g invierte el orden de las puertas y cruza el alias pero cae T-C igual)
no entran al tronco. Ninguno se rejuzga; v14.2 sigue de tronco. Sigue disponible: XOR como prior estructural declarado (`xor_7`) y `v15g`
como reapertura posible SOLO con preregistro propio y siete puertas. Entrada "LÍNEA CERRADA: memoria de pares en la vía lenta" en el registro.
**15.17 (21-sep 14:50–15:13): serie de `BA-v` bajo ERR-90 (puertas absolutas), 961–980 (`198f08856aeaf607`), Pool 8.** `BA-v` pasa P0–P5 y P7
(R6 completo con base `b4b` por primera vez: muertes 1.4643× ≤ 1.50, okU igual; la única de las seis celdas que lo pasa entero; `b5k3`/`b6suf`/`A1`
caen okU por la cuantización de 1/6 predicha), pero cae P6 (dist(PAR) 13/19 < 15, margen de 2 semillas) y por eso la misión cruda de esta serie.
Control barajado `BA-v-sh` funciona (CANAL 2/19, dist 0/19). Predicción del creador "ninguna celda k=3 pasa R6" refutada. BA-v acumula misión
cruda 2/3 series y letra absoluta 0/1. Decisión del coordinador (delegada): la réplica 981–1000 se corre después de dE5-v2; si cae P6 otra vez,
BA-v se cierra. Nivel 5 sigue en 75 %. Commits `20d9656` (paquete), `e02b139` (crudo).
**15.18 (21-sep 15:14–15:22): Fase 9, bloque 1 "cuerpo nuevo", serie 1501–1520.** Instrumento por anclas sobre v14.1 (`organismo_f9.py`, 11 anclas
desde `organismo_alma2`; identidad 99/99 en el arnés, inline OK en la corrida). El ancla F9-1 reproduce NADA_CM y RENACE_CM de H-1: el instrumento no
se movió. Por la letra, 8 de 10 puertas pasan y 2 caen (F9-4, F9-7); ninguna caída está a una semilla del umbral. La pregunta central (F9-3, "menos
de una vida") pasa con efecto grande: el recién nacido que lee el nodo por relevancia rechaza el veneno en su primer encuentro (p1 0.962 contra
0.194) sin dejar de comer. F9-4 cae por mitad: el nodo barajado también alarga algo la vida pero produce cautela genérica que hunde c1 a 0.598
(la trampa 2 del preregistro en el control, no en el candidato), así que la frase completa del preregistro sigue sin desbloquearse. F9-7 refuta la
predicción del creador: conectarse tarde no cuesta (A₁₂ 0.426). F9-8: la reproducción desacoplada sube R₀ sin reordenar y NINGÚN brazo cruza
H1-6: H-1 y ERR-62 siguen en pie. Nivel 9 sigue en 30 % hasta la réplica 1521–1540 (en cola tras dE5-v2 y la réplica de BA-v). Datos
`f9_cuerpo_nuevo_s1501-1520_20260921_151405` (veredicto `fadb7bcee33d7f54`); commits `e38c841`, `893dd3a`.
**15.19 (21-sep 15:22–15:37): cierre de dE5 bajo el CRITERIO DE TRONCO v2, semillas 2001–2080.** Paquete 68/68 corrido entero: dE5 **NO ENTRA** — cae
T-A (A₁₂(r) 0.4 en VIVO aunque muertes y r cumplan), T-C (ii: A₁₂(rev) 0.5, revierte menos, no más), T-E (los seis escenarios, siempre mordiendo más
veneno que el tronco) y T-G (recupera 3.23× más rápido con pareado 20/20 y apagado 20/20, y el control `CONST` sin información recupera más lento que
el apagado, razón 1.281×; pero el veneno tras el cambio sube 1.128× sobre 1.10 y esa cláusula tumba la puerta). Pasa T-B, T-C (i), T-D (B-5 repara
el alias con la dosis encendida) y T-F. El creador firmó ~40 % y avisó en el humo que T-A iba peor; se confirmó. Comparado con v15f-v2, dE5 invierte
T-D y T-G; los dos caen T-A y T-C (ii) con A₁₂ 0.4–0.55, indistinguibles del tronco en el mundo vivo pareado: observación transversal para el
director, sin recalibrar. Tronco v14.2; dE5 queda como órgano medido con coste, no candidato. Sin ERR nuevos. Commits `9ac631c`, `2a35577`.
**15.20 (21-sep 15:58–16:06): réplica de la fase 9, bloque 1, semillas 1521–1540 (Pool 8).** El ancla bloqueante F9-1 **CAE**: tres cláusulas en rango
(R₀ NADA 0.13, R₀ RENACE 1.0, r RENACE 1.0) pero la vida mediana de NADA sale a 88.5, 1.5 por debajo del límite inferior 90. Por la letra, la
réplica **no confirma** el bloque 1: nada se declara. Exploratorio: las mismas siete puertas vuelven a pasar y las mismas dos vuelven a caer con cifras
casi idénticas (REL vida 598.5 → 589.0, p1 0.962 → 0.966; REL_BAR p1 0.568 en las dos). El rango [90, 170] se calibró con dos series de H-1 (125/119)
y hoy hay cuatro (125, 119, 94.0, 88.5): candidato a ERR de rango de ancla. Nivel 9 sigue en 30 %. Datos `f9_cuerpo_nuevo_s1521-1540_20260921_155801`
(veredicto `db58916c2b15b57b`); commit `a743704`.
**15.21 (21-sep 18:20–19:05): junta de tres creadores y dos ERR de criterio.** Voto unánime: el criterio v2 rechaza al propio tronco (placebo pasa T-A
0.316, T-A y T-C ii juntas 0.006) → **ERR-91**, CRITERIO_TRONCO_v3 con placebo en construcción (creador A), sólo para candidatos futuros. **ERR-92:** el
rango del ancla F9-1 se calibró con dos series y hoy hay cuatro → enmienda (rango [70, 170], `F9_VIDA_NADA_MIN`), tercera serie 1621–1640 con
predicción escrita. Síntesis y decisiones en `experimentos/junta_20260921/SINTESIS.md`. Regla 15 de EQUIPO. En construcción para mañana: gemelo numba
de la fase 9 (compilador) y el informe de necesidades reales donde vender el sistema (`registro/investigacion/NECESIDADES_20260921.md`).
**15.22 (21-sep 16:06–16:24): tercera serie de `BA-v` bajo ERR-90, 2101–2120 — CIERRE de la línea BA/BA-v.** N = 16 (cuatro emisores sin mensaje), así
que P0 cae para las seis celdas. `BA-v` cae además P3 (BAR-T 6) y P6 (dist(PAR) 11/16, margen de 4 semillas contra 2 y 1 antes); pasa P1, P2, P4, P5 y R6
(1.40×). Tres series ERR-90, tres caídas de P6 (13/19, 14/18, 11/16): patrón, no ruido (bajo el modelo de tasa única de A, fallar las tres ≈ 0.5 %);
la explicación estructural de B (una de tres ganadoras de variante comparte casilla con la hermana, 37/37) cierra la cuenta. La dirección del mensaje es
exacta (1/32, hermana fuera del grupo); lo que falla es el valor. Nada se rejuzga; `BA-vm` (B) y `V-5` (C) quedan preregistrados sin correr. Nivel 5
sigue en 75 %. Entrada "LÍNEA CERRADA: BA / BA-v (fase 5)" en el registro. Commit `84e5247`.
**15.23 (21-sep 16:24–16:32): tercera serie de la fase 9, bloque 1, bajo la ENMIENDA 1 (ERR-92), 1621–1640, Pool 8 — DECLARACIÓN.** El ancla F9-1
**PASA** (vida NADA 95.5), incluso bajo la letra original [90, 170]: la enmienda no fue necesaria esta vez, pero fue la corrección correcta. Con dos series
válidas por la letra (1501–1520 y 1621–1640) que repiten las mismas ocho puertas positivas y las mismas dos negativas número a número, el coordinador
**declara** el núcleo del bloque 1 (el recién nacido rechaza lo malo al primer encuentro sin dejar de comer; vida ~6.3–6.4× el cuerpo vacío; relevancia >
recencia y > azar; el ranking congelado evita pero deja de comer y el vivo no; la reproducción desacoplada sube R₀ sin reordenar; H-1 sigue en pie) y
**deja sin declarar** F9-4 (cautela genérica del nodo barajado, cae ×3) y F9-7 (conectarse tarde no cuesta, negativo ×3, el contraste interno empeora
9 → 10 → 5/20). Predicciones de la enmienda: siete de ocho acertadas; la banda de A₁₂(REL > REL_TARDE) [0.35, 0.55] quedó corta (0.626), parcialmente
refutada con el coordinador como autor. **Propuesta: nivel 9 de 30 a 40 %** (decide el director). Bloque 2 en construcción (F9-4bis con J y CAUTELA,
C-F9B′, ORÁCULO; `nivel09_cuerpo_nuevo_b2/`); gemelo numba en construcción. Datos `f9_cuerpo_nuevo_s1621-1640_20260921_162410` (`c908a720d3de3fb9`); `8888b9b`.

### Cierre del 21-sep-2026 (20:15, ventana de dos horas del director "dale candela")
**Corrido y registrado hoy (11 series, un Pool a la vez):** v15f-v2 (NO ENTRA) · BA 921–940 + 941–960 · BA-v 961–980 + 981–1000 + 2101–2120 (línea
BA/BA-v CERRADA) · fase 9 bloque 1: 1501–1520, 1521–1540 (exploratoria, ancla caída), 1621–1640 (ERR-92) → **DECLARADO en parte** · dE5-v2 (NO ENTRA).
**Líneas cerradas hoy:** memoria de pares en la vía lenta (v15c–v15g); BA/BA-v (fase 5). **Declarado hoy:** el cuerpo nuevo que lee el nodo por
relevancia viva rechaza lo malo al primer encuentro sin dejar de comer y vive ~6.3× (dos series válidas). **ERR-87..92** (dos de instrumento, uno de
código muerto, uno de puerta sin juez, dos de criterio: el v2 rechaza al propio tronco; el rango del ancla). **Junta** de tres creadores (SINTESIS.md):
voto unánime en el criterio. **Organización:** ESTADO.md, INDICE.md, agentes y skills fijos, regla 15. **Necesidades:** NECESIDADES_20260921.md (una
sola: la invalidación de lecciones por consecuencia; ranking daño repetido > lección que muere > deriva).
**Decisiones del director tomadas hoy (delegadas, "llena las 3"):** cerrar v15; BA-v como candidato aparte → cerrado tras tres series; fase 9 abierta.
**Decisiones pendientes del director:** (1) fijar el nivel 9 (propuesta 40 %); (2) aprobar CRITERIO_TRONCO_v3 con placebo cuando la calibración
CAL-1..CAL-5 pase; (3) autorizar dos Pools en paralelo (ninguna puerta mide tiempo de pared).
**Para mañana, en orden:** (a) calibración del criterio v3 (placebo; paquete en `experimentos/criterio_v3/`); (b) bloque 2 de la fase 9
(`nivel09_cuerpo_nuevo_b2/`: C-F9B′ + F9-4bis con J + CAUTELA + ORÁCULO); (c) gemelo numba de la fase 9 (`organismo_f9_rapido.py`, arnés antes de usarlo
para confirmar); (d) alefast Fase 3 (número contra Mem0) es de su propio repo. Quien retome: `registro/ESTADO.md`, luego esta sección, luego las cinco
últimas entradas del registro. Los paquetes de (a), (b) y (c) llegaron o llegan al cierre; se commitean con la nota "verificado" o "borrador" según su arnés.
**15.24 (21-sep 16:56–17:10): calibración del CRITERIO DE TRONCO v3 por placebo, bloque A-CAL, 2121–2200 (Pool 7).** CAL-1..CAL-5 acertadas las cinco: el
placebo (el tronco consumiendo y descartando un sorteo por paso, identidad 54/54) pasa T-A bajo v3 con 0.974 (n = 40) y bajo v2 con 0.285: **ERR-91
confirmado con corridas reales nuevas**; v3 rechaza con 1.000 a un candidato desplazado −20, igual que v2; el brazo PEOR (coste ×1.5) cae T-A con las
dos letras. Punto débil declarado sin recalibrar: T-C (ii) bajo v3 sólo 0.789 a n = 40 (0.548 a n = 20): con sd ≈ 27 y margen 10, ≥ 0.95 pide n ≈ 80 o
margen 15 → candidato a enmienda para el director. Réplica 2281–2360 en marcha; **v3 no se declara utilizable hasta que repita**; nada juzgado bajo v2
se rejuzga. Datos `critv3_20260921_165615` (`c031c9585242d850`); commits `10da31b`, `4ead270`.
**15.25 (21-sep 17:07–17:14): nivel 6, bloque "rodeo obligado", serie 1702–1721 (Pool 6, en paralelo con la calibración v3).** El campo difundido por
relajación local (la tabla M leída como bloqueo) **CAE por la letra en 5 de 10 puertas**: rodea limpio el 35 % (umbral 60), no supera a BARAJADO por el
margen (0.15 contra 0.25: la cláusula de refutación que el propio creador fijó), huye el 42.5 %, J −0.4, pasos 0.781. Pasan comida (2.46×), muertes
(0.38×), el control INVERTIDO y el placebo. Coherente con nivel6_2d: mejora comida y supervivencia sin rodeo fiable. Mundo muralla con geometría sorteada
queda como instrumento; port a v14.2 no escrito. Nivel 6 sigue en 50 %; réplica no se corre. Datos `muralla_s1702-1721_20260921_170652`; `a9fc850`, `0925beb`.
**15.26 (21-sep 17:08–17:20): réplica de la calibración del criterio v3, 2281–2360 (Pool 7) — NO REPITE.** CAL-1 refutada por 0.002 (T-A v3 0.898) y
CAL-4 refutada (muertes_VIVO 0.627 fuera de [0.40, 0.60], el gatillo que declara el instrumento roto); CAL-2, CAL-3 y CAL-5 repiten; en la realización
el placebo cae T-C (ii) bajo v3 (LI −11.93). Por la letra, **v3 no se declara utilizable**: se propone v4 con ERR (T-C ii n = 80 o margen 15; CAL-4 con
n = 80 o placebo que no toque el rng; decisión del director). Lo que se sostiene en dos series: v2 rechaza al propio tronco (0.285 / 0.297) y las dos
letras rechazan al peor por 20. Hasta v4, cualquier candidato se juzga con v2 y v3 lado a lado, declarándolo. Datos `critv3_rep_20260921_170812`
(`fd10cce51f4cdc53`); `b9626d1`.
