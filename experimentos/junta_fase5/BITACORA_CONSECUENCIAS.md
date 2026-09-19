# BITÁCORA DE CONSECUENCIAS — memoria compartida de la junta (exoesqueleto)
Formato por línea: `[creador] idea → prueba (semillas) → resultado → lección`. Se escribe al final; no se borra nada.

## Consecuencias heredadas (del registro, bloques 4–6 del mundo de familias)
- [registro] k = 3 → referencia de FAMILIA exacta (BAR-T 5/20) pero no distingue variante (PAR 12/20).
- [registro] sufijo de 3 píxeles de variante → PAR 15/20, hermana cae a 5–6/20, pero BAR-T sube a 10–11/20 y la base sin
  mensaje sube 0 → 4–6: con 4 casillas por par, una sola ganadora reparte entre familias (tabla 8× más dispersa).
- [registro] la predicción del creador acertó en la hermana y falló en el otro token: medir BAR-T siempre.
- [registro] ERR-54: el análisis del runner puede detenerse en una puerta; calcular brazos desde los crudos.
- [registro] ERR-64b / ERR-70 / ERR-71: controles DEBE-diferir, P-I4 por exclusión, el caso (d) del arnés debe probar la
  dirección con un mensaje del catálogo en las tres semillas.
- [alefast, 19-sep] en agentes, la ganancia grande vino del ciclo "preguntar una vez y recordar"; el algoritmo propio sumó poco.
  Lección para la junta: pregunta cuando el criterio no esté claro, y registra cada consecuencia.

## Consecuencias de la junta

- [B] **Diagnóstico antes de proponer** (lectura de b5/b6, sin correr): el precio del sufijo no es de *bits* sino de
  **densidad**. `mem_cobertura` cae de 3.5/4 (88 %) a ~11/32 (34 %) → en b5 las k celdas **votaban** (las que no se
  fugaban contestaban su valor propio, negativo) y en b6 **abstienen** (aportan 0), así que la única celda por la que
  se cuela el mensaje decide sola. → Predicción escrita antes de medir: *devolver el voto devuelve BAR-T*.
  **Lección:** la suma de "las que saben" es una DISYUNCIÓN; quien fija la referencia es el combinador, no el ancho
  de la dirección.
- [B] **Relevo marginal** (`mem_marginal=1`: si la celda no conoce la subcasilla exacta, contesta la marginal de su
  bin ponderada por visitas) → humo 901–903, T = 30 000, 7 brazos → **REFUTADO**: BAR-H 2/3 y VALOR 1/3 (b6 da 0/3
  en los dos) y CANAL cae a 2/3. El diagnóstico de la entrega lo enseña: la marginal del bin **incluye la subcasilla
  que el mensaje acaba de sobrescribir** (y la sobrescritura conserva las visitas, así que ni la moda la salva).
  **Lección:** cualquier agregado sobre el bin hereda el mensaje; la objeción (a) del preregistro del bloque 6 vale
  también cuando el nivel grueso se **calcula** en vez de escribirse. Con `mem_marginal=0` sigue siendo b6 bit a bit.
- [B] **Dos canales (forma / variante) con relevo por conflicto de signo** (`mem_canales=2`; k celdas de forma + 1 que
  toca los píxeles 9–11, y la vía lenta abstiene si los dos canales se contradicen) → humo 901 → **REFUTADO**: en
  BAR-H la vía lenta lee **+4.00 con 4/4 celdas exactas** — el canal de variante, ciego a la forma, tenía valor propio
  **positivo** para el referente, así que no hay contradicción que detectar. **Lección (la que más vale):** ningún
  combinador de *valores propios* puede vetar al mensaje si el valor propio no lo contradice; lo que discrimina no es
  el valor sino **si el mensaje alcanzó la dirección de esa celda**.
- [B] **Lectura CONJUNTIVA** (`mem_conj=1`: la vía lenta contesta sólo si **las k** celdas conocen su dirección exacta;
  si una no, abstiene y releva a la lineal) → humo 901–903, T = 30 000 → **SOBREVIVE**: es la única celda con BAR-H
  0/3 **y** BAR-T 0/3 (b5 3/3 y 2/3; b6 0/3 y 2/3), con `dist(PAR)` 3/3 y muertes 17 (b6 11, b5 296 en estas
  semillas). El diagnóstico de la entrega es el mecanismo, no la conducta: para el referente, CANAL lee **+3.00 con
  3/3 exactas** y BAR-H **−9.00**; BAR-T y VALOR o abstienen (0/3 exactas) o leen negativo. **Lección:** la tupla de
  las k direcciones **ya es un código factorizado** (la forma en el bin de cada par, la variante en la firma); lo que
  faltaba no era más tabla, era leerla como **intersección** y no como unión.
