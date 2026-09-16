# Comunicación y aprendizaje simbiótico — contemplación y diseño (NO es un preregistro)

**16 sep 2026, día 4.** Pedido de dirección: *"cómo hago para que este ser comience a comunicarse a los otros y los
otros puedan aprender de manera simbiótica"*.

Es la Etapa 5 del brief (transmisión), con vistas a la 6 (acumulación) y la 7 (comunicación). Lo que sigue es
pensamiento de diseño; cada nivel se preregistra aparte antes de correr.

---

## 1. Qué significa "comunicarse" aquí (definición operativa, para no engañarnos)

Hay comunicación entre dos organismos sólo si se cumplen **las cinco** condiciones:
1. **Emisor:** un organismo produce una **señal** con su cuerpo.
2. **Canal:** la señal viaja por el mundo, con alcance y posibilidad de pérdida, y **otro** la percibe con un sentido.
3. **Información privada:** la señal está correlacionada con algo que el receptor **no puede percibir por sí
   mismo**.
4. **Efecto:** la conducta o el aprendizaje del receptor **cambian** por la señal.
5. **Beneficio medible:** el receptor gana algo (supervivencia, menos veneno, aprendizaje más rápido).
   - Es **simbiótica** si **los dos** ganan: cada uno es a la vez emisor y receptor, y ninguno vive a costa del otro.

**Lo que NO es comunicación (y la trampa más fácil):** copiar pesos de un organismo a otro. Eso es telepatía, o
herencia horizontal. El día 1 ya se probó ("compartir pesos del mejor") y propagaba ruido. La comunicación exige un
**cuerpo que emite** y un **sentido que recibe**.

## 2. Qué información privada tiene un organismo de JUACO

- **Todos ven lo mismo:** el patrón de 6 píxeles del objeto más cercano.
- **Nadie ve lo que el otro sabe:** el valor aprendido `W` de cada patrón y el **resultado** de lo que acaba de
  morder (comida o veneno).
- Con lo medido hoy, esa información vale mucho. Aprender que B es veneno cuesta **~19 mordidas de veneno**, y
  descubrir que el mundo cambió cuesta **probar lo temido con hambre** (etapas 2 y 4). Un organismo que **ve el asco
  del otro** podría ahorrarse las dos cosas.

## 3. Escalera de cuatro niveles (cada uno falsable, uno por vez)

### N0 — Control ecológico: dos organismos, sin señal
Antes de hablar de comunicación hay que medir **qué cambia por el simple hecho de ser dos**. Compiten por los
objetos, se reparten el mundo y lo **renuevan** mordiendo: hoy se encontró que morder veneno limpia el mundo y sube
la comida disponible (frontera hambre–supervivencia). **Cualquier "beneficio social" que N0 ya produzca no es
comunicación.**

### N1 — Señal innata honesta + aprendizaje vicario (el primer paso real)
- **Emisión:** al morder, el organismo emite una señal de **placer (+) o asco (−)**, según el resultado. Es un reflejo
  del cuerpo, no una decisión, y por eso es **honesta por construcción**.
- **Recepción:** un organismo a distancia ≤ `d` ve **el patrón mordido y la señal**. Actualiza **su propio valor** de
  ese patrón con una regla vicaria, igual a Rescorla-Wagner pero más débil y sin comer:
  `dlt_v = R̂(señal) − W_propio(patrón)`, tasa `η_v < η`, con el mismo drenaje. `R̂` es la escala innata: + → +1 y
  − → −3.
- **Qué la hace comunicación y no telepatía:** la señal sólo dice "bien/mal" del **patrón**. El receptor la mapea a
  **su propio** código Kenyon, que es distinto (sorteado al nacer). Lo que se transmite es la **valoración de un
  estímulo visible**, no los pesos.
- **Biología:** el aprendizaje del miedo por observación (roedores, primates), las llamadas de alarma y el asco
  facial.
- **Simbiosis:** los dos emiten y los dos reciben. Predicción: **cada uno** muerde menos veneno para aprenderlo, y
  la pareja se adapta antes cuando el mundo se invierte, porque basta con que **uno** pruebe lo temido.

