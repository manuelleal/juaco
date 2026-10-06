## 10. El reloj

**Idea principal.** Decir "la selección no encontró tal cosa" sólo vale si la selección tuvo tiempo de buscar. El 1 de octubre se midió cuánto "tiempo evolutivo" habían tenido en realidad los experimentos anteriores, y resultó ser unas **diez veces menos** de lo que se creía: alrededor de 12 eventos de mutación por línea, no 150. Eso no convierte ningún NO en un sí, pero obliga a rebajar varias frases. El montaje de "perillas" se construyó para corregirlo: mide su propio reloj y exige un mínimo antes de leer el resultado.

Esta medición (llamada F0) está en `exploratorio/investigacion_20261001/F0_relojes.md` y su auditoría en `AUDITORIA_F0.md`. **Es trabajo fuera de protocolo**: un análisis de archivos ya existentes, auditado ("se sostiene con reservas"), pero no un experimento preregistrado.

### 10.1 Qué es un reloj, con una imagen

Piense en el juego del teléfono roto. Si el mensaje pasa por tres personas, cambia poco; si pasa por cien, puede terminar siendo otra cosa. Para que la selección "encuentre" algo necesita muchas rondas de copiar con pequeños errores y descartar las copias peores. El reloj cuenta cuántas rondas hubo.

Hay dos maneras de contarlas, y la confusión entre ellas fue el error:

- **Nacimientos.** Cuántos cuerpos nacieron en la cadena. Es lo que se contaba: unos 50 por linaje y pasaje, 150 en tres pasajes.
- **Profundidad mutacional.** Cuántas mutaciones hay **en la ascendencia de un genoma concreto**: de este cuerpo a su padre, a su abuelo, hasta el origen. Es lo que de verdad limita qué tan lejos puede haber llegado un gen.

No coinciden porque la mayoría de los nacimientos son "hermanos": salen de muy pocos padres (unos 5.7 por linaje y pasaje) y no se encadenan. Muchos nacimientos, poca profundidad.

### 10.2 Qué se midió

| Montaje | Profundidad mutacional | Comentario |
|---|---|---|
| O1 libre, serie | 11.6 de media (mediana 11.2) | 10 cadenas, 3 pasajes de 100 000 |
| O1 libre, réplica | 11.9 de media (mediana 11.6) | ídem |
| `o1_evo` y `entre_linajes` | "del orden de 20 a 30" | **No usar cifra exacta**: una sola serie, pocos genes medibles, cadenas que van de 3 a 58 |

Cómo se mide sin tener guardada la genealogía: en el brazo neutro los genes cambian sólo por azar, y la estadística dice cuánto se dispersa un número al que se le suman n errores del mismo tamaño. Midiendo la dispersión se despeja n. El auditor lo recalculó con un programa propio y le dio lo mismo.

Otros dos números de F0:

- **Tamaño efectivo de linajes: 8.27 y 8.10**, con un máximo posible de 9. Quiere decir que casi los nueve linajes aportan a la siembra por igual. La auditoría advierte que **no es un tamaño efectivo genético** en el sentido de los libros de biología: es sólo una medida de reparto.
- **Padres distintos en la siembra: 24 y 23.5** (de 90 genomas sembrados): casi clones.

### 10.3 Las correcciones de la auditoría

El informe original decía cosas más fuertes de lo que los números permiten. El archivo no se reescribió; lleva una fe de erratas que manda sobre el texto. En resumen:

1. Lo medido es el reloj **mutacional**. **El reloj de selección entre linajes no está medido.** Hay unas 224 refundaciones por pasaje que copian de linajes que paren más: eso es selección que la profundidad no cuenta. Así que 12 es una cota baja de las "rondas de selección", no su valor.
2. "150 contra 12" compara dos cosas distintas (nacimientos contra profundidad). Los nacimientos sobreestiman; la profundidad subestima.
3. La explicación "casi neutro" (que la ventaja era demasiado pequeña para que la selección la viera) **no se sostiene como explicación única**: en el mismo montaje la selección sí movió otro gen, PISO, en 10 de 10 cadenas, dos veces. El montaje sí transmitía selección de ese tamaño en 12 eventos.

### 10.4 Por qué importa

Porque cambia lo que se puede decir. Antes: "la selección afina perillas pero no inventa combinaciones". Después de F0, la frase corregida en el registro es:

> "Con los montajes corridos (O1 libre, unos 12 eventos mutacionales por línea; `o1_evo` y `entre_linajes`, del orden de 20 a 30, una serie, genes limitados), la selección afinó perillas continuas y no encontró combinaciones. No se midió el reloj de selección, de modo que no se concluye que no pueda."

Y "la selección sostiene a O1 frente a la deriva y no lo supera" lleva ahora la coletilla "vale para ese reloj, no para evolución larga".

En términos de aula: es la diferencia entre decir "este estudiante no puede aprender a dividir" y "en tres clases no aprendió a dividir".

### 10.5 Cómo lo resolvió el montaje de perillas

El preregistro de perillas se escribió ese mismo día, con F0 a la vista, y cambió cinco cosas:

| Problema | Solución en perillas |
|---|---|
| El reloj no se medía. | **Cada genoma lleva un contador** de las mutaciones de su ascendencia. No hay que estimarlo: se lee. |
| Las generaciones no se encadenaban dentro de un pasaje. | **Cámara continua**: cuando un linaje se extingue, el reemplazo copia con una mutación los genes de otro linaje vivo. El reloj corre aunque nadie se establezca. |
| Pasajes cortos, donde casi nadie se establece. | **Cinco pasajes de 100 000 pasos.** |
| Varios genes mutaban a la vez. | **Una mutación por nacimiento, en un solo gen.** |
| No había un mínimo de reloj exigido. | **Es condición de validez.** El brazo neutro debe alcanzar profundidad de 30 o más y 3 000 refundaciones o más, en 16 de 20 cadenas. Si no, el experimento "no se lee". |

Lo medido: el neutro llegó a **79.5 y 82.5** de profundidad mediana (mínimos 65 y 67) y a **4 819.5 y 4 841** refundaciones (mínimos 4 607 y 4 598). Es decir, unas siete veces el reloj de O1 libre.

Dos matices honestos:

- Los umbrales se exigen sobre el brazo **neutro**, porque representa la oportunidad que hubo si la perilla no ayudara. El brazo de selección tiene un reloj menor (39 y 36 de profundidad), porque cuando un linaje se establece deja de refundarse y su reloj se frena. La auditoría pide **no citar esos números como "el reloj de la selección"**.
- El propio autor del montaje predijo "unos 100 eventos por pasaje" y resultaron ser unos 13. Lo dejó anotado como predicción refutada.

### 10.6 Lo que sigue abierto

- Si con un reloj todavía más largo, o con mutaciones más pequeñas, la selección llega del primer escalón (GV de 0.19) al diseño (GV de 1). Es el plan 4 de la próxima sesión, con relojes y nulos nuevos antes de correr.
- Si el montaje de perillas, con su reloj, mueve algo en la pista vieja. Es el plan 1: MARGEN como gen desde cero.
- El reloj de selección entre linajes sigue sin una medida propia.
