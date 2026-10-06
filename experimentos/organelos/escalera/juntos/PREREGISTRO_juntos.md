# PREREGISTRO — "LOS TRES JUNTOS": MEMORIA DE LUGAR (P1) + SEÑAL CON COSTO (P7) + PREGUNTA (P10) EN UN SOLO ORGANISMO (O1_TODO), EN UN MUNDO QUE PIDE LAS TRES. ¿SE SUMAN O SE ESTORBAN? CONFIRMATORIO (1-oct-2026, madrugada)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y
réplicas). Encargo nocturno del director (1-oct, "LOS TRES JUNTOS"). Escalera: `../ESCALERA.md`. Bitácora: `../BITACORA.md`.
**DECLARACIÓN (sesgo del diseñador):** este diseño VIENE DE EXPLORACIONES VISTAS (sec. 11): un humo (738590–738591, T 30k) y cuatro
exploraciones de un proceso (738581–738586, T 100k). Con ellas se vio **la trampa del TECHO** (sec. 9): la pareja memoria + pregunta ya cruza
18 de 18 en el mundo de la serie, así que la puerta SUMAN por cruce es casi inalcanzable. Se declara ANTES de datos y la letra lo reporta por
código (`techo`). El mundo y la letra son los del encargo del director; no se cambiaron tras ver la exploración. Las semillas de la serie son
NUEVAS y disjuntas de las vistas. Escrito ANTES de cualquier dato de serie. Este bloque no abre ERR (177–179 siguen libres).

## 0. Qué es y qué no es
Es una prueba de COMPOSICIÓN por diseño: tres piezas que FUNCIONAN ×2 por separado (P1, P7 con reserva ERR-175, P10) se ponen en un mismo
carro sin una sola línea de unión, y se mide si el conjunto cruza más que cada pareja. NO es selección natural, NO es un peldaño nuevo de
capacidad y NO dice nada de la pista vieja (el muro sigue en pie). Si da NO SUMAN por techo, eso NO es "no se suman": es "este mundo no deja
verlo en el cruce" (sec. 9).

## 1. Pregunta
En el mundo de P1b donde el oasis se muda cada 20 000 pasos y emitir cuesta 0.01 de E, ¿el organismo con las tres piezas (`todo`) cruza más
que el de memoria + señal (`sen`) y que el de memoria + pregunta (`preg`)? ¿O cruza MENOS que la mejor pareja (epistasis negativa)?

## 2. Mecanismo y memoria nueva (carro `O1_TODO`, `construye_juntos.py` sha `d469c8f3bf194d64`)
- Por anclas sobre el texto de O1_LUGAR (`construye_p1.py` sha `90dc1b6f848fac80`, texto sha `49eee6bb278ea097`), aplicando las anclas y los
  métodos IMPORTADOS de `construye_p7.py` (sha `50179cf58798120c`: SEÑAL) y después los de `construye_c.py` (sha `024a89476109b997`, peldaño
  'preg': PREGUNTA). No se copia código de las piezas. **Memoria nueva: CERO. Código de conducta nuevo: CERO** (lo único propio es la cabecera).
- Perillas: `LUGAR` (1), `SENAL` + `SN_BARAJA`, `PREGUNTA` + `PG_BARAJA` (0). Parámetros de las piezas, sin tocar: SN_CADA 100, SN_UMBRAL 0.3,
  SN_W 1.0, PG_OLVIDO 0.01.
- **Interacciones que el texto deja (no se arreglan; son la pregunta):** (i) la señal sólo siembra bins donde el linaje NO ha mordido
  (`nl == 0`): si el oasis vuelve a un bin ya vivido y olvidado, lo oído no entra (posible estorbo); (ii) el que emite manda su mejor bin
  recordado: sin PREGUNTA manda el oasis VIEJO hasta que muerde en otro lado; con PREGUNTA el olvido por presencia limpia lo que emite (posible
  suma); (iii) emitir cuesta E a un linaje que con PREGUNTA ya llega solo (posible estorbo).