- [B] La única semilla en que CANAL no muerde con la conjunción (902) tiene `fam1 = 1`: el receptor ya leía por la vía
  **rápida** y el mensaje quedó escrito y no consultado. Es **P-I5**, el punto ciego conocido del bloque 4b, no el
  mecanismo. **Lección:** mirar `fam1` antes de culpar a la lectura.
- [B] **Arnés, no instrumento:** mi caso (z) afirmaba "con el relevo la vía lenta no abstiene nunca" y es falso (un
  bin puede estar entero sin visitar). Se sustituyó por comparar las tres reglas **sobre la misma tabla**.
  **Lección:** una afirmación del arnés que necesita dos trayectorias distintas no es una propiedad del mecanismo;
  las reglas de lectura se comparan sobre el mismo estado.
- [B] El humo **no reproduce las líneas base** (b5 da `dist(PAR)` 3/3 donde la serie dio 12/20, y BAR-T 2/3 donde dio
  5/20): a T = 30 000 y n = 3 los brazos no se pueden comparar entre sí. Lo que el humo sí decide es el **mecanismo**
  (qué lee la vía lenta en el paso de la entrega) y el montaje (P-I2 3/3, P-I3 OK, P-I4 3/3).
  **Lección:** pedir siempre el diagnóstico de la entrega; sin él, las tres ideas de arriba habrían parecido iguales.
- [B] **Entrega al coordinador**: `corre_jb_serie.py` con `Pool` por variable de entorno `JUACO_POOL`
  (default 6) y `--pool N`; el Pool se abre UNA vez y los crudos los escribe el proceso PADRE tras cada
  resultado (por el BrokenPipe de hoy con Pool(14)). Probado de punta a punta con `--desde 901 --n 2
  --T 30000` (36.5 s) sin gastar ninguna semilla de 821-860. **Lección:** un runner que sólo se prueba en la
  serie real es un experimento sin humo; el humo del *instrumento* y el del *runner* son dos cosas distintas.
- [C] antes de proponer, repaso de ERR-35..84 → los que mi idea podía repetir: ERR-46..49 (recalibrar la medida
  hasta que pase), ERR-44 (medir pesos en vez de conducta), ERR-54 (análisis que tumba el registro), ERR-64b
  (controles que deben diferir), ERR-70/71 (P-I4 por exclusión; el caso (d) no pasa por el emisor), ERR-31 (no
  recopiar el mundo) → lección aplicada: umbrales, diagnósticos y refutadores escritos ANTES de correr; el
  crudo se guarda antes del análisis; el emisor se importa del bloque 6 sin tocarlo.
- [C] mecanismo: la CASILLA se divide por conflicto de signo (regla de v11/B-5 un nivel más abajo) y las hijas
  NACEN CON EL VALOR DE LA MADRE → arnés `identidad_c1.py` (semillas 1–3, T 20 000/60 000/120 000) →
  **61/61**: con `variante_hija=0` es `organismo_familias_b6` BIT A BIT en 12 mundos × k ∈ {1,3} × sufijo
  ∈ {0,1}, en los tres modos del canal, == organismo_v14 (TRONCO) y == organismo_v15f_on; inercia sin tabla; 8
  formas de escribir mal la perilla que LANZAN; 4 controles que DEBEN diferir (≥ 2/3, ERR-64b) → lección: la
  identidad bit a bit contra b6 hereda su cadena entera sin recopiar una línea.
- [C] estructura (T = 0 y sin pasar por el emisor, ERR-71): con la casilla dividida la HERMANA sale de la
  dirección vigente del referente (grupo 1–3 de 32, hermana fuera) y el referente sigue en la suya; cobertura
  de la ganadora **4/4 contra 12/32** del sufijo uniforme del bloque 6 → lección: el precio que pagó el bloque 6
  (tabla 8× más dispersa, celdas que abstienen y no pueden votar) NO se paga si la hija nace con el valor de la
  madre; ahí estaba el BAR-T de 11.
