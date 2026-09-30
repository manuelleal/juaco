# PREREGISTRO — grande: MUNDO MÁS GRANDE Y CON MÁS COSAS (EXPLORATORIO)

> Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
> controles y réplicas). Encargo del director, 30-sep-2026. **Historia del texto (corregida tras la auditoría):** la versión
> sha `aa3158bd5748d0b7` (la que registra el log del humo) se escribió ANTES del humo, pero DESPUÉS de una prueba de cañería de un
> proceso en G 2 (O1 ×9, T 1500, s 718085: sólo tiempo, L/nobj y los contadores de un linaje; ningún cruce ni R0) y del arnés
> (mundo G 1, T 3000). No es "antes de cualquier dato". Tras el humo se editaron: la sec. 2 ("costo medido en el humo"), la
> sec. 5bis (ERR-157) y, tras la auditoría, esta nota, la nota de la sec. 4, la sec. 5bis ampliada (H-2) y la sec. 5ter.
> Estado: **EXPLORATORIO**. No decide tronco ni nivel; su lectura propone (o no) un confirmatorio con semillas nuevas.

## 1. Pregunta
¿El orden **O1 > termo > v143** (linajes que cruzan R0 real ≥ 0.9, ENMIENDA 5) se mantiene en un mundo más grande y con más cosas,
y cuánto margen le queda a O1 allí (qué falla)?

## 2. Mundo (`pista_grande.py`, por anclas desde `carrera_escuderias/pista.py` sha `9f47c65e438e0ff4`; `juez.py` `6a68f640a7832f12`)
- **G = 2**: anillo L = 720 (el de la carrera es 360), 72 objetos, 18 sorteos de olvido por paso: **la misma densidad** (0.1 objeto
  por celda) y la misma tasa de olvido por objeto. 9 linajes iguales, fundador limpio, T = 100 000, pizarra 1: la tarea es
  `corre_v143.tarea` sin tocar (regla 14).
- **Costo medido en el humo** (línea EDITADA TRAS EL HUMO) (1 proceso, T 20 000, G 2): o1 91.8 s, termo 31.7 s, v143 28.8 s, pc 30.1 s, o1liso 86.9 s, o1pas 93.5 s
  (366 s las 6). Proyección a T 100 000 con pool 4: 25 corridas ≈ 28 min; 30 con o1pas ≈ 38 min (dentro de los 45).
- **Por qué G = 2 y no 3 (costo):** el costo por paso crece con el número de objetos (cada carro recorre todos). Medido en el arnés:
  O1 ×9, T 1500, G 1 → 3.1 s, G 2 con cosas → 8.4 s (×2.3). Con los tiempos del humo de patas_muro (T 20k: O1 32 s, termo 17 s,
  pc 22 s) la exploración en G 2 cuesta ≈ 25 corridas × 3–6 min / 4 procesos ≈ 25–35 min; en G 3 pasaría de 45 min.
- **Confusión declarada:** misma densidad por celda pero, con los mismos 9 linajes, **cada linaje tiene el doble de objetos y de
  anillo**: el mundo puede ser más fácil por menos competencia o más difícil por más distancia. El brazo **o1liso** (G 2 sin cosas
  nuevas) separa el tamaño de las cosas.
- **Oasis (comida RICA, rica = 1):** un arco de 72 celdas (10 %). A o C mordidas DENTRO dan (+0.8, +0.8) (su efecto + 0.8 en la otra
  necesidad). Sólo existe allí. El spawn no cambia (ni un sorteo de más): el oasis tiene la densidad y la composición del resto.
- **Pantano (VENENO LENTO, lento = 1):** un arco de 72 celdas en el lado opuesto (inicio + 360). A o C mordidas DENTRO dan su efecto
  nominal inmediato y dejan una CARGA: −0.0025 E por paso durante 400 pasos (total −1.0 E; acumulable). A del pantano neto −0.2 E;
  C del pantano +0.8 Ag y −1.0 E. La carga es del cuerpo (muere con él).
- **Canal:** las mismas letras A B C D (ninguna letra nueva: ningún carro necesita un patrón de retina inventado); `resultado()`
  devuelve el dS que el cuerpo recibió EN ESE PASO (oasis: el doble; pantano: el nominal; la carga no se anuncia, se siente en E).
  Nadie recibe la posición de las zonas.
