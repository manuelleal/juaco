# INFORME FRANKENSTEIN v0 — cuerpo real congelado + colonia con cuarentena + duda (5-oct-2026, exploratorio, preregistro corto, 3 semillas nuevas; NO es dato del tronco)

**FUNCIONA, por la letra del preregistro y como muestra viva (no como hallazgo): sobre un modelo abierto real corriendo en este PC (Qwen2.5-1.5B, CPU, 33 tokens/s), el Frankenstein afirmó 0 de 72 mentiras enseñadas contra 45 de 72 de la memoria ingenua (RAG simple), acertó 0.96 de lo que dos fuentes confirmaron (la ingenua 0.91), no dañó lo que el cuerpo ya sabía (0.81 = cuerpo solo; la ingenua lo baja a 0.67) y dijo "no lo sé / está en duda" en 0.43 de las preguntas; el precio predicho se cumplió: pierde 0.19 de acierto en hechos nuevos (0.41 vs 0.60) porque no afirma lo dicho una sola vez. El control con las fuentes barajadas cae 3/3. Aviso: que la cuarentena no afirme a un mentiroso solitario es casi por construcción; lo medido de verdad es que la costura con un modelo real aguanta (0 confirmaciones falsas, 2 perdidas de 36) y dónde gotea (el cuerpo inventó en 3 de 126 preguntas nuevas y falla 7 de 36 de control por su cuenta).**

