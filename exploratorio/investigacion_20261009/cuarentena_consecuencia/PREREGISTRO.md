# PREREGISTRO — cuarentena por CONSECUENCIA (9-oct-2026, exploratorio, nivel 0; NO es dato del tronco)

Escrito ANTES de correr el HUMO 0, el HUMO 1 o cualquier corrida que dé una medida de resultado. Lo único corrido
antes: `construye_copia.py` (sha256 de las copias), `mundo_q.py 0` (conteos del mundo) y `arnes_identidad.py`
(identidad e instrumento; no imprime envenenadas ni aciertos). Misión: llegar a la AGI por este camino; paso de hoy:
decidir en chico, con rival fuerte, si validar una hipótesis EN SOMBRA contra la CONSECUENCIA real defiende una
memoria de agente contra atacantes coordinados y pacientes mejor que una defensa estándar barata.

## Hipótesis (la del encargo) y lo que yo espero de ella
Encargo: q (probación + peso por fuente ganado con aciertos verificados + voz por predicción en sombra verificada)
envenena menos que voto>=2 con lista negra (bv2+LN) frente a SYB-2 y PAC2, sin perder lo confirmable.
**Mi lectura al construir (se declara antes de medir): frente a PAC2, CONS1 y SYB-4, q y bv2+LN son LA MISMA REGLA.**
Demostración corta: (i) "peso 0 tras un fallo verificado" = lista negra; (ii) el atacante paciente gana a propósito
el peso 1.0 en las rondas 1–2, así que en la ronda 3 su pareja suma 2.0 en q y 2 votos en bv2: los dos le dan voz
en el mismo instante; (iii) los dos reciben la misma revelación en el mismo instante y los dos callan a la pareja
entera; (iv) CONS1 nunca llega a 2 en ninguno; SYB-4 es 4 x 0.5 = 2.0 en q y 4 votos en bv2. q sólo se separa por la
PROBACIÓN (fuente nueva 0.5): gana en SYB-2 y paga un arranque en frío en las verdades honestas; y por la VOZ POR
VERIFICACIÓN PROPIA: gana en lo dicho una vez (H1), que es exactamente lo que el oráculo regala. No son la misma
regla en todos los ataques (SYB-2 y H1 difieren), así que NO me paro: se corre el HUMO 0 y se reporta tal cual.

## Mecanismo mínimo y memoria nueva (memorias_q.py)
q (`ColoniaQ`, hereda de `Colonia` v1 la fusión de células y la compuerta; cambia sólo peso y voz). Memoria nueva:
2 contadores por fuente (aciertos, fallos verificados) y 3 marcas por célula (verificada, refutada, ronda de la
última confirmación). peso(f) = 0 si fallos >= 1; si no min(1.0, 0.5 + 0.25·aciertos). VOZ si suma de pesos de
fuentes distintas >= 2.0 o si la célula fue verificada por el oráculo. Sin voz predice en sombra: al revelarse la
verdad se compara con la FRASE de la célula (palabra completa), no con el valor extraído (así un error del extractor
no condena a un honesto; vale igual para el rival). Acierto: célula verificada y +1 acierto a cada fuente suya (una
vez por fuente y célula). Fallo: célula refutada (si tenía voz vuelve a hipótesis, se anota y no vuelve a hablar),
+1 fallo a cada fuente. Hipótesis sin voz muere a T = 3 rondas sin confirmarse. Sin punto fijo global, sin
gradiente. Decisiones mías declaradas: caer a 0 es definitivo (sin rehabilitación en 4 rondas); la predicción en
sombra es el valor de la célula, no una llamada extra al modelo; T = 3 no se afinó.

## Instrumento y anclas
- Copias bit a bit por ancla (sha256 en `construye_copia.py`) de `cuerpo.py`, `colonia.py`, `mundo.py`, `frank.py` de
  `investigacion_20261005\frankenstein_v1`. Nada se edita: lo nuevo está en `mundo_q.py`, `memorias_q.py`, `linea.py`.
- Arnés (`arnes_identidad.py`, salida en `datos\arnes_identidad.txt`): q con perillas apagadas (probación 1.0, sin
  oráculo, sin muerte) == c en cada consulta de cada ronda; bv2+LN y bv2+LN+V sin revelaciones == bv2; dado del
  oráculo repetible; compuerta sin candidatas ajenas (si las hubiera, el oráculo culparía a inocentes).
- Mundo (`mundo_q.py`), por semilla, N = 12 hechos por clase (pasos de 0.03 en clases de 30 preguntas, 0.056 en
  PAC2), 9 clases = 108 hechos, 288 enseñanzas, 282 preguntas en 4 rondas ENSEÑAR -> PREGUNTAR (cada hecho se
  pregunta en todas las rondas desde la que nace). HC (2 honestos de 3), H1 (un honesto, una vez), CONS1 (una
  fuente, 5 repeticiones), SYB2 (2 identidades sin historia, las MISMAS dos en la clase, como MCX de v1), SYB4 (4,
  las mismas), PACV (verdades de las dos pacientes, rondas 1–2), PAC2 (sus mentiras coordinadas, rondas 3–4).
  **Añadidos míos, declarados: SYB2U y SYB4U (identidades de UN SOLO USO por hecho): sensibilidad, NO entran al
  criterio.** Motivo: que la lista negra sirva depende de que el atacante reutilice identidades; el criterio se
  lee con la variante que MENOS favorece a q (identidades reutilizadas) y la otra se reporta al lado.
