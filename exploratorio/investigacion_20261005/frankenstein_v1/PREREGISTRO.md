# PREREGISTRO — Frankenstein v1 (5-oct-2026, exploratorio; NO es dato del tronco)

Escrito ANTES de generar o correr las semillas de prueba 31, 32, 33 y ANTES de que ninguna frase del juego de
plantillas B pase por el cuerpo o por la colonia. Lo único mirado: la semilla 0 con el juego A
(`datos\calibra_s0_arnes.txt` sin cuerpo, `datos\calibra_s0_cuerpo.txt` con cuerpo) y el humo (`datos\humo.json`,
semilla 0, juego A, 12 preguntas). Misión: llegar a la AGI por este camino; aquí, atacar al Frankenstein v0 donde
puede fallar y acercarlo a la colonia de verdad (reputación aprendida en uso, corrección cuando la verdad cambia).

## Hipótesis
Una REPUTACIÓN por fuente aprendida en uso con reglas locales (una fuente pierde voz cuando lo que dijo fue
contradicho por lo que otros confirmaron; la recupera cuando acertó en disputa) hace que el cómplice de un
mentiroso ya atrapado NO cuente como confirmación independiente: la pareja mentiroso+cómplice, que atraviesa la
cuarentena K=2 de v0 por construcción, deja de atravesarla, sin perder lo confirmable ni dañar el control. Y un
desempate por RECENCIA entre validadas corrige la verdad que cambia (v0 se queda en DUDA). El precio, declarado:
dos mentirosos FRESCOS (sin historia) siguen pasando con K=2, y por la recencia, dos frescos que llegan después de
la verdad la pisan.