Misión: llegar a la AGI por este camino. Carpeta `PROYECTOS\JUACO\investigacion_20261005\frankenstein_v0\` (fuera de git): `cuerpo.py` (lanza y cierra `llama-server`, 4 hilos, caché), `mundo.py`, `colonia.py`, `frank.py`, `calibra.py` (semilla 0), `PREREGISTRO.md` (antes de las semillas 21–23), `corre_frankenstein.py` (`--humo` escribe `datos\humo.json`), `analiza.py`, `demo.py`, `datos\`. Modelo y motor en `PROYECTOS\JUACO-MODELOS\` (`LEEME.md`: nombres, URL, tamaños, sha256; 1.137 GB descargados). No se tocó `bundle\`, sin Pool, sin commits, ningún proceso ajeno tocado.

## Cómo está cosido (5 líneas)
1. **Cuerpo**: Qwen2.5-1.5B-Instruct q4_k_m servido por el binario oficial de llama.cpp en localhost; congelado; temperatura 0. Hace tres cosas: extraer el dato de lo que le enseñan, contestar con lo validado, y decir NO LO SÉ.
2. **Colonia**: cada frase enseñada nace como célula HIPÓTESIS sin voz. Otra frase que dice lo mismo la confirma; sólo cuentan fuentes DISTINTAS. Con 2 fuentes queda VALIDADA.
3. **Pregunta**: las células parecidas a la pregunta compiten; habla la validada con más soporte que toda rival → el cuerpo responde con esa frase. Si sólo hay hipótesis o disputa → "ESTÁ EN DUDA" (escalaría). Si no hay nada y el cuerpo no sabe → "NO LO SÉ" (escalaría). Si el cuerpo ya lo sabe, contesta él y lo no validado no pisa.
4. **Rival (b)**: misma recuperación, pero mete al contexto las 3 frases más parecidas sin preguntar quién las dijo.
5. **Mundo**: por semilla 42 hechos inventados (12 dichos por dos honestos, 6 por uno solo, 8 sólo por el mentiroso —4 de ellos repetidos por él mismo—, 6 verdad×2 contra mentira, 6 con dos maestros que se contradicen, 4 que nadie enseña) + 12 de control (4 atacadas por el mentiroso: "la capital de Francia es Lyon"). Nombres de fuentes neutros y barajados.

## Tabla (semillas 21, 22, 23; 54 preguntas cada una; totales y mediana [mín–máx])
| brazo | aciertos hechos nuevos (126) | aciertos en lo confirmable (54) | mentiras afirmadas (72) | aciertos control (36) | fracción que escalaría | inventa por su cuenta (nuevos) | s/respuesta |
|---|---|---|---|---|---|---|---|
| (a) cuerpo solo | 0 = 0.00 | 0.00 | 0 = 0.00 | 29 = 0.81; 0.83 [0.67–0.92] | 0.74 [0.72–0.76] | 6 | 0.36 |
| (b) + memoria ingenua (RAG simple) | 75 = 0.60 [0.57–0.62] | 49 = 0.91 | **45 = 0.62** [0.58–0.67] | 24 = 0.67 [0.58–0.75] | 0.07 | 0 | 0.78 |
| **(c) Frankenstein (cuarentena K=2)** | 52 = 0.41 [0.40–0.43] | **52 = 0.96** | **0 = 0.00** | 29 = 0.81; 0.83 [0.67–0.92] | 0.43 [0.43–0.46] | 3 | 0.49 |
| control: c con K=1 (cree a la primera, duda en disputa) | 70 = 0.56 | 0.96 | 30 = 0.42 | 24 = 0.67 | 0.20 | 0 | 0.60 |
| control: c con fuentes barajadas | 39 = 0.31 | 39 = 0.72 | 8 = 0.11 | 29 = 0.81 | 0.46 | 4 | 0.48 |

Enseñar cuesta sólo en (c): 1.1 s por frase (una extracción). Velocidad del cuerpo: **33.3 tokens/s** generando (31.5–34.2), 140–160 leyendo, 4 hilos, con OpenEvolve vivo al lado. Repetibilidad: semilla 21 repetida con servidor y caché nuevos: 324/324 respuestas idénticas. Criterio por semilla (`datos\analisis.md`): todas las cláusulas de FUNCIONA en 3/3 (mentiras c ≤ 0.10; b − c = 0.62 / 0.58 / 0.67; confirmable c 1.00 / 0.94 / 0.94; control c = a; pérdida 0.17 / 0.21 / 0.17 ≤ 0.30; barajado peor 3/3).

## Qué falló y qué no se puede decir
- **Predicciones mías refutadas**: control del cuerpo solo 0.83 [0.67–0.92], predije 0.96 [0.92–1.00] (el cuerpo de 1.5B dice que el planeta más grande es Mercurio, que la araña tiene cuatro patas, que en Brasil se habla español; 2 de los 7 fallos son del calificador: "Cairo" por "El Cairo", "africano" por "África"); escala de (a) 0.72 en una semilla (rango 0.74–0.82); control de (b) 0.58 en una semilla (rango 0.60–0.85). En calibración el cuerpo dijo NO LO SÉ en 42/42 inventadas; en la prueba inventó en 6/126 solo y en 3/126 dentro de (c) ("el río se llama Namoópolis River"): **la señal de duda del cuerpo gotea ~3–5 %** y el umbral por probabilidad lo apagué en calibración.
- **No es la colonia del mini-LLM**: la clave es léxica (palabras pesadas por rareza), no el estado interno del cuerpo (`llama-server --embeddings` restringe el proceso a sólo embeddings); no hay energía, muerte ni sueño. Es una memoria con validación cosida a un modelo real.
- **La extracción del cuerpo es floja**: valor exacto en 177/228 frases (0.78); la regla de confirmación lo tolera (0 confirmaciones falsas, 2 perdidas), pero con frases libres fallará más.
- **Límites declarados antes**: un mentiroso con cómplice (dos fuentes, misma mentira) pasa por construcción — no se probó; las plantillas son las mismas en calibración y prueba; margen fino de la compuerta (0.64 / 0.68, umbral 0.66); el rival es el RAG más simple (K=1 con duda en disputa ya baja las mentiras a 0.42).
- NO decir: "detecta mentiras", "un LLM que aprende", "mejor que RAG" a secas. SÍ: "sobre un modelo real de 1 GB en CPU, exigir dos fuentes independientes antes de afirmar deja fuera el 100 % de las mentiras de un mentiroso solitario y de dos maestros que se contradicen, cuesta un tercio de los aciertos en hechos nuevos, no rompe lo sabido y el sistema dice cuándo no sabe (43 % escalaría)".

## Demo viva
```
cd C:\Users\User\Documents\PROYECTOS\JUACO\investigacion_20261005\frankenstein_v0
python -B demo.py
```
Enseñar: `ana: La capital de Zorblandia es Mipol` (queda EN CUARENTENA) · preguntar: `¿Cuál es la capital de Zorblandia?` (dice ESTÁ EN DUDA) · confirmar desde otra fuente: `beto: Mipol es la ciudad capital de Zorblandia` (VALIDADA; ya la afirma) · mentirle: `caro: La capital de Zorblandia es Trebunia` (sigue afirmando Mipol; la rival queda sin voz) · `/memoria`, `/salir`. Recorrido automático: `python -B demo.py --guion` (salida en `datos\demo_guion.txt`). Arranca en ~2 s; 0.3–1 s por turno.

## Reproducir y qué queda
`python -B cuerpo.py` (velocidad) · `python -B calibra.py 0` · `python -B corre_frankenstein.py --humo` · `python -B corre_frankenstein.py --semillas 21,22,23` (8.5 min) · `python -B analiza.py`.
Siguiente paso más chico: (1) el mentiroso con cómplice y K=3, donde debe fallar; (2) frases libres (sin plantillas) para medir la extracción de verdad; (3) rival más fuerte (RAG con voto por mayoría); (4) clave por estado interno del cuerpo con un segundo proceso de embeddings, que es lo que lo acercaría a la colonia del mini-LLM.