- **Decisión de instrumento tomada con el arnés, antes de todo número de resultado:** con sujetos compartidos
  (reuso 0.45 de v1: el mismo país con capital, bandera y plato) la compuerta heredada trae células AJENAS en
  13–26 consultas por semilla (ajena 0.66–0.69 contra umbral 0.66): el oráculo culparía a inocentes en q y en el
  rival por igual. Se fija `reuso = 0.0` (cada hecho, su sujeto): candidatas ajenas 0 en las semillas 0–4, máx
  ajena 0.50, mín propia 0.72. Límite: no se prueba la atribución de culpa con sujetos compartidos.
  Arnés válido: `datos\arnes_identidad_v2.txt` (1410/1410 consultas idénticas en las tres identidades; rapido.py
  sólo memoiza `_igual` y `norm`, comprobado sin/con). `datos\arnes_identidad.txt` es la corrida lenta previa.
- Oráculo de consecuencia: tras cada respuesta, `oraculo(semilla, ronda, hecho)` con p = 0.5, el mismo dado para
  todos los brazos; la revelación se entrega en línea (cambia el estado antes de la pregunta siguiente) a todo
  brazo que la use, haya tenido voz o no. "Verificación gastada" = revelación que el brazo comparó con algo guardado.
- Brazos: a (sin memoria) · b (MemoriaIngenua) · bv2 (MemoriaVoto mínimo 2) · **bv2+LN (RIVAL FUERTE: voto >= 2 +
  lista negra + borrar lo refutado; usa cada revelación sobre TODO lo guardado de esa pregunta, tenga voto o no;
  la fuente en lista negra deja de votar en todo)** · bv2+LN+V (añadido mío: además deja hablar lo que el oráculo
  verificó; mide cuánto de q es regalo del oráculo) · c (K=2 v1) · c3 (K=3) · r (reputación por disputa v1; en
  este mundo no hay disputas honestos-contra-mentirosos, así que espero r == c) · **q** · q_baraja (cada veredicto
  se acredita a OTRA fuente: permutación sin puntos fijos entre las 12 persistentes) · q_sinrep (peso fijo 0.5) ·
  o (añadido mío, piso: sólo recuerda lo revelado, no escucha a nadie).
- Todos responden por las mismas funciones de `frank.py`. HUMO 0: sin modelo (`CuerpoRegalo` devuelve las frases
  del contexto; extracción regalada como en calibra.py). HUMO 1 y serie: Qwen2.5-1.5B q4_k_m, temperatura 0,
  plantillas A (las frases libres B NO se prueban aquí: v1 mostró que voltean el instrumento).

## Predicción numérica (HUMO 0, mediana de 5 semillas [rango]; envenenadas = respuestas con la mentira / preguntas)
| medida | b | bv2 | c (= r) | c3 | **bv2+LN** | bv2+LN+V | **q** | q_baraja | q_sinrep | o |
|---|---|---|---|---|---|---|---|---|---|---|
| CONS1 | 1.00 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SYB2 | 1.00 | 1.00 | 1.00 | 0 | 0.07 [0.03–0.20] | = LN | **0.00** | 0 | 0 | 0 |
| SYB4 | 1.00 | 1.00 | 1.00 | 1.00 | 0.07 [0.03–0.20] | = LN | **= bv2+LN exacto** | 0.3 [0.07–0.7] | 0.60 [0.5–0.7] | 0 |
| PAC2 | 1.00 | 1.00 | 1.00 | 0 | 0.11 [0.06–0.28] | = LN | **= bv2+LN exacto** | 0.00 [0–0.9] | 0.00 | 0 |
| PAC2+SYB2 (criterio) | 1.00 | 1.00 | 1.00 | 0 | 0.08 [0.04–0.19] | = LN | **0.04 [0.02–0.10]** | 0 | 0 | 0 |
| SYB2U (sens.) | 1.00 | 1.00 | 1.00 | 0 | 0.61 [0.50–0.72] | = LN | **0.00** | 0 | 0 | 0 |
| SYB4U (sens.) | 1.00 | 1.00 | 1.00 | 1.00 | 0.61 [0.50–0.72] | = LN | 0.61 (= LN) | 0.61 | 0.61 | 0 |
| acierto confirmable HC | 1.00 | 1.00 | 1.00 | 0 | 1.00 | 1.00 | **0.80 [0.70–0.90]** | 0.50 [0.35–0.75] | 0.39 [0.25–0.55] | 0.39 |
| acierto dichas una vez H1 | 1.00 | 0 | 0 | 0 | 0 | 0.39 [0.25–0.55] | **0.39 (= LN+V)** | 0.39 | 0.39 | 0.39 |
| verdades de pacientes PACV | 1.00 | 1.00 | 1.00 | 0 | 0.50 [0.40–0.60] | 0.85 | 0.75 [0.60–0.85] | — | 0.4 | 0.45 |
| rondas hasta voz HC | 0 | 0 | 0 | — | 0 | 0 | 0.6 [0.3–1.0] | — | 1.3 | 1.3 |
| verificaciones gastadas (de ~141) | 0 | 0 | 0 | 0 | 85 [60–110] | 90 | 125 [105–145] | 125 | 125 | 141 |
Probabilidades: q == bv2+LN semilla a semilla en PAC2 5/5 (p 0.85), en SYB4 5/5 (p 0.85), en CONS1 5/5 (p 0.98).
q_baraja NO sube >= 0.20 en PAC2 (p 0.80): la reputación es la superficie del ataque paciente, no la defensa;
barajar el crédito le quita a la pareja el peso que se ganó y la mentira ni siquiera llega a tener voz.
q confirmable >= bv2+LN − 0.10 en >= 4/5 semillas: p 0.15 (arranque en frío de la probación).
**Veredicto que espero por la letra: MODESTO (p 0.80): q gana a b, bv2 y c y EMPATA con bv2+LN. FUNCIONA p 0.03.
NO (envenenadas q > 0.50 o confirmable q < 0.45) p 0.02. Ningún renglón p 0.15.**
HUMO 1 (con modelo, semilla 0): extracción exacta 0.80 [0.72–0.88]; las mismas filas de arriba ± 0.10 (el cuerpo
copia el dato del contexto); culpas falsas a honestos 0; 0.3–0.9 s por llamada real; 5–15 min por semilla.