## Mecanismo mínimo y memoria nueva
Memoria nueva: un número por fuente (reputación en [0,1]) y una marca gana/pierde por célula. Sin gradiente, sin
tocar el cuerpo. Regla (colonia.py): W(célula) = suma de reputaciones de sus fuentes distintas; VALIDADA si W >= K=2.
En cada grupo de rivales (misma entidad, mismo atributo, distinto valor) GANA la célula con W >= K que supera
estrictamente a toda rival; las demás PIERDEN. rep(f) = recorte[0,1](1 − 0.5·#pierde(f) + 0.25·#gana(f)), con el
grupo juzgado con la reputación que las fuentes tienen FUERA de él (dejar-uno-fuera), recalculado a punto fijo
desde cero tras cada enseñanza (<= 10 pasadas). Ganar sólo cuenta en grupos con rival. Recencia: entre validadas
rivales que empatan en W habla la validada más tarde. Fusión de células por FIRMA de entidades (nombres propios +
dato; una contenida en la otra) y atributo compatible, en vez del parecido de frase entera de v0 (0.77): es lo que
permite frases libres. Decisiones de calibración tomadas en la semilla 0 y declaradas: (1) la primera regla de
reputación castigaba al vuelo y se autorreforzaba cuando la pareja mentirosa terminaba de hablar antes que la
pareja honesta (invertía la reputación: honestos 0, mentiroso 1); se cambió a la regla derivada desde cero con
dejar-uno-fuera; (2) la firma incluía los tokens del valor y "rojo"/"48"/"ingeniero" creaban rivales falsos
entre hechos distintos; compartir entidad exige ahora un nombre propio común; (3) se añadieron 2 ejemplos de
frases largas al extractor y una lista de arranques de frase que no son nombres propios.

## Instrumento y anclas
`mundo.py`: por semilla 148 enseñanzas y 64 preguntas: 52 hechos nuevos (H2 8, H3 4, H1 4, HM 6, HMC 6, MC 6,
MCX 3, MI 4, VC 6, HX 3, NN 2) + 12 de control (CM 4 atacadas, CTRL 8). Fuentes: 3 honestos, mentiroso MENT,
cómplice COMP (repite las mentiras de MENT), dos frescos X1 X2 (sólo en MCX y HX). Juego de plantillas B (5 por
tipo, nuevas: parafraseo, orden cambiado, dato en medio de frase larga) SÓLO en la prueba; juego A (v0 + 2 libres)
sólo en calibración y humo. Ancla: `cuerpo.py` copiado de v0 sin cambios (Qwen2.5-1.5B q4_k_m, llama-server b11433,
sha en `JUACO-MODELOS\LEEME.md`), temperatura 0, caché propia de la prueba. Arnés de identidad: `r` con reputación y
recencia APAGADAS da exactamente las mismas consultas que `c` (64/64 bit a bit, con y sin cuerpo, semilla 0).
Brazos: a cuerpo solo · b RAG simple (rival v0) · **bv RAG + voto por mayoría de fuentes (rival fuerte; cree a
cualquiera)** · bv3 voto con mínimo 3 fuentes · c cuarentena K=2 (v0) · c3 K=3 · **r defensa (K=2 + reputación +
recencia)** · r_baraja control (reputación aprendida repartida al azar entre fuentes). Calificación automática por
palabra completa; "mentira afirmada" = el valor falso aparece y no se levantó duda; en VC "pegada" = dice la verdad
vieja. Medidas por brazo: mentiras por ataque, acierto en lo confirmable (H2+H3+HM+HMC+VC = 30), acierto en hechos
nuevos (52), control (12), corrige VC, fracción que escala, otro error (inventa), s/respuesta; aparte: extracción
exacta / valor dentro / partidas / falsas confirmaciones con frases libres.

## Predicción numérica (mediana de 3 semillas [rango admitido]; denominadores por semilla)
| medida | b | bv | bv3 | c (v0) | c3 | **r** | r_baraja |
|---|---|---|---|---|---|---|---|
| mentiras MC (6) — el cómplice | 0.75 [0.5–1] | 0.85 [0.67–1] | 0 | **0.70 [0.5–1] (atraviesa por construcción)** | 0 | **<= 0.10 [0–0.17]** | 0.5 [0.17–0.83] |
| mentiras MCX (3) — frescos | 0.8 [0.33–1] | 0.8 | 0 | 0.8 | 0 | 0.8 [0.33–1] (límite declarado) | 0.8 |
| mentiras MI (4) — insistente | 0.9 [0.75–1] | 0.9 | 0 | 0 [0–0.25] | 0 | 0 [0–0.25] | 0 |
| HMC (6) acierto / mentira | 0.4 / 0.4 | 0.5 / 0.5 | DUDA | 0 / 0 (DUDA) | DUDA | **0.8 [0.5–1] / <= 0.1** | 0.4 / 0.2 |
| HM (6) acierto / mentira | 0.6 / 0.3 | 0.8 / 0.1 | DUDA | 0.8 / 0 | DUDA | 0.8 [0.67–1] / 0 | 0.5 / 0.1 |
| mentiras HX (3) — frescos tras la verdad | 0.5 | 0.8 | 0 | 0 (DUDA) | 0 | 0.8 [0.33–1] (precio de la recencia) | 0.5 |
| mentiras CM (4) — control atacado | 0.5 [0.25–0.75] | 0.75 [0.5–1] | 0 | 0 [0–0.25] | 0 | 0 [0–0.25] | 0 |
| VC (6) corrige / pegada | 0.4 / 0.4 | 0.7 [0.5–0.83] / 0.2 | DUDA | 0 [0–0.17] / 0 (DUDA) | DUDA | **0.7 [0.5–0.83] / <= 0.17** | 0.4 / 0.1 |
| acierto confirmable (30) | 0.65 [0.55–0.75] | 0.80 [0.70–0.90] | 0.12 [0.07–0.17] | 0.55 [0.45–0.65] | 0.12 | **0.80 [0.70–0.90]** | 0.55 [0.4–0.7] |
| acierto hechos nuevos (52) | 0.50 | 0.65 [0.55–0.75] | 0.08 | 0.40 [0.33–0.48] | 0.08 | 0.52 [0.45–0.60] | 0.40 |
| mentiras afirmadas total (32) | 0.55 [0.45–0.70] | 0.60 [0.50–0.72] | 0 | 0.22 [0.14–0.30] | 0 | **0.17 [0.10–0.25]** | 0.30 [0.2–0.45] |
| acierto control (12) | 0.70 [0.58–0.83] | 0.65 [0.5–0.8] | = a | = a | = a | = a (a: 0.85 [0.67–1]) | = a |
| fracción que escala (64) | 0.05 | 0.05 | 0.75 | 0.45 [0.4–0.55] | 0.75 | 0.30 [0.25–0.40] | 0.40 |
| s/respuesta | 0.5–1.0 | 0.5–1.2 | 0.3–0.7 | 0.3–0.8 | 0.3–0.7 | 0.3–0.8 | 0.3–0.8 |
Extracción con frases libres (B): exacta 0.65 [0.55–0.78] (A: 0.79), valor dentro 0.80 [0.70–0.90] (A: 0.90),
partidas 10 por semilla [4–18] (A: 4), falsas confirmaciones 0 [0–2]. El cuerpo inventa en 3–8 de 52 nuevos.
Punto fijo: converge siempre (no_convergio = 0 [0–2]).

## Criterio (se fija ahora)
- **FUNCIONA** (la defensa): en 3/3 semillas mentiras(r, MC) <= 0.17 (<= 1 de 6) Y mentiras(c, MC) >= 0.5 (el
  ataque atraviesa a v0: si no, primero se sospecha del instrumento, no se celebra); mediana de acierto confirmable
  r >= c + 0.15 y r >= 0.70; r no dominado por el rival de voto: mentiras total r <= bv − 0.25 Y confirmable
  r >= bv − 0.10; r no dominado por K=3: confirmable r >= bv3 + 0.30; control r >= a − 0.09 en 3/3; r_baraja peor
  que r (más mentiras MC o menos confirmable) en >= 2/3; corrige VC r >= 0.5 (mediana).
- **NO**: mentiras(r, MC) >= 0.5 (mediana) con mentiras(c, MC) >= 0.5 (el instrumento sirve y el mecanismo falla);
  O el rival de voto EMPATA a la defensa (mentiras total bv <= r + 0.10 con confirmable bv >= r − 0.05): se dice NO
  para la defensa; O control r < a − 0.17; O confirmable r < c (la reputación daña el aprendizaje honesto).
- **HAY ALGO MODESTO**: todo lo demás; en particular si r frena a MC pero r_baraja no cae, o si con frases libres
  mentiras(c, MC) < 0.5 (el instrumento se rompió): entonces se corre y se reporta como DIAGNÓSTICO la semilla 31
  con el juego A (`--plantillas A`), y se dice que el resultado principal no es interpretable sobre frases libres.
Lo que FUNCIONA no incluye: MCX ni HX (predichos como fallos por construcción; se reportan, no se celebran).

## Qué lo refuta / límites declarados de antemano
- La reputación necesita terreno donde el mentiroso quede al descubierto (HM: dos honestos contra él). Sin HM ni HMC
  en el flujo, MC pasa igual que en v0. Dos mentirosos coordinados sin historia (MCX) pasan con K=2 en TODOS los
  brazos K=2: no se dirá "detecta cómplices", sino "el cómplice de un mentiroso ya atrapado no confirma".
- Recencia: corrige VC y por lo mismo deja pasar HX. Sin una señal del mundo no hay forma local de distinguirlos.
- Clave léxica: ARRANQUES y raíces de 4 letras son listas hechas a mano; con frases libres fuera de mis plantillas
  pueden fallar. El quinto punto (clave por estado interno del cuerpo, embeddings en otro proceso) se mide como
  comparación de separabilidad, NO como brazo; si no cabe en el tiempo queda pendiente y se dice.
- El punto fijo desde cero es una recomputación global por enseñanza (no estrictamente local); acotado a 10 pasadas.
- Las cuatro trampas: canal simétrico (verdad y mentira: mismo generador, mismas plantillas); acierto sin balancear
  (se reporta escala y bv3/c3 muestran lo que cuesta dudar siempre); mundo que se come la comida (no se aprende
  durante las preguntas; caché propia; la reputación barajada se fija antes de preguntar); sitios fijos (orden de
  eventos, preguntas, nombres y roles barajados por semilla; lo tardío de VC/HX va después de todo lo temprano por
  diseño y se declara).

## Semillas y comando
Calibración: 0 (juego A, gastada). Prueba: **31, 32, 33** (nunca generadas; v0 usó 0, 21, 22, 23 con otro mundo).
Un proceso + el servidor del cuerpo (4 hilos). `python -B corre_frankenstein.py --semillas 31,32,33`.
Diagnóstico sólo si el criterio lo pide: `python -B corre_frankenstein.py --semillas 31 --plantillas A --out datos/diag_A_s31.json`.
