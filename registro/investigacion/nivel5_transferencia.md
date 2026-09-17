# Nivel 5 — Transferencia (escalera del punto 6): investigación y propuesta

**17 sep 2026, noche del día 5. Documento de investigación, no preregistro (salvo la sección 7).** Base: tronco v13,
N1 cerrado, N2 refutado, N2b preregistrado. Sin ejecutar nada. Definición de nivel: lo aprendido en un
contexto/organismo sirve en otro — entre organismos (cultural), entre tareas/mundos, entre generaciones (herencia),
de un sensor a otro.

## 1. Qué existe

*Juegos de señalización (Lewis/Skyrms) y su dinámica de refuerzo:*
- Lewis, D. (1969), *Convention*: el significado de una señal es una convención de equilibrio en un juego
  emisor–receptor, no algo dado de antemano.
- Skyrms, B. (2010), *Signals: Evolution, Learning, and Information*: una dinámica de refuerzo simple, tipo
  Roth–Erev (ajustar la probabilidad de una acción según su resultado; Roth y Erev, 1995, *Games and Economic
  Behavior*), hace emerger la convención en juegos de Lewis repetidos, sin razonamiento ni gradiente global.

*Transmisión cultural / comunicación emergente en agentes artificiales:*
- Lazaridou, A., Peysakhovich, A. y Baroni, M. (2017), ICLR: protocolos referenciales emergen entre redes
  entrenadas de punta a punta con gradiente compartido.
- Mordatch, I. y Abbeel, P. (2018), AAAI: lenguaje composicional emergente, también con gradiente compartido entre
  agentes.

*Aprendizaje social/vicario en animales y teacher–student en robots:*
- Bandura, A. (1977), *Social Learning Theory*: aprender observando las consecuencias de otro, sin ensayo propio.
- Rendell, L. et al. (2010), *Science*: torneo de estrategias de aprendizaje social; copiar rinde más que aprender
  solo bajo condiciones, no siempre.
- Thomaz, A. y Breazeal, C. (2008), *Artificial Intelligence*: cómo un humano enseña a un robot y qué debe
  interpretar el aprendiz de esa señal.
- Argall, B., Chernova, S., Veloso, M. y Browning, B. (2009), *Robotics and Autonomous Systems*: revisión de
  aprendizaje por demostración.

*Herencia lamarckiana en vida artificial:*
- Baldwin, J.M. (1896) e Hinton, G. y Nowlan, S. (1987, *Complex Systems*): aprender en vida puede orientar la
  selección genética sin heredar directamente lo aprendido (efecto Baldwin).
- Whitley, D., Gordon, S. y Mathias, K. (1994) [verificar]: compara heredar directamente lo aprendido contra el
  efecto Baldwin en algoritmos evolutivos.

No encontré, con la confianza que pide la regla de no inventar, un trabajo que combine las cinco condiciones de
JUACO a la vez. Lo registro como ausencia, no como cita.

## 2. Qué falta en la literatura para nuestro caso

- Casi toda la señalización emergente citada (Lazaridou, Mordatch) depende de backprop o un crítico centralizado:
  el gradiente cruza del receptor al emisor por construcción. En v13 cada vía aprende de su propio error (regla 4
  del CLAUDE.md); no hay ese cruce.
- Los modelos de refuerzo tipo Skyrms/Roth–Erev sí son locales, pero su receptor siempre actúa en proporción a su
  tabla de refuerzo (softmax); nunca hay una puerta dura que exija confianza antes de actuar. Esa puerta es lo que
  usó N2, y no es un caso que esa literatura estudie.
- Ningún resultado de la lista opera bajo apuesta letal: un episodio con reinicio no cuesta lo que cuesta una
  mordida de veneno para un cuerpo sin reinicio. La literatura de agentes puede explorar barato al inicio; JUACO no.
- No hay literatura que pueda garantizar sobre dos vías de aprendizaje concurrentes (rápida por código, lenta
  lineal) arbitradas por una puerta de familiaridad, más un canal social encima de las dos.
- La literatura lamarckiana hereda pesos o políticas completas; no hereda una convención de señalización a medio
  formar entre dos individuos no emparentados (experto–novato, no padre–hijo).

## 3. Mecanismo mínimo compatible con v13

