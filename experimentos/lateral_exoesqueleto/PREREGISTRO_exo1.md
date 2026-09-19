# PREREGISTRO EXO-1 — JUACO como exoesqueleto de un LLM congelado (piloto + réplica)
Escrito el 18-sep-2026 ~21:50, ANTES de correr. Línea LATERAL (`registro/investigacion/HIPOTESIS_exoesqueleto_20260918.md`);
no toca el tronco ni la escalera. Pedido del director: "una última prueba hoy".

## Qué problema resuelve
Saber si la capa JUACO (valor por consecuencia, escritura de un golpe por sorpresa, sobrescritura ante contradicción,
contexto de 3 piezas por valor) aporta a un LLM de pesos congelados algo que un RAG no da: acertar en VARIANTES nuevas y
DESDECIRSE cuando el mundo cambia. Si empata con RAG, la hipótesis cae en su forma fuerte.

## Mundo (taller de cajas; `exo1.py`)
- 4 familias = material de la caja (latón, roble, cristal, hierro), dichas en el texto de la tarea.
- 4 herramientas con nombres sin sentido (vek, tulo, brim, saf) → el LLM no tiene prior.
- Regla oculta por familia y semilla: una herramienta ABRE (+1), una DAÑA (−1), dos NO ABREN (0). Consecuencia verificable.
- Superficie: color, tamaño, marca. Pool S1 (días 1, 2) y pool S2 NUNCA VISTO (día 3); día 5 mezcla S1+S2.
- Calendario (48 tareas): día 1 = 12 (3/familia; aquí se cometen errores), día 2 = 8 (situación relacionada),
  día 3 = 8 (variante: superficie nueva), día 4 = 12 (CAMBIO: en latón y roble la herramienta que abría pasa a NO ABRIR y
  otra neutra pasa a abrir; la que daña sigue dañando), día 5 = 8 (recuperación, todas las familias).
- Una acción por tarea; el LLM responde JSON {herramienta, prediccion ∈ abre|no_abre|dano}.

## Brazos (mismo LLM congelado: Claude Haiku vía `claude -p --model haiku`, sin herramientas, sin memoria de sesión)
- **A** LLM solo.
- **B** RAG léxico: guarda cada episodio como texto (día, descripción, herramienta, resultado); recupera los 3 más
  parecidos por TF-IDF coseno sobre la descripción (empate → más reciente).
- **Bf** RAG con filtro de familia (línea base FUERTE, añadida por honestidad): los 3 episodios más recientes de la misma
  familia. Si C no le gana, la capa de valor no aporta más que "recordar lo último de esta familia".
- **C** LLM + JUACO: tabla por familia×herramienta; Q lento (delta 0.3); episodio de un golpe si |resultado − predicción| ≥ 1
  o si el episodio guardado contradice el resultado (sobrescribe = reversión; lo contradicho se olvida); relevo: el episodio manda sobre Q si existe; contexto = 3 piezas de tamaño fijo
  (advertencia de valor más negativo, ejemplo de valor más positivo, estrategia vigente con confianza + no probadas).
- **Cx** control: C con las etiquetas de herramienta de la tabla permutadas al escribir el contexto (contenido falso).
- **J** referencia sin LLM: la tabla de C elige sola (argmax; no probadas antes que 0; empate al azar). No es brazo de la
  hipótesis: dice si el LLM suma o resta.

## Semillas
Serie 901–903 y réplica 904–906 (6 × 5 brazos LLM × 48 = 1440 llamadas). Nada se declara con una sola serie.

## Métricas (por brazo, sumando semillas de la serie)
M1 acierto (abre) por día; M2 errores repetidos = elegir una herramienta que ya DAÑÓ en esa familia; M3 día 4, familias
cambiadas: nº de veces que se vuelve a la herramienta vieja después de su primer fallo tras el cambio; M4 acierto día 5;
M5 caracteres de contexto (≈ tokens); M6 latencia media; M7 respuestas inválidas.

## Predicciones (escritas antes)
- P1 variante (día 3): acierto C − B ≥ 0.15 y C − Bf ≥ 0.10.
- P2 cambio (día 4, latón+roble): M3 de C < M3 de B y < M3 de Bf; y acierto día 4 cambiadas C > Bf.
- P3 recuperación literal (día 2): |C − Bf| ≤ 0.15 (empatan donde basta recordar).
- P4 A peor que B, Bf y C en acierto días 2–5.
- Control: Cx pierde ≥ 0.30 de acierto días 2–5 contra C (el contenido es lo que paga, no el formato).
## Qué refuta
- C ≈ Bf (|Δ| < 0.10) en día 3 Y en día 4-cambiadas → la capa JUACO no aporta más que memoria reciente por familia.
- C ≈ B (|Δ| < 0.15) en día 3 Y día 4 → la hipótesis cae también en la forma débil (la del documento).
- Cx ≈ C → el efecto no es del contenido.

## Límites dichos de antemano
La familia viene explícita en el texto (la clave de JUACO está regalada; el mundo no mide descubrir familias). El RAG es
léxico, no de embeddings. Un solo LLM (Haiku). Mundo de juguete: si C gana, sólo dice que el mecanismo funciona en el caso
fácil; si pierde aquí, cae en serio. J puede igualar a C: eso diría que en este mundo el LLM no razona nada útil.