### N2 — Señal aprendida: el significado emerge (juego de señalización)
- El emisor tiene `k` símbolos posibles y **aprende** qué símbolo emitir según su propio estado (código y valor). El
  receptor **aprende** qué significa cada símbolo.
- Nadie fija el significado: los dos se refuerzan por la **ganancia compartida** (lo que come y lo que evita el
  receptor).
- **Criterio de emergencia (punto 14 del brief):** el código:
  - no existe en el individuo;
  - aparece al conectar dos;
  - no está programado;
  - es reproducible;
  - y **desaparece al barajar los símbolos**.

### N3 — Simbiosis complementaria: lo que uno solo no puede
- Dos organismos con **sentidos distintos**: uno ve los píxeles 0–2 y otro los 3–5.
- Hoy se midió que **ninguno generaliza una regla no lineal (XOR)**. Una regla que cruza las dos mitades es
  **irresoluble para cada uno por separado**.
- Si al comunicarse **la pareja** la resuelve, la capacidad está **en la conexión**, no en ningún individuo. Es la
  forma más fuerte de emergencia que puede medir este proyecto, y conecta directamente con la frontera XOR de la
  Etapa 3.

## 4. Trampas que hay que cerrar ANTES de correr (punto 15 del brief y lecciones del día 4)

| trampa | control |
|---|---|
| Beneficio por ser dos (competencia, renovación del mundo) | **N0**: pareja sin señal |
| La señal ayuda por su **tasa** (el receptor aprende "algo") y no por su **contenido** | **señal barajada**: mismo número de señales, signo al azar |
| Telepatía disfrazada | el receptor sólo recibe **(patrón visible, signo)**; nunca pesos ni códigos del emisor |
| Un organismo se aprovecha del otro (parasitismo, no simbiosis) | medir el beneficio **de cada uno**, pareado, no sólo el del grupo |
| Criterio que pasa por construcción (ERR-11, 12, 16) | con la señal apagada, el instrumento debe ser **idéntico** a v9 con un solo organismo; verificar que cada control **puede** cambiar algo |
| Línea base mal puesta (ERR-15) | la línea base de N1 es N0, no el organismo solo |

## 5. Primer experimento propuesto: N1

- **Instrumento:** `mundo_social.py`, con N organismos v9 en el mismo anillo compartiendo los objetos, un RNG por
  organismo y el del mundo, y señal con alcance `d`.
  - **Control de identidad:** con N = 1 y la señal apagada, **bit a bit v9**.
- **Condiciones (20 semillas; mundo E1 y mundo E2 con inversión):**
  1. **SOLO:** un organismo.
  2. **PAR-N0:** dos, sin señal.
  3. **PAR-N1:** dos, con señal honesta.
  4. **PAR-BARAJADA:** dos, con el signo de la señal al azar.
- **Métricas por organismo:**
  - mordidas de veneno hasta el criterio de miedo (`W_B ≤ −2.5`);
  - veneno en Q1;
  - muertes;
  - en E2, cuánto tarda en extinguir el miedo a B;
  - **pareado por semilla y por organismo.**
- **Predicciones que escribiría en el preregistro:**
  - **N1 < N0** en veneno hasta el criterio, en **cada** organismo, en ≥ 15/20 (simbiosis: los dos ganan);
  - **BARAJADA ≥ N0** (la señal sin contenido no ayuda, y probablemente estorba);
  - **en E2**, N1 extingue antes que N0, porque basta con que uno pruebe B para que el otro lo sepa.
- **Qué NO se podrá afirmar aunque pase:** que "hablan", que "entienden" o que hay lenguaje. N1 es **transmisión
  social de valor con una señal innata**. El significado emergente es N2.

## 6. Por qué este orden

Etapa 4 muestra, si se sostiene, que **la memoria heredada sólo sirve en un mundo que no cambió**. La comunicación
(N1) es la respuesta natural a ese límite: **transmitir lo que es verdad ahora**, no lo que fue verdad para los
padres. Y N3 es donde un organismo puede dejar de ser el límite de lo que sabe.