## 3. Mundo (`mundo_tramo_c.py` sha `4a1044a4e0e1d5c9`)
El de P1b (oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista_r 20) + `mueve` 20 000 (4 mudanzas en T 100k) + `c_e` 0.01. Es el mundo de P10 con
el costo de P7. Arnés: `c_e` no toca a quien no emite (los brazos `lug` y `preg` son físicamente los de P10).

## 4. Brazos (monocultivo de 9, L 360, 36 objetos, fundador limpio, T 100 000)
| brazo | carro | piezas | papel |
|---|---|---|---|
| `todo` | O1_TODO | memoria + señal + pregunta | CANDIDATO |
| `sen` | O1_TODO_SEN | memoria + señal (pregunta apagada; == O1_LUGAR_SENAL bit a bit) | pareja (`sen_preg_off` del encargo) |
| `preg` | O1_TODO_PREG | memoria + pregunta (señal apagada; == O1_LUGAR_PREG bit a bit) | pareja (`preg_sen_off` del encargo) |
| `lug` | O1_LUGAR | sólo memoria | base (validez) |
| `todobar` | O1_TODO_SBAR | las tres, la señal LEÍDA al antípoda (b + 15 mod 30) | control de contenido |

## 5. Medidas y validez
- **Principal:** linajes que cruzan (`cruza_real` del juez), por semilla (de 9) y suma (de 180).
- **Descriptivo:** mayorías, fundadores por linaje, latencia tras la mudanza (pasos hasta el primer bocado A+C dentro del oasis nuevo; física),
  nunca llegan, escrituras/cobros/siembras, excursiones/olvidos, A+C del mundo (trampa 3).
- **Validez (todas o NO SE LEE):** V1 completa, coherente, 0 abortos · V2 el mundo pide (4 mudanzas, mueve 20000, c_e 0.01 en la salida) ·
  V3 el oasis actúa · V4 estado (carro y perillas de cada brazo) · V5 los módulos actúan donde deben y callan donde no (escrituras, cobros y
  lecturas > 0 con SENAL; 0 sin ella; excursiones y olvidos > 0 con PREGUNTA; 0 sin ella) · **V6 BANDAS** (suma de 180, escaladas a n):
  - `lug` 60–115 (P10: 82 y 91; P7: 80 y 81; P1b igual)
  - `preg` 140–180 (P10: 164 y 163)
  - `sen` 50–155 (**no hay serie previa de la señal en el mundo que se muda**: P7 sin mudanza dio 132 y 124; exploración aquí 13 de 18 ≈ 130
    de 180; banda ancha, declarada como débil)

## 6. LA LETRA (`corre_juntos.lee_serie`; 14 casos sintéticos en el arnés (f))
Umbrales (n 20): pareada ≥ 13/20; suma ≥ +10. Pareada = semillas donde `todo` cruza ESTRICTAMENTE más (los empates no cuentan).
- **SUMAN** = `todo` > `sen` en ≥ 13/20 Y suma ≥ +10, Y `todo` > `preg` en ≥ 13/20 Y suma ≥ +10, Y `todo` > `todobar` en ≥ 13/20 Y suma ≥ +10
  (si gana a las parejas pero no al control: NO SUMAN con matiz "la señal no suma por su contenido").
- **SE ESTORBAN** = `todo` < la MEJOR pareja (la de mayor suma; si empatan, contra las dos) en ≥ 13/20.
- **NO SUMAN** = lo demás. Matiz por código: `TECHO` si SUMAN no era alcanzable (semillas ganables = n − semillas con la pareja en 9/9 < 13, o
  margen de suma 180 − suma(pareja) < 10).
- **NO SE LEE** = falla la validez.
- **Sombra (no cambia la letra):** fundadores y latencia de `todo` menores que los de cada pareja en ≥ 13/20 (`SUMAN_en_sombra`).
**Nulos por puerta:** cada pareada bajo p = 0.5 sin empates: P(≥ 13/20) = 0.132; con los empates que el techo impone es MENOR (declarado: el
nulo real de SUMAN es < 0.132² ≈ 0.017 para las dos parejas si fueran independientes; no lo son). SE ESTORBAN: ≤ 0.132. Las sumas: media 0
bajo el nulo, dispersión no calibrada (se reporta).