- [C] humo 901–903, T = 100 000, 3 celdas pareadas (k3v0 = b5 bit a bit, k3v1 = b6 bit a bit, k3h1 = candidato)
  → k3h1: CANAL 1/3, CORTADO 0, BAR-H 0, BAR-T 1, VALOR 0, PAR dist 2 (PAR0 0), muertes 29 contra 462 (k3v0) y
  51 (k3v1) → **P-I5 CAYÓ: la boca leyó la vía RÁPIDA en 2/3** → lección: con la puerta cerrada todos los brazos
  dan 0 y la "especificidad" es VACUA; BAR-H 0 no se puede leer como éxito (es el mismo error de vacuidad que
  ERR-64b arregló en los controles).
- [C] ¿por qué se cerró la puerta? (diagnóstico en las mismas semillas, sin gastar ninguna nueva): mi tabla
  acierta más → la boca se contradice menos → hay MENOS divisiones de Kenyon (49 celdas contra 65) → el código
  del referente deja de cambiar y acumula evidencia → `puerta_pat` lo declara FAMILIAR → el mensaje se escribe y
  no se consulta → lección para la junta: **el organismo que aprende mejor el mundo deja de escuchar**; la
  puerta de familiaridad del tronco es una oreja que se cierra con la competencia, y cualquier candidato que
  mejore la vía lenta va a chocar con P-I5.
- [C] ¿es sistemático? → el gemelo MUDO de las tres celdas en las semillas del arnés (1, 2), que son las que ya
  usó el humo del bloque 6 → vía LENTA 2/2 en las tres celdas (y 901–903 son mundos donde la base muere 936 y
  457 veces) → lección: la caída de P-I5 no está demostrada como propiedad del mecanismo; queda como RIESGO
  DECLARADO de la serie, no como resultado.
- [C] diagnóstico completo en las semillas del arnés (1, 2), declarado como desviación de la nave (el humo son
  901–903; 1 y 2 son las del arnés y las del humo del bloque 6): k3h1 CANAL 2/2, CORTADO 0, BAR-H 1, BAR-T 1,
  VALOR 0, PAR dist 1, muertes 27; pero **k3v0 da BAR-H 0/2** cuando la serie del bloque 6 midió 13–14/20 →
  lección (la misma que escribió el creador del bloque 6): con n ≤ 3 la línea base NO se reproduce, así que el
  humo no puede pre-validar ningún contraste; sólo sirve para montaje, coste y mecanismo.
- [C] predictor del mecanismo (gemelo mudo, foto al final de la vida): valor GRUESO de las k ganadoras en el bin
  del referente → negativo (el de la familia) en 12 de 15 celdas-semilla; en las 15, la ganadora comparte bin
  entre referente y hermana en 13 → lección: la precondición del mecanismo (que el mensaje CONTRADIGA a la
  familia para que la casilla se divida) se cumple en ~80 %, y donde una ganadora ya vale +1 el mensaje se filtra
  igual que en b5: eso acota cuánto puede bajar BAR-H y hay que predecirlo, no esconderlo.
- [C] decisión del coordinador (19-sep, tras mi humo): **P-I5 no se toca**; se lee como puerta de VALIDEZ y la
  semilla vacua sale del numerador Y del denominador de todos los brazos de esa celda, declarada, con el mismo
  trato para la línea base → implementado en `corre_c1.py` (`PI5_por_semilla`, `vacuas_PI5`, lectura PRINCIPAL
  por celda y SECUNDARIA pareada en la intersección), escrito en `UMBRALES` ANTES de correr → lección: un
  criterio no se cambia después de ver datos, pero sí se puede declarar cómo se leen las semillas que no miden.
- [C] el hallazgo de la oreja cerrada convertido en predicción falsable en la MISMA corrida (orden del
  coordinador): **V1** vacuas(k3h1) − vacuas(k3v0) ≥ +3 en las dos series (predigo 6/20 contra 1/20 y 2/20) y
  **V2** las semillas vacuas de k3h1 tienen MENOS celdas de Kenyon que las válidas → lección: un hallazgo
  colateral deja de ser anécdota en cuanto se le pone umbral y refutador antes de correr.
- [C] "la oreja" (que la puerta consulte la vía lenta cuando la casilla que tocaría leer ACABA DE NACER) queda
  como candidato APARTE en `C/PREREGISTRO_oreja.md`: mecanismo en código, identidad exigida, semillas 861–900,
  predicción y seis refutadores — **escrito y NO corrido**, con el refutador (6) diciendo que si C1 pasa sin
  oreja, la oreja sobra por Occam → lección: el parche que se me ocurrió DESPUÉS de ver datos no entra en el
  candidato; se escribe como hipótesis con su propio preregistro y espera su turno.
