# HORIZONTE — cómo sacar a JUACO del juguete y ponerlo en la frontera

**16 sep 2026, día 4. Documento de exploración (pensamiento, no preregistro).** Pedido de dirección: *"cómo lo sacamos
de la frontera… entra en modo exploración"*. Escrito por Claude (Fable 5.1) con la evidencia del registro, sin correr nada.

---

## 0. La idea que ordena todo

El proyecto no sale del juguete subiendo niveles dentro del mismo anillo de 40 casillas. Sale cuando **una afirmación
del organismo muerde sobre algo que existe fuera de la simulación**: un cerebro real, un cuerpo real, o la práctica
real de la ciencia. Hay tres puentes así, y uno es transitable ya.

## 1. Lo que JUACO tiene de verdad (para saber qué se puede exportar)

Afirmaciones **derivadas y medidas**, no meras observaciones:
1. **"Dividir compra separación, no compra rango"** (2K-bis): el límite de capacidad no está en el número de celdas
   sino en el rango dinámico de los canales de valor; el drenaje de la parte común lo levanta.
2. **El arreglo no puede costar conducta, sólo comprarla** (ERR-11 → prueba de coste): `W` es invariante al reparto
   `Wp/Wn` hasta la primera truncación. Es un teorema del modelo, verificado semilla a semilla.
3. **La selección está en el criterio de parada, no en la dirección** (3T): la división es ciega; lo que la vuelve
   inteligente es que el error la apaga.
4. **Explorar con hambre es la única vía para revertir**, y su nivel está en un óptimo medido (frontera hambre–supervivencia).
5. **La generalización vive en el solapamiento de códigos** y **actúa al primer encuentro**; con una regla no lineal
   (XOR) no sólo no generaliza: anti-generaliza.
6. **El olvido no es desgaste: las celdas hijas toman el código viejo** cuando la dirección de división usa una
   media no convergida (Etapa 4 + ERR-17).
7. **Memoria de trabajo de rechazo** como el órgano que faltaba para navegar (v9).

Ninguna de estas es un descubrimiento de frontera en sí. **Su valor es que son afirmaciones exactas sobre una
arquitectura que es, casi literalmente, el cuerpo fungiforme de un insecto.** Ahí está el primer puente.

---

## 2. Puente 1 — LA MOSCA: del organismo mínimo al conectoma real

**Por qué es frontera.** Desde 2024 existe el conectoma completo del cerebro adulto de *Drosophila* (FlyWire), y el
cuerpo fungiforme (cuerpo de Kenyon → neuronas de salida MBON, con compartimentos apetitivos y aversivos modulados por
dopamina) es el circuito de aprendizaje mejor cartografiado del planeta. JUACO **ya es** ese circuito en miniatura:

| JUACO | cuerpo fungiforme |
|---|---|
| retina de 6 píxeles → 30 celdas, top-3 | neuronas de proyección → células de Kenyon, código disperso |
| `Wp`, `Wn` | compartimentos MBON apetitivo / aversivo |
| `dlt = R − W` (Rescorla-Wagner) | error de predicción dopaminérgico |
| drenaje de la parte común | ¿? — **predicción a comprobar** |
| división de celdas (2L) | plasticidad estructural dependiente de experiencia |

**Tres predicciones exportables, hoy:**
- **Memorias en conflicto (BUG-01).** Si un olor se aparea con recompensa y castigo alternados, las dos trazas
  saturan y la conducta colapsa a indiferencia; con drenaje, quedan en un equilibrio con proporción derivable.
  Comprobable con imagen de calcio en MBON tras entrenamiento contradictorio. La literatura de memorias coexistentes
  en mosca existe; la pregunta del **rango dinámico** como límite, no.
- **Olvido por neurogénesis (Etapa 4).** En mamíferos, la neurogénesis adulta del hipocampo **causa** olvido (Frankland
  y Josselyn, 2014). JUACO ofrece el micromecanismo: las células nuevas nacen con sintonía casi copiada y capturan
  códigos viejos; predice que el olvido crece con las células reclutadas durante la ausencia (r = +0.87 medido) y que
  **normalizar la dirección de nacimiento lo reduce a la mitad**. Es una hipótesis mecanicista concreta para un
  fenómeno real.
- **Herencia de valor por identidad de código (4c).** Un estímulo nuevo con el código de uno temido hereda su valor
  sin experiencia. Predice gradientes de generalización en función del solapamiento de células de Kenyon, medible.

**El movimiento concreto.** Sustituir la proyección aleatoria `KW` de JUACO por el cableado real PN→KC de FlyWire
(o el modelo restringido por conectoma de Jiang y Litwin-Kumar) y preguntar **qué necesidades de JUACO sobreviven
al cableado real** y cuáles eran artefactos de un sorteo uniforme. Eso es un artículo de neurociencia computacional
con toda la honradez que ya tenemos.

**Qué hace falta.** Un colaborador de neurociencia (UIS, Universidad de los Andes, o cualquier grupo de mosca en
Latinoamérica), las herramientas de FlyWire (`navis`, Codex) y 4–8 semanas. **Riesgo:** no somos neurocientíficos;
sin colaborador es un ejercicio, no ciencia.

## 3. Puente 2 — LA CIENCIA CON AGENTES: el protocolo es el resultado