## 7. Regla de parada y vocabulario
Una serie de 20; réplica (20 semillas nuevas, mismo runner, mismo sha) sólo si la serie da SUMAN, SE ESTORBAN o NO SUMAN en el umbral (± 1).
Un veredicto con letra no se re-corre; cortada o NO SE LEE: sólo `--reanuda`. Si el apagado corta la serie, `--reanuda` completa las mismas
semillas (cada corrida escribe su JSON). "SUMAN ×2" sólo con serie + réplica. NO SUMAN con matiz TECHO se escribe así, entero, nunca "no suman".

## 8. Predicciones firmadas (antes de la serie; calibradas con la exploración de 2 semillas, declarado)
1. **Letra: NO SUMAN con matiz TECHO** (80 %). SUMAN: < 3 %. SE ESTORBAN: 5 %. NO SE LEE por banda: 12 % (la de `sen` es la débil).
2. Sumas de 180: `todo` 155–178 · `preg` 150–175 · `sen` 95–140 · `lug` 70–105 · `todobar` 70–130.
3. `todo` − `preg` entre −8 y +10; `todo` gana a `preg` en 3–9 semillas de 20, pierde en 2–8. `preg` en 9/9 en ≥ 7 semillas (techo activo).
4. `todo` > `sen`: ≥ 15/20 y ≥ +25 (esa puerta pasa: la pregunta sí suma sobre la señal).
5. **Control:** `todo` > `todobar` en ≥ 13/20 y ≥ +25: el contenido de la señal IMPORTA dentro del organismo conjunto (leído al antípoda
   deshace lo que la pregunta da). Es la predicción con más riesgo: viene de 2 semillas (18 contra 10).
6. Latencia tras la mudanza: `todo` y `preg` 350–550 pasos, sin orden entre ellas (pareada 7–13); `sen` y `lug` > 1 000.
7. Fundadores (mediana por linaje): `todo` y `preg` < 2; `sen` 2–15; `lug` > 15.
8. A+C del mundo: `todo` 4.4–5.2, `preg` 4.2–4.9 (los dos pelan el mundo respecto de `lug` ~6.5; trampa 3, se reporta).
**Qué lo refuta:** (1) cae si la letra es SUMAN o SE ESTORBAN; (5) cae si `todobar` queda a menos de 10 de `todo`; (3) cae si `preg` < 150.

## 9. Las cuatro trampas (y la del techo)
- **Canal simétrico:** el control `todobar` escribe y paga igual; sólo cambia a dónde lleva lo leído (antípoda fijo, ERR-170). `preg` y `lug`
  no escriben (arnés: 0 escrituras, 0 cobros).
- **Acierto sin balancear / TECHO (LA QUE MUERDE AQUÍ):** `preg` cruzó 9/9 en 10 y 7 de las 20 semillas en las dos series de P10 y en 2 de 2
  de la exploración: `todo` no puede ganarle en esas semillas, así que SUMAN (≥ 13/20) queda casi fuera de alcance; SE ESTORBAN sí es
  alcanzable. La letra es ASIMÉTRICA y se declara. Se probó si un mundo más duro abría recorrido (mueve 10 000 y 5 000, exploraciones 3 y 4):
  NO lo abre (preg 15 y 16 de 18; `todo` 16 y 15). El techo es de la pieza PREGUNTA, no del ritmo de la mudanza.
- **Mundo que se come la comida:** `todo` y `preg` dejan el mundo en ~0.7 del A+C de `lug`; se reporta (`mundo_AC_todo_sobre_lug`), no puntúa.
- **Sitios fijos:** el oasis se sortea por semilla y se muda 4 veces; el control usa un desplazamiento fijo de 15 bins, nunca dentro del oasis
  (4 bins contiguos).

