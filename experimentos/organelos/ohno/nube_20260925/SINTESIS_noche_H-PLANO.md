# Lo que dicen juntas las dos series de esta noche: H-PLANO (hipótesis, no resultado)

Nube, 25-sep-2026, 04:10. Es una lectura cruzada de datos ya registrados. No se corrió nada nuevo para escribirla.

## Los cuatro datos
1. **Anfitrión (26001–26020, NO).** La selección llevó el control al valor que ya tiene de fábrica el brazo sin control: tx 0.97, san 0.03. Que CONTROL no le gane a SIN_CONTROL (9/20) es un empate por convergencia.
2. **Ohno (25011–25030, NO).** La mutación es carga pura:
   - VIDA no persiste nunca donde FIJO muere (0/20); FIJO sí persiste donde VIDA muere (4).
   - Nacen 6 cuerpos antes del corte y el cuello es de 1–5 cuerpos.
   - Lo que persiste vuelve a filtra0.
3. **Gramática (21011–21030, NO, del PC).** La selección desde un slot al azar no encuentra el órgano que el diseño fijo ya da.
4. **Código genético v0 (exploratorio de Fable, del PC).**
   - CODIGO vive mejor que PERILLAS en casi todos los mundos, también en QUIETO, y la ventaja viene de los **errores de copia más neutros**: ~0.65 contra ~0.40 hijos con fenotipo idéntico.
   - Es el único paquete de la línea donde la variación "gana". Y no gana por hallar función nueva: gana por **amortiguar su propia mutación**.

## H-PLANO
**En los mundos de organelos, con poblaciones de 1–30 cuerpos y pocos partos por generación, la selección no premia función nueva; premia la robustez a la propia mutación.**
- Es la "supervivencia del más plano" (Wilke, Wang, Ofria, Lenski y Adami, *Nature* 2001), que se da con mutación alta y N chico.
- Regla de bolsillo de genética de poblaciones: la selección le gana a la deriva sólo si N·s > 1. Con N ≈ 5 hace falta una ventaja s > 0.2 por generación, y ningún órgano nuevo la da de golpe.
- Por eso todo paquete que pide "que la evolución cree X" choca con el mismo muro, y el único que se movió fue el que evolucionó robustez.
- Encaja con F9-4bis ("el muro es el mundo"), visto ahora desde el lado de la población.

## Predicciones que la pueden tumbar (para un preregistro, si el director quiere)
1. **Umbral de N·s.** Con el paquete de Ohno tal cual, pero un vivero que produzca ≥ 200 partos antes del corte (N·s alto), VIDA deja de ser carga: la persistencia pareada "sólo FIJO" baja de 4 a ≤ 1. Si sigue en ≥ 4, H-PLANO cae.
2. **Mutación a la mitad.** Con `p_mut` a la mitad en el mismo mundo pobre, la diferencia VIDA − FIJO se achica en proporción. Si no se mueve, la carga no es mutacional y H-PLANO cae.
3. **Robustez como precursora.** En CODIGO, la fracción de hijos neutros crece con la generación antes de que aparezca cualquier fenotipo nuevo. Si lo nuevo aparece sin robustez previa, H-PLANO cae en su versión fuerte.

## Qué implicaría para la misión
- Para que la evolución cree órganos aquí, primero hay que darle **población y tiempo** (N·s > 1), y quizá **robustez** (CODIGO) como sustrato.
- Hay que hacerlo **antes** de preguntarle por función nueva.
- Pedirle a un linaje de 5 cuerpos que invente es pedirle a la deriva que haga el trabajo de la selección.