**Diagnóstico de N2** (`datos/N2_s1-20_20260917_181950`, log completo leído): E1 (convención) 1/20, consistencia Q4
mediana 0.50 — azar —, símbolos distintos 6/20. E2 (decodificación) 1/20, contraste mediana +0.00 y +0.03 (M crudo
−2.69 / −2.63: casi idéntico para los dos símbolos). E4 (beneficio): veneno del novato en CONV, mediana 375, peor
que N0 (318) y que SOLO (319); INNATO llega a 194. E5 se sostiene: barajar destruye lo poco que había. Refuerzos del
emisor: 37.088 a favor contra 692 en contra — casi ciego al símbolo — y `Pq` termina saturado en el tope (±3) para
los dos símbolos del mismo estado. Causa (ya escrita en la ENMIENDA 1 del preregistro, confirmada por estos
números): el receptor sólo actúa sobre el símbolo con `|C| ≥ 0.5`, y no llega a esa confianza porque nada generó
antes la diferencia que la confianza necesita. Círculo sin gradiente, no error de medida (K1 pasa 3/3; se revisó el
instrumento primero, regla 5).

**Corrección ya preregistrada (N2b):** quitar la puerta de acción (el símbolo entra en la decisión desde el primer
paso como sesgo `gamma_sim·C[s]`, no como umbral) y el emisor aprende por ventaja (refuerzo menos línea base móvil)
en vez de refuerzo bruto. Estado real, verificado ahora: la corrida arrancó (`datos/N2b_s1-20_20260917_183004.log`,
K1 y progenitores hechos) y el log se corta al entrar a las 100 corridas — no hay JSON ni veredicto. No se puede
decir que N2b funcionó ni que falló; sigue abierta.

**Encuadre:** N2 no es requisito para cerrar el nivel 5 tal como lo define el punto 6 (transferencia entre
organismos, tareas, generaciones, sensores). N1 ya cierra el eje cultural. El significado emergente es, en la
numeración propia del punto 16, la etapa 7 (comunicación), no la 5.

**Mecanismo mínimo para cerrar el nivel** (mundo, no órgano nuevo; ≤15 líneas):
1. Cero órganos nuevos en v13 para los tres ejes que faltan.
2. Reusar progenitores ya vividos (200.000 pasos, en `datos/` de N1/N2): costo marginal ~0.
3. Mundo-tarea: el mismo progenitor, plasticidad activa, cae en una regla distinta (lineal → azar, o mundo
   invertido) sin reiniciar `Wp`/`Wn`/código Kenyon.
4. Mundo-generación: un hijo hereda `Wp`/`Wn` (no `Pq` ni `M`) del progenitor de (3) en el mundo ya cambiado;
   formaliza con preregistro y réplica lo que la Etapa 4 dejó "no consistente" en el mundo invertido.
5. Mundo-sensor (= N3): dos v13 con la retina partida en mitades complementarias (0–2 / 3–5), señal honesta de N1
   (no la de N2), sobre la regla no lineal ya usada en la Etapa 3.
6. Ningún canal de aprendizaje nuevo: Rescorla-Wagner como siempre, señal honesta como en N1.
7. Cierre: identidad K1 con señal apagada, controles N0/SHUF ya estandarizados, réplica en semillas nuevas antes de
   declarar.

## 4. Cómo acortar la línea

- N2/N2b se mueven a la etapa 7 (comunicación, punto 16) y dejan de bloquear el cierre de nivel 5; se retoman con
  lector externo o cuando los otros tres ejes cierren.
- Transferencia de tarea y de generación (mundo-tarea, mundo-generación arriba) no piden órgano nuevo: se corren ya,
  reusando progenitores existentes.
- Transferencia de sensor (nivel 5) y composición (nivel 7, N3) se funden en una sola batería: mismo diseño, misma
  corrida, dos niveles resueltos con un dato.
- **Experimento único que más información da por corrida:** la batería fundida sensor+composición (mundo-sensor).
  Responde a la vez si hay transferencia entre sensores y si la pareja resuelve lo que ninguno resuelve solo,
  reusando el canal honesto ya cerrado (N1) y la medida ya tomada de la regla no lineal en un solo organismo (0.44,
  Etapa 3) como referencia. Un resultado ahí, en cualquier dirección, vale más que los otros dos ejes juntos, que
  son extensión directa de algo que ya casi se sostenía (Etapa 4).

## 5. Romper la frontera

