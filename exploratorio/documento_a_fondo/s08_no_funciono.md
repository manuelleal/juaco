## 8. Lo que no funcionó y lo que se cayó

**Idea principal.** En el registro los negativos ocupan más espacio que los positivos, y se escriben con el mismo cuidado. Hay tres clases: lo que dio **NO** con protocolo, lo que **se cayó** porque una señal inicial no se repitió, y lo que se **cerró sin construir** porque una sonda mostró que no había espacio para ganar. Para el póster esta sección es tan valiosa como la anterior: muestra que el método tumba cosas, incluidas ideas del director y predicciones de los propios agentes.

### 8.1 Los intentos contra el muro

Todos en la pista vieja. La referencia: O1 cruza entre 135 y 139 linajes de 180.

| Intento | Qué se probó | Resultado | Qué enseñó |
|---|---|---|---|
| GLOTU y GLOTU + PATAS (25 y 28 de septiembre) | Añadir piezas al tronco. | NO las dos. 0 de 20 semillas cruzan. | Ganarle al tronco no es cruzar. |
| TERMO (28 de septiembre) | El termostato de boca. | Modesto ×2 (sección 7.1). | La mayor parte de la distancia estaba en la boca frente a lo bueno. Tras esto el director declaró el muro "mapeado". |
| Dinamita (28 de septiembre) | Cuatro tandas de variantes: vetos, limpieza, patas. | **Se cerró sin informe**: el agente nunca lo entregó. La lectura del auditor: tocar lo malo en la boca da 0 de 10; una variante de patas parecía ganar, pero era la mejor de doce en las mismas diez semillas. | Dejó dos reglas (ERR-154 y ERR-155): una predicción escrita con datos a la vista no es predicción; nada se guarda como cerrado sin haberlo leído. |
| Patas sobre TERMO (29 de septiembre, serie) | Cambiar sólo a dónde va el cuerpo. | NO. 101 contra 90 de TERMO; la puerta que pasó lo hizo en el borde exacto y en semillas nuevas se deshizo (96 contra 92). | El "15 de 20" era un borde. El organismo comía más y pelaba el mundo, pero no decidía mejor. |
| Veto sobre TERMO (29 de septiembre, serie) | Prohibir sólo las mordidas malas que el cuerpo no puede pagar. | NO claro: 35 contra 92 de TERMO. | Salvó al recién nacido (muertes tempranas de 13 % a 0.4 %) y hundió al linaje: el hijo moría de hambre más tarde y el mundo se tapaba. Arreglar un síntoma empeoró el conjunto. |
| Un sentido de "riesgo de morder" (29 de septiembre) | Darle al organismo un sentido que pone la decisión de O1 a una sola regla de distancia. | NO. La regla no se fijó en ninguna de 5 cadenas (0.0 %). Puesta a mano sí cruzaba más (23 de 45). | El sentido contenía una política que servía; la selección por pasajes no la encontró. |
| Ocho cuerpos por linaje (29 de septiembre) | Una pista con población por linaje. | NO: 17 contra 16 del neutro, de 45. | Más cuerpos, con ese genoma y ese tiempo, no separan selección de azar. |
| Mundo enriquecido (29 de septiembre; idea del director, por los chimpancés) | Nueces que sólo abren tras una llave, con un canal para copiar al que abrió. | NO. | La selección fijó "evitar la nuez" en casi todos los vivos. **Evitar es más barato que aprender.** |
| Baldwin y Baldwin con exploración (29 de septiembre, dos series) | Un gen de "plasticidad" en un mundo donde las letras se invierten. | NO las dos. 0 de 20 persisten con inversión. | La regla sólo aprende después de morder, y un órgano de rechazo impide morder: nunca se entera de que el mundo cambió. El NO vale para esa forma de plasticidad, no para toda. |
| O1 con cuatro genes heredables, `o1_evo` (30 de septiembre, una serie) | ¿La selección mejora a O1? | NO por la regla: 128 contra 135 de fábrica. | Pero 128 contra 81 del neutro: **la selección conserva a O1 y no lo mejora.** |