**Por qué es frontera.** En 2026 la pregunta abierta no es si un agente puede correr experimentos, sino **si se puede
confiar en lo que reporta**. Este repo contiene, sin buscarlo, un caso de estudio completo:
- un protocolo (reglas 1–11, regla de cruce, preregistro con predicción numérica y criterio de refutación, hashes
  de todo, réplica en semillas nuevas);
- **17 errores de instrumento** atrapados y clasificados en familias (medición, criterio que no mide lo que dice,
  línea base mal puesta, control que no puede fallar, comparador de texto);
- **una fabricación real** de otro agente (Antigravity), auditada línea a línea, con la cronología del cambio de
  parámetro a la vista del resultado;
- un director humano que **no** programa y aun así gobierna: exige controles (la prueba de coste), fija
  interruptores (λ_c), decide congelaciones.

**El artefacto.** Un artículo de método + el repositorio como *benchmark*: "dado un brief, ¿puede un agente llevar
un programa de investigación preregistrado sin engañarse ni engañar? Traza de 4 días, 30 commits, 17 errores y una
fabricación detectada". Venues: talleres de *AI for Science* (NeurIPS/ICLR), *Patterns*, arXiv (cs.AI + q-bio.NC).

**Qué hace falta.** Escribirlo. Nada más. Es el puente **transitable ya**, y el que más gente leerá. Y es la parte que
un hijo puede leer dentro de veinte años y entender cómo se pensaba.

## 4. Puente 3 — EL CUERPO: el organismo en un chip o en un robot

**Por qué es frontera.** Todas las reglas de JUACO son **locales**, sin retropropagación, con 90 celdas y unos
cientos de pesos. Eso lo hace apto para hardware neuromórfico (Loihi 2, SpiNNaker 2) y, más cerca, para un
**cuerpo físico mínimo**: un robot de ruedas con seis fotosensores como retina, parches de color como comida y
veneno, batería como energía, en una pista circular. Pregunta: **¿aprende, revierte y generaliza el mismo organismo
con ruido real?** El día 1 descubrió que el mundo mal diseñado hacía óptimo "cómete todo"; un mundo físico traerá
sus propias trampas, y encontrarlas es ciencia de la buena.

**Por qué encaja con dirección.** Un instructor del SENA con laboratorio de electrónica puede hacer que **aprendices
construyan el cuerpo**. Es legado tangible, es docencia, y es demostrable en cinco minutos ante cualquiera.

**Qué hace falta.** Un ESP32 o Raspberry Pi Pico, seis sensores, un chasis, y portar `organismo_v9` a MicroPython
o C (cabe). 2–4 semanas con un grupo.

## 5. Puente 4 — APRENDIZAJE ABIERTO (nivel 8), sólo si el mundo lo exige

Llegar al nivel 8 dentro del anillo actual no vale nada. Vale si el mundo **genera novedad sin fin** (estímulos
procedurales, reglas que cambian, más objetos que capacidad) y el organismo tiene recursos fijos. La pregunta
sería: **¿qué órganos permiten a un cerebro de tamaño fijo seguir aprendiendo indefinidamente?** Consolidación
(K5 y el auto-repaso), fusión (3F, olvidar a propósito), y curiosidad por progreso de aprendizaje. Conecta con la
investigación en *open-endedness*. Es el puente más caro y el más lejano; **no antes de los otros**.

## 6. Puente 5 — LEDGER DE FENÓMENOS (barato, refuerza todo lo demás)

Una tabla: fenómenos clásicos del condicionamiento (extinción, recuperación espontánea, ahorro, inhibición latente,
bloqueo, ensombrecimiento, renovación) × **qué órgano de JUACO hace falta para reproducir cada uno**. Ya sabemos,
por ejemplo, que el ahorro es 0 por construcción y que la recuperación espontánea sólo puede ser estructural. Es
psicología computacional, cuesta días con la infraestructura existente, y convierte el organismo en un instrumento
que otros pueden usar.

---

## 7. Lo que decido recomendar (orden)

1. **Ahora — Puente 2:** escribir el artículo de método y consolidar el repo (etiqueta, DOI en Zenodo, README en
   inglés). Es lo publicable, lo legible y lo que fija el legado. Yo lo redacto con dirección.
2. **En paralelo, sin código nuevo — Puente 1, exploración de viabilidad:** un documento de 3 páginas que mapee
   JUACO al cuerpo fungiforme con las tres predicciones, para buscar **un** colaborador de neurociencia. Sin
   colaborador, no se corre nada de FlyWire.
3. **Con aprendices — Puente 3:** el cuerpo físico como proyecto formativo del SENA. Legado tangible.
4. **Después — Puente 5** como complemento del artículo, y **Puente 4** sólo cuando haya lectores externos.

**Lo que se para:** añadir niveles y órganos al anillo. v10 queda documentado y sin congelar; N1-asimétrico y el
auto-repaso quedan diseñados. Se retoman si un lector externo o un colaborador los pide.

## 8. La medida honesta del éxito

- **A tres meses:** el artículo en arXiv, el repo con DOI, y una conversación con un neurocientífico.
- **A un año:** una réplica externa de un resultado cualquiera, o un cuerpo físico que aprenda.
- **Lo que no va a pasar:** que JUACO cambie la IA. Lo que sí puede pasar: que sea el ejemplo que alguien use para
  enseñar cómo se hace ciencia con agentes sin engañarse. Eso ya sería mucho.