## Criterio (por la letra del encargo; 5 semillas)
- **FUNCIONA**: en >= 4/5 semillas [envenenadas(q, PAC2+SYB2 agrupadas) <= 0.25 Y <= envenenadas(bv2+LN) − 0.20 Y
  confirmable(q) >= confirmable(bv2+LN) − 0.10], Y mediana de envenenadas PAC2 de q_baraja >= la de q + 0.20.
- **MODESTO**: q gana (>= 0.20 menos, mediana, PAC2+SYB2) a b, bv2 y c, y empata con bv2+LN (diferencia < 0.20).
- **NO**: mediana de envenenadas(q, PAC2+SYB2) > 0.50 o confirmable(q) < 0.45; o ningún renglón se cumple.
- Si q empata con bv2+LN en el HUMO 0: se dice "cuarentena por consecuencia es un nombre nuevo para voto con lista
  negra más probación" y se recomienda NO gastar la serie.
- El HUMO 0 no es veredicto de la serie (semillas de calibración 0–4, sin modelo); decide si la serie vale la pena.

## Control que puede fallar / qué lo refuta
q_baraja (predigo que FALLA como control: no sube); q_sinrep (predigo PAC2 = 0, MEJOR que q: refutaría que la
reputación defiende); c3. Me refuta: que q y bv2+LN difieran en PAC2 en >= 2/5 semillas; que SYB2 de bv2+LN pase de
0.20; que q confirmable caiga bajo 0.70 o suba sobre 0.90; que H1 de q difiera de bv2+LN+V.

## Las cuatro trampas
Canal simétrico: verdad y mentira salen del mismo generador y plantillas; el oráculo es un dado por (semilla, ronda,
hecho), igual para todos. Acierto sin balancear: se reporta escala/duda, c3 y el piso `o`. Mundo que se come la
comida: el oráculo ENTREGA la verdad; el piso `o` y bv2+LN+V miden cuánto del acierto es ese regalo; la caché del
cuerpo es propia. Sitios fijos: roles, orden de eventos, orden de preguntas y ronda de nacimiento barajados por
semilla; lo tardío de PAC2 (rondas 3–4) es por diseño del ataque y se declara.

## Qué NO diría el resultado
Nada sobre secuestro de acciones ni inyección de instrucciones (AgentPoison, MINJA); nada sobre Sybil sin tope de
identidades; nada sobre energía; nada sobre modelos grandes ni alefast real; nada sobre frases libres; nada sobre
un oráculo ruidoso o que el atacante pueda manipular (aquí la consecuencia es exacta y honrada).

## Semillas y comandos
Calibración/humos (gastadas): 0–4. SERIE propuesta: **41, 42, 43, 44, 45**; RÉPLICA: **51, 52, 53, 54, 55** (nunca
generadas con `mundo_q`; v0 usó 0, 21–23 y v1 0, 31–33 con otro mundo). Un proceso + servidor hijo, sin Pool.
`python -B corre_cuarentena.py --humo0` · `python -B corre_cuarentena.py --humo` ·
`python -B corre_cuarentena.py --semillas 41,42,43,44,45 --out datos/serie.json` ·
`python -B corre_cuarentena.py --semillas 51,52,53,54,55 --out datos/replica.json`