**La lectura de conjunto, escrita el 29 de septiembre:** las piezas de O1 sueltas no cruzan; O1 funciona como conjunto. Una nota del 1 de octubre le puso el matiz que le faltaba: con los montajes corridos la selección afinó perillas y no encontró combinaciones, pero **el reloj de selección no se había medido**, de modo que no se puede concluir que no pueda.

### 8.2 La moneda del muro

"Moneda" es en qué se le paga a un linaje para que sus genes pasen al siguiente pasaje: estar vivo en un instante, o haber durado.

- **Primer experimento (29 de septiembre, 5 cadenas).** Se sembró a mano, en la mitad de la población, la regla que cruza, y se miró si diez pasajes cortos la purgaban o la conservaban. Indeterminado: derivó igual que una regla neutra (0.247 contra 0.253).
- **Segundo (30 de septiembre, 5 cadenas).** Con pasajes de 100 000 y siembra sólo de establecidos, la regla pareció subir a 0.80 contra 0.14 del neutro. Se escribió "CONSERVA, en el umbral" y, peor, se escribió como causa.
- **Réplica (1 de octubre, 10 cadenas, preregistrada).** La regla terminó en **0.0** con la moneda y en **0.42** con el neutro. Cruce: 41 contra 42 de 90. Indeterminado: no replicó.

Qué enseñó: lo que cuenta la sección 6 bajo ERR-177. Y un dato de fondo que sí quedó: con pasajes de 25 000 la selección **purga** esa regla (0.26 contra 0.64).

### 8.3 Planear (P9)

"Planear" se definió de forma operacional: hacer A para que después B valga. El mundo: el oasis sólo paga a quien mordió antes una letra neutra, la "llave". El módulo: cuando un bocado da más de lo esperado, la última letra mordida antes recibe parte del crédito.

- **Tres pruebas cortas, tres mundos distintos, sin señal.** Los tres brazos colapsaban (vida mediana de 200 a 300 pasos) y el control con el crédito mal asignado cruzaba igual o más. Cerrado por la regla de parada.
- **Antes de volver a construirlo se hizo algo sensato: una sonda de "¿hay espacio?".** Se comparó el piso contra un oráculo que ya sabe el plan. Resultado: piso 8, oráculo 6, azar 6, de 18. El oráculo no le ganaba al piso. **ESPACIO NO**: se liberó sin construir.

Qué enseñó: antes de construir un módulo, medir si el mejor caso imaginable gana algo en ese mundo. Y un detalle físico: el tope de niveles (1.5) y el gasto fijo se "comen" cualquier premio de energía adicional.

### 8.4 La colonia pegada (P2)

La idea venía de un experimento famoso con levadura: células hijas que se quedan pegadas a la madre y forman un grupo que sobrevive mejor a un filtro. Aquí: un "cuello" que mata a los sueltos con más probabilidad que a los agrupados.

- Cinco pruebas cortas: tres con O1 y dos con la célula nativa de ECO, incluida la versión más favorable posible (el cuello sólo mata a los sueltos).
- En todas, pegarse **costó** (menos partos, menos vivos) y no pagó: en la última, 0 de 18 persisten pegados contra 4 de 18 sueltos.
- Una pista que apareció con O1 ("pegarse protege al recién nacido") **no se repitió** con la otra célula.

Qué enseñó: el grupo pela su propio vecindario. Se reabriría sólo con un mundo donde el recurso esté en manchas o con reparto de comida dentro del grupo.

### 8.5 El tramo de sexo y familia (idea del director)