- [C] confirmación lista para el coordinador: `corre_c1.py --serie --desde 821|841 --T 100000` (27 tareas de
  identidad + 20 emisores + 540 corridas por serie, Pool(14), ~8–12 min); comprobado **en seco** con `--plan`
  (no simula nada) → lección: entregar el comando probado en seco y con los shas de origen verificados evita que
  el coordinador descubra el error con 560 corridas ya lanzadas.
- [A] el precio del sufijo (b6) es de DENSIDAD y no de referencia → cálculo estructural T=0 en 901-903 (sin simular) →
  `piso_forma` = 4/32 en las tres: tres celdas de FORMA no pueden bajar de la familia, y el sufijo baja la densidad ×8 →
  lección: la resolución se puede multiplicar con DOS particiones densas (forma × mixta) sin vaciar ninguna casilla.
- [A] dos tipos de ganadora (3 de FORMA + 1 mixta por píxel de variante), lectura = promedio de las dos sumas →
  humo 901-902 (T=30000) → CANAL 2/2, CORTADO 0/2, BAR-T 0/2, pero BAR-H 2/2 y dist(PAR) 1/2 → lección: la DIRECCIÓN
  conjunta ya es única (1-2 de 32) y aun así el VALOR leído se cuela: la dirección no es la lectura.
- [A] descomposición en el paso exacto de la entrega (T = t_entrega+1, 901/902) → tras un mensaje de +1 las ganadoras
  elegidas son las celdas que dicen +1 EN TODAS PARTES (el mensaje actualiza `_MEv` y re-elige) → lección: en b4/b4b/b5/b6
  el mensaje no sólo escribe, también cambia QUIÉN lee; fuga no medida hasta hoy (perilla `msg_elige`, celda b5k3e lista).
- [A] `msg_elige=0` (el mensaje escribe pero no re-elige) con lectura de promedio → humo 901-902 → BAR-H 2/2 y BAR-T 2/2
  → lección: quitar la re-elección sola no basta; con promedio, el tipo ciego (FORMA) decide.
- [A] `combina='min'` (conjunción entre tipos: para morder, los dos de acuerdo) → humo 901-902 → CORTADO/BAR-T/VALOR
  leen -9 y dist(PAR) 2/2, pero BAR-H +3 en una semilla → lección: la suma dentro del tipo da -1 cuando falta una casilla,
  y -1 no frena a una boca hambrienta (hace falta ≲ -2.1 con hambre=1): el problema es de ESCALA, no de signo.
- [A] `exige_dir=1` (una casilla desconocida no es "no opino", es "no me consta": la tabla calla) → humo 901-903 →
  A1: CANAL 3/3, CORTADO 0/3, BAR-H 1/3, BAR-T 1/3, dist(PAR) 2/3, muertes 10/258/20 → lección: primera lectura que baja
  BAR-H y BAR-T a la vez; los tres fallos son la MISMA semilla 902 (mundo hambriento) y todos con valor leído -1.0 de la
  LINEAL, no de la tabla: al abstenerse, la tabla devuelve la decisión a un lector sin referencia.
- [A] ablaciones en el mismo humo (901-903): sin conjunción (A1-c) BAR-H 2/3 y BAR-T 2/3; sin dirección completa (A1-d)
  BAR-T 2/3 y muertes 393; con re-elección (A1-e) igual que A1 en 3 semillas → lección: las dos reglas nuevas sostienen
  el resultado, pero 3 semillas NO separan A1 de A1-e: eso lo decide la confirmatoria.
- [A] pesos de tipo aprendidos por consecuencia (multiplicativos, normalizados) → identidad y humo → BIT A BIT idénticos
  bajo `combina='min'` (el mínimo no usa pesos) → lección: MI mecanismo favorito quedó medido INERTE; no entra en el
  candidato (Occam), y se reporta como predicción propia refutada.
- [A] `dentro='min'` (mínimo escalado dentro del tipo) → arnés (1,2) y humo (901-903) → idéntico a la suma en TODOS los
  casos → lección: las ganadoras de un mismo tipo, elegidas por error propio, no discrepan entre sí; la perilla se
  documenta como inerte medida y se retira del candidato. Un control que no difiere también es un dato (no se fuerza).
