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
| **3 generalización** | lineal: Etapa 3 cerrada (v9), recuperada en v13 tras ERR-20 (0.80–0.90 en nunca vistos; `bateria_generaliza` obligatoria) | no lineal (XOR 0.44): bloque 3 (límite de lectura) | 70 % |
| **4 memoria persistente** | retención 20/20 (v11/v13), capacidad ×5 (50/60 v11; 35/60 v13 por la puerta), examen v3' | retención de lo **ausente** bajo interferencia (0.67 a 150k pasos); canje puerta/capacidad; olvido dirigido | 60 % |
| **5 comunicación / transferencia** | N1 experto→novato (replicado); N3d transferencia entre sensores por conducta (replicado); mudo = obedece, crea dependencia | **N2 cerrado con dos mundos** (6 diseños ❌; N2f v3 con montaje válido; INNATO 60 vs 278: el canal serviría con significado dado); que el receptor aprenda algo propio; XOR entre dos | 50 % |
| **6 planificación** | mapa: elige la dirección hacia comida recordada fuera de la vista (replicado; invertido huye); tras el cambio de regla muere menos | horizonte real (dos metas, rodeo), secuencia de acciones, `M` que se degrade; canje exploración/explotación (bloque 2) | 35 % |
| **7 composición** | 3T-k: historia de hasta 4 pasos con distractores (control ≈ 0); techo = pool de celdas | composición de rasgos: **XOR no es límite de dimensión ni de puerta sino de la REGLA de la vía lenta** (3, 3b, trío); 3d pendiente; composición social (XOR entre dos) | 55 % |
| **8 aprendizaje abierto** | sigue aprendiendo hasta el techo de la retina (50 patrones, 0.80); se recupera del cambio de regla (2–4k pasos, 18/20); el mapa cobra exploración | retención de lo ausente (0.67 = interferencia); **canje del mapa: curiosidad por progreso ❌ y novedad de sitio ❌ (dos dosis; lo desplaza, no lo rompe)**; dominio distinto del anillo; olvido/fusión | 40 % |
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