Reproducción de a dos y reducción de camada, en ECO. Sin señal, y por una razón de instrumento: en el mundo de nueve quedan entre 2 y 5 cuerpos vivos, y no hay familias que medir. En la prueba de reproducción de a dos, mezclar genes de dos padres **restó** (578 nietos contra 772 del clon con pareja), que era justamente el caso en que el control podía ganar. **No está refutado: no hay instrumento.** Necesita un ECO grande.

### 8.6 COMP, la primera versión de la celda retenida

En el peldaño P8 se probaron dos versiones del módulo. La primera, COMP, dio "hay algo modesto" en la serie (y por igualdad exacta con el corte: 0.25 contra 0.25) y **NO** en la réplica (13 de 20 semillas, el corte era 15). Por la regla de parada, un modesto que no se repite **no se declara**. La segunda, COMP2, es la que funciona (sección 7.10).

Qué enseñó: la sonda previa había dado 0.5 con un instrumento ligeramente distinto; al criar el organismo como era debido, la cifra no se repitió. Una sonda sirve para fijar umbrales, no para anticipar el resultado.

### 8.7 O1 libre con poderes (sesión paralela)

Otra sesión del proyecto le dio a O1 cuatro "poderes" apagados (memoria de lugar, copiar a otros, reserva, pausa) para ver cuál prendía la selección. En la serie, la memoria de lugar subió en 10 de 10 cadenas (diferencia 0.0596, justo sobre el umbral de 0.05). Se escribió "cuando puede elegir, la selección elige la memoria de lugar". La réplica dio 6 de 10 (diferencia 0.047). **BLOQUE NO**; la frase se retiró.

Qué enseñó: una diferencia pegada al umbral no es un resultado. Lo único que se repitió dos veces fue lo descriptivo: la selección sostiene a O1 frente a la deriva y no lo supera, y eso vale para un reloj de unas 12 mutaciones por cadena.

Es interesante ponerlo al lado de "perillas", que sí funcionó dos veces con la misma memoria de lugar: la diferencia fue el montaje (un mundo que la paga, una mutación por nacimiento con sesgo, cámara continua, reloj medido), no la idea.

### 8.8 Un gen por parto

La misma sesión paralela probó después una hipótesis razonable: quizá lo que tapaba el efecto era la "carga" de mutar muchos genes a la vez. Se cambió a una mutación por parto. La carga efectivamente desapareció (el neutro llegó a R0 0.97), pero el organismo libre cruzó **57 contra 72 de O1**. NO.

Qué enseñó: la carga mutacional no era lo que impedía ganar.

### 8.9 Otros negativos que conviene conocer

- **Lo que la selección logra en ECO no se traslada a la pista.** Los genomas seleccionados en ECO, llevados a la carrera, empeoraron al organismo (dos pruebas exploratorias). El arranque en frío tampoco se trasladó.
- **Aprender dentro de una vida no descubre la limpieza.** Un organismo que corrige por refuerzo cuándo morder (22 y 23 de septiembre, modesto replicado) aprendió a **contenerse**, no a limpiar; y esa ventaja sólo existía si se heredaba.
- **El significado de una señal no surge por refuerzo** en este organismo: seis diseños cerrados en septiembre. Por eso en P7 el significado se da por diseño y se dice.
- **La curiosidad** (por novedad, por progreso) se refutó en un mundo donde explorar no pagaba. Por eso P10 se probó en un mundo donde sí paga, y no se le llama curiosidad.

### 8.10 Lo que dicen juntos

1. **Evitar es más barato que aprender.** Cuando la selección puede resolver algo evitándolo, lo evita.
2. **Las piezas sueltas de un organismo que funciona no funcionan solas**, y a veces dañan.
3. **Una señal en el umbral no es una señal.** Tres veces en una semana algo "casi pasó" y la réplica lo tumbó (patas, O1 libre, la moneda).
4. **Antes de construir, medir si hay espacio.**
5. **Varias de las ideas caídas eran del director**, y están registradas igual que las demás. Eso no es un defecto del proyecto: es la prueba de que el método no distingue de quién es la idea.