Idea — combinación no probada, no una técnica nueva: un **período crítico** para el canal social, medido en
mordidas propias del receptor, no en pasos de reloj. Hoy N2 usa una puerta dura y N2b un peso fijo (`gamma_sim`
constante) para mezclar valor propio y valor por símbolo. Proponer que ese peso decaiga con la experiencia propia
acumulada del receptor: alto al nacer, cuando no hay nada propio con qué competir por la varianza; bajo después,
cuando el receptor ya sabe por sí mismo. No pide gradiente: es un estado local más (contador de mordidas propias) y
una función decreciente, de la misma familia que `memoria_rechazo` ya usada en v9. Por qué podría funcionar: ataca
el mecanismo de falla medido en N2 (el aprendizaje propio del novato borra la ventana en la que el símbolo tenía con
qué correlacionarse) sin reintroducir la puerta dura que impidió que N2 cerrara el círculo. Cómo se refutaría:
preregistrar, pareado contra N2b con `gamma_sim` constante, que la versión con período crítico gana en E1 y E2 en
≥15/20 semillas; si no gana, o cae en los mismos umbrales que N2, se descarta sin volver a tocarla.

## 6. Trampas

- E1 podría pasar por saturación de `Pq` en el tope sin relación con la conducta del receptor, si el sorteo inicial
  ya correlaciona signo con estado; el control real es E5 (barajar), no E1 aislado.
- Un acierto en la batería sensor+composición podría venir de que dos cuerpos exploran más casillas (el hallazgo de
  N0: ser dos ya cambia el mundo), no de combinar información — exige control de "mitades iguales" (los dos ven el
  mismo tercio) además de N0/SHUF.
- La transferencia generacional podría "pasar" porque heredar cualquier `W` no nulo frena la exploración temprana y
  eso protege, sin que el contenido heredado sea correcto — control: heredar `W` de igual magnitud pero barajado
  entre patrones.
- Contar sólo sobrevivientes infla cualquier beneficio (la muerte filtra la muestra); reportar muertes aparte, no
  sólo el valor final, en los tres ejes.
- Declarar el nivel cerrado con una sola tanda de semillas, sin réplica en semillas nuevas — el error ya cometido y
  corregido en ERR-21; aplica igual aquí.

## 7. Propuesta en formato del proyecto

**Hipótesis.** Dos v13 con mitades de retina complementarias (0–2 y 3–5) y el canal honesto de N1 resuelven en
pareja una regla que ninguno resuelve solo (la no lineal de la Etapa 3, donde un organismo con retina completa y
vía lenta obtiene 0.44); eso es transferencia entre sensores (nivel 5) y composición (nivel 7) en el mismo dato.

**Mundo.** `mundo_social`, 2 organismos v13, retina de cada uno enmascarada a 3 píxeles fijos y complementarios;
regla de valencia no lineal de la Etapa 3, repartida entre las dos mitades; señal de placer/asco honesta de N1 sin
cambio de constantes; semillas 1–20, T=200.000.

**Medidas.** Aciertos pareados por semilla en patrones conocidos y nunca vistos; mordidas de veneno; muertes;
acierto de cada organismo con su mitad sola y de un v13 de referencia con retina completa.

**Predicción numérica (mía, sin correr nada).** Pareja con señal ≥0.75 de aciertos en conocidos, frente a ≤0.55 de
cada mitad sola y ~0.50 de la pareja barajada; en nunca vistos, pareja ≥0.65 frente a ≤0.50 de cada mitad. Incierto:
no sé si un canal diseñado para "bien/mal de un patrón entero" alcanza para portar información de una mitad ajena
sin distorsión.

**Criterio de refutación.** Si la pareja con señal no supera, pareada, tanto a cada mitad sola como a la pareja
barajada en ≥15/20 semillas, se refuta la composición por esta vía.

**Controles.** Identidad K1 (señal apagada ≡ v13 con media retina, sin plasticidad social); N0 (pareja sin señal);
SHUF (señal barajada); mitades iguales (ambos ven el mismo tercio, no complementario); referencia de retina
completa (techo).

**Coste estimado.** 5 condiciones × 20 semillas = 100 corridas; N2 corrió el mismo tamaño (100 corridas, 5
condiciones, T=200.000, Pool(14)) en 298.5 s reales — orden de minutos. Réplica en 21–40 sólo si pasa: 100 corridas
más.