- **Zonas:** inicio sorteado por semilla con una rng nueva `[seed, 0, 18, 0]` (pista 11–15, pista_pob 16–17): no toca ninguna
  corriente de la pista y no son sitios fijos entre semillas.

## 3. Brazos (carros por sha, sin tocar)
| brazo | carro | archivo (sha) | mundo |
|---|---|---|---|
| o1 | O1 | carrera_escuderias/carros/O1.py (`99436afa2715f028`) | grande |
| termo | V143_TERMO | organelos/termo/carros/V143_TERMO.py (`3db639cab75641fb`) | grande |
| v143 | V143 | tronco_v14_3/carros_v143/V143.py (`2a03048a7f1525e5`) | grande |
| pc | TPATAS, PATAS = 3 (UTIL+CEDE) | organelos/dinamita/carros/TPATAS.py (`1b6272ef4616af8b`) | grande |
| o1liso | O1 | (el mismo) | G 2 sin oasis ni pantano |
| o1pas (OPCIONAL) | O1_PAS de la parte A, sigma 0.03 | organelos/o1_evo/carros/O1_PAS.py (`c5377ada6b28bee0`) | grande |

o1pas sólo corre con `--siembra <ruta>` (carpeta de la parte A con `cadena_i*_o1pas.json`, un `cadena_*.json`, una lista de genomas o
el `resumen.json` de o1_evo). La semilla j usa la siembra de la cadena j mod (número de cadenas). Si la parte A cambia O1_PAS.py tras su
auditoría, el coordinador actualiza `SHA_O1PAS` en `corre_grande.py` y esta línea ANTES de correr (sin eso, `--siembra` aborta).

## 4. Predicciones (5 semillas × 9 linajes = 45)
P1–P7 están, con estos mismos números, en la versión `aa3158bd5748d0b7`, escrita ANTES del humo (su sha figura en la cabecera del log
del humo). Ninguna se escribió ni se movió tras el humo; en particular P2 (22–40) y P4 (−3 a +10) se fijaron antes de ver que en el humo
o1 cruzó 1/9 y o1liso tuvo 7/9 casi inmortales. Lo único agregado después es la reserva de P4 (sec. 5bis, H-2), que no cambia su rango.

| id | predicción | p |
|---|---|---|
| P1 | **el orden se mantiene**: suma que cruza o1 > termo > v143 (estricto) | 0.65 |
| P2 | o1 cruza entre 22 y 40 de 45 | 0.60 |
| P3 | o1 con mayoría que cruza (≥ 5/9) en ≥ 3 de 5 semillas | 0.65 |
| P4 | o1liso − o1 entre −3 y +10 (las cosas nuevas, en neto, no ayudan a O1: no sabe dónde está el oasis y muerde el pantano) | 0.60 |
| P5 | **nadie usa el oasis**: pasos en el oasis / 0.10 entre 0.7 y 1.4 en todos los brazos del mundo grande | 0.80 |
| P6 | **nadie evita el pantano**: (A+C mordidas en el pantano / A+C mordidas) / 0.10 entre 0.6 y 1.4 en todos | 0.80 |
| P7 | pc ≈ termo: \|suma pc − suma termo\| ≤ 6 | 0.60 |

Descriptivo sin predicción: fracción de muertes con carga activa, drenado, causas, fundadores, mordidas B+D, A+C del mundo; o1pas − o1.

## 5. Lectura por código (`corre_grande.lee`)
- **Validez** (si falla alguna: NO SE LEE): V1 completa (5 semillas × brazos, sin abortos, contabilidad coherente y t_fund
  reconstruible); V2 las cosas actúan en cada corrida del mundo grande (mordidas A+C en el oasis > 0 y cargas > 0); V2b o1liso sin
  zonas; V3 estado (carro, PATAS, mundo) por corrida; V4 L = 720 y 72 objetos; V5 (sólo o1pas) todos sus fundadores salen de la siembra.
- **L1 (principal):** ORDEN SE MANTIENE si suma(o1) > suma(termo) > suma(v143); si no, ORDEN NO SE MANTIENE (y qué par se invierte).
- L2 pareados por semilla o1–termo y termo–v143 (gana/empata/pierde; empates en contra). L3 margen de O1 (45 − suma, mayorías).
  L4 o1liso − o1. L5 oasis (razón de pasos y de mordidas A+C contra 0.10). L6 pantano (razón de mordidas, muertes con carga,
  drenado). L7 pc − termo. L8 (opcional) o1pas − o1.