## 10. Instrumento, semillas, costo, comandos
- Runner `corre_juntos.py`; cada corrida ES `corre_v143.tarea` con `mundo_tramo_c.run`; la fila es `corre_c.fila_c('preg')` + los bloques
  pizarra/señal/latencia de `corre_p7.fila` (IMPORTADOS por sha: `corre_c.py` `01e4ad94dd06e133`, `corre_p7.py` `82c3811c144d1a2b`,
  `corre_p1.py` `392b71186cf49b60`, `mundo_escalera.py` `4f28b372207ba0a6`).
- Arnés `identidad_juntos.py`: 51/51 (salida en `identidad_juntos_salida.txt`): las tres apagadas == O1_LUGAR, sólo señal == O1_LUGAR_SENAL,
  sólo pregunta == O1_LUGAR_PREG (salida ENTERA, 3 mundos, 2 semillas); regla 14 campo a campo contra corre_p10 y corre_p7.
- Semillas NUEVAS 7385xx: serie 738501–738520 · réplica 738551–738570 · explora 738581–738586 (usadas) · humo 738590–738595 (738590–92
  usadas) · arnés 738530–738539.
- Costo: 100 corridas × ~110 s (120 s los brazos con PREGUNTA) con pool 2 ≈ 1.6–1.8 h. **Si arranca después de la 1:50 no termina antes del
  apagado de las 4:00**: se completa con `--reanuda` (no se cambia n).
- Comandos (sólo el coordinador, con todo commiteado):
  `python experimentos/organelos/escalera/juntos/corre_juntos.py --serie --pool 2`
  `python experimentos/organelos/escalera/juntos/corre_juntos.py --serie --pool 2 --reanuda`
  `python experimentos/organelos/escalera/juntos/corre_juntos.py --replica --pool 2`
  `python experimentos/organelos/escalera/juntos/corre_juntos.py --lee <carpeta>`

## 11. Historia honesta (ráfaga; NADA de esto cuenta; `../BITACORA.md`)
| qué | semillas, T, mueve | cruzan | lectura |
|---|---|---|---|
| humo 1 | 738590–91, T 30k, mueve 10k | todo 2, sen 8, preg 7 (de 18) | el runner corre y escribe JSON; a T 30k el cruce no se lee (como en P10) |
| explora 1 | 738581–82, T 100k, mueve 20k | todo 18, sen 13, preg 18 | TECHO: preg ya está en 9/9 en las dos; fund 0.06 = 0.06; latencia 387.5 vs 387.0 |
| explora 2 | mismas semillas | lug 9, todobar 10 | la señal al antípoda deshace la pregunta: 10 contra 18; fund 18.3 contra 0.06 |
| explora 3 | 738583–84, T 100k, mueve 10k | todo 16, sen 12, preg 15 | mundo más duro: no abre recorrido (+1) |
| explora 4 | 738585–86, T 100k, mueve 5k | todo 15, sen 9, preg 16 | más duro aún: tampoco (−1) |
| humo 2 | 738592, T 30k, mueve 10k, los 5 brazos | todo 7, sen 5, preg 1, lug 2, todobar 0 (de 9) | runner FINAL (sha `db75135c8c2f3e0d`) por main con los cinco brazos; V1–V5 pasan; a T 30k no se lee |
Orden real: la identidad corta (las tres identidades bit a bit) pasó ANTES del humo; el arnés completo (51/51) terminó mientras corría el humo
1 y antes de leer ningún número de cruce. Se declara.

## 12. Cierre antes de datos (1-oct)
Shas: `construye_juntos.py` `d469c8f3bf194d64` · carros O1_TODO `b7519a4a481a0cf5`, O1_TODO_SBAR `153891018a52b5db`, O1_TODO_SEN
`dff5e762bd23612e`, O1_TODO_PREG `382dafcf822b36a1`, O1_TODO0 `4e197ff6d7d86841`. Runner `corre_juntos.py` `db75135c8c2f3e0d` · arnés `identidad_juntos.py` `52221ec214fd2840` (51/51 con ese runner). Si alguno cambia, re-correr el arnés.
