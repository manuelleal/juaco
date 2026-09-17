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

## 11.5 Estado al cierre de la sesión (noche del 17 sep) y cómo retomar N2
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