- Predicciones P1–P7 evaluadas por código (sólo cuentan con 45 linajes; el humo no cuenta).

## 5bis. Reserva por casi inmortales (escrita TRAS EL HUMO y ANTES de la exploración; ERR-157, sec. 5ter)
El humo (T 20 000, s 718090) mostró que en G 2 **sin cosas** 7 de 9 linajes de O1 no llegan a 5 muertes (casi inmortales): la letra
de la ENMIENDA 5 no los ve (ni cruzan ni fallan). Un mundo más fácil puede así "bajar" a O1 por la letra sin que O1 empeore. No se
cambia L1 ni ninguna predicción; se agrega: `casi_inmortales` por brazo, `L1b` = cruzan + casi inmortales (descriptivo), y la lectura
lleva "CON RESERVA" si o1, termo o v143 tiene ≥ 10 de 45 casi inmortales. Nada de esto cambia qué corridas se hacen.

**H-2 (auditoría, antes de datos de la exploración):** L4 y P4 llevan "CON RESERVA" si o1liso tiene ≥ 10 de 45 casi inmortales
(`reserva_inmortales_o1liso`, `P4_con_reserva`).

## 5ter. ERR-157 (abierto aquí; el siguiente libre es ERR-158)
- **Fecha:** 29/30-sep-2026, antes de cualquier corrida de la exploración (718001–718005).
- **Qué cambió:** la sec. 5bis (reserva por casi inmortales: columna `casi_inmortales`, L1b, marca "CON RESERVA" con ≥ 10/45 en
  o1, termo o v143) se escribió DESPUÉS del humo, motivada por él (o1liso 7/9 casi inmortales en T 20 000). Tras la auditoría se
  agregó la misma reserva para L4/P4 sobre o1liso (H-2) y el candado de siembra en `--reanuda` (H-4, no toca la lectura).
  L1 y P1–P7 no cambian.
- **Efecto contrafáctico en el humo:** con el umbral escalado a 9 linajes (≥ 2/9), la reserva NO habría disparado para o1 (1/9),
  termo (0/9) ni v143 (0/9): la lectura del humo es la misma. Sí dispara para o1liso (7/9): H-2 marca L4/P4 en el humo.

## 6. Qué refuta, qué sigue
- P1 falsa refuta "el orden de la carrera es robusto al mundo". P5/P6 falsas (alguien usa el oasis o evita el pantano sin memoria de
  lugar) obligan a buscar el canal antes de leer nada más (posible fuga).
- Exploratorio: sin réplica automática. Si L1 o L4 dan algo lejos de lo predicho, el coordinador puede proponer un confirmatorio
  con semillas nuevas y letra propia. Cambiar esta lectura después del humo se paga con ERR (ERR-157 ya usado, sec. 5ter; siguiente libre: ERR-158).

## 7. Cuatro trampas
1. Canal social simétrico: no se agrega canal; la pizarra y la foto de cuerpos son las de siempre, iguales para todos.
2. Acierto sin balancear: el uso de las zonas se mide contra su parte del anillo (0.10), no en crudo.
3. Mundo que se come la comida: el oasis no repone más (spawn uniforme); si los cuerpos lo vacían, lo muestra `comp_oasis` (descriptivo).
4. Sitios fijos: zonas sorteadas por semilla (arnés U8: 10 semillas, 10 inicios distintos); ningún carro tiene posiciones escritas.

## 8. Semillas (grep 30-sep en .py/.md de todo JUACO: 718xxx no aparece)
explora 718001–718005 · arnés 718080–718089 · humo 718090. T 100 000 (humo 20 000).

## 9. Comandos
`python experimentos/organelos/o1_evo/grande/identidad_grande.py` (arnés, 1 proceso) ·
`python experimentos/organelos/o1_evo/grande/corre_grande.py --humo [--siembra <ruta>]` (1 proceso, ≤ 6 corridas) ·
`python experimentos/organelos/o1_evo/grande/corre_grande.py --explora --pool 4 [--siembra <ruta>] [--reanuda]` (SOLO el coordinador,
con este preregistro, el runner y pista_grande commiteados).
