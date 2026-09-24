EXPLORATORIO — no es dato

# Prototipos exploratorios de la nube — noche del 23→24-sep-2026

> Libertad para experimentar dada por el director para esta noche (`NUBE.md` §2b, punto 3). **Nada de aquí es dato ni sube un
> nivel**: sirve para decidir qué se preregistra. Cada número lleva su comando y su semilla.
>
> **Reglas de esta carpeta:**
> - Semillas exploratorias **24001–24099** (grep del 24-sep: ningún paquete las usa). No deben reutilizarse en series confirmatorias.
> - Un proceso a la vez, en el núcleo que dejan libre las series (Pool 3).
> - No se toca ningún archivo de la carrera ni del tronco: todo son subclases o copias, construidas aquí.

## Instrumento
- **Pista:** la de la carrera del 22-sep sin tocar (`carrera_escuderias/pista.py` 9f47c65e438e0ff4). Monocultivo de 9 carros,
  escala 1 (L 360, 36 objetos), pizarra 1, `fundador_limpio=1`. Es la misma entrada que `juez.tarea` y `corre_v143.tarea`.
- **Juez:** `juez.resumen_linaje` (6a68f640a7832f12). Las medidas salen sólo de la física (ERR-96).
- **Corredor:** `corre_explora.py`.
- **Identidad:** `corre_explora.py --identidad` comprueba que la subclase sin reglas (W0) es FABRICA bit a bit, en toda la física de
  los 9 linajes y la pista (semillas 24098 y 24099, T 3000). Resultado: **OK** (01:50 UTC).

## (i) Arriesgar según la reserva
Carros en `carros_reserva.py` (NEO, LIM) y `carros_extra.py` (NEO, MAL, LIM con la función `aplica`, también sobre APR en
`carros_apr_reserva.py`). Todos son subclases: dejan correr la boca del carro base (mismo consumo del rng) y sólo corrigen la
decisión final. La reserva es r = min(E, Ag).

**Tanda i1** (01:50–02:04 UTC):
`python experimentos/exploratorio_nube_20260924/corre_explora.py --brazos FAB,NEO5,LIM,NEO5_LIM,O1 --desde 24001 --n 6 --T 30000 --tag i1`
Semillas 24001–24006, T 30 000. JSON: `datos/explora_i1_FAB-NEO5-LIM-NEO5_LIM-O1_s24001-24006_T30000_20260924_015047.json`.

| brazo | R0 real (mediana) | persisten | vida | muere sin parir | gana a FAB (pareado) |
|---|---|---|---|---|---|
| FAB | 0.149 | 1/54 | 66 | 0.89 | — |
| NEO5 (no prueba lo desconocido si r < 0.5) | 0.133 | 1/54 | 66 | 0.90 | 1/6 |
| LIM (limpia lo malo si r ≥ 1.4) | 0.033 | 0/54 | 70 | 0.97 | 0/6 |
| NEO5_LIM | 0.033 | 0/54 | 70 | 0.97 | 0/6 |
| O1 | 0.775 | 20/54 | 3454 | 0.25 | 6/6 |

Lectura:
- **La neofobia sola no ayuda.** Lo desconocido es poco: el 12 % de los encuentros en la semilla 24001.
- **Limpiar desde 1.4 hunde el R0.** El golpe deja el nivel en 1.0, y al paso siguiente el costo lo baja de la ventana de parto
  (hacen falta E y Ag ≥ 1.0 durante 500 pasos seguidos). El que limpia pierde su parto.
- **El 72 % de los encuentros de FABRICA son con objetos que su valor ya marca como malos.** Semilla 24001: 17 706 de 24 682.
  De ahí salen las variantes MAL (no morder lo malo conocido con reserva baja) y VER (tema iii).

**Tanda i2** (02:06–02:32 UTC, nice 19):
`python experimentos/exploratorio_nube_20260924/corre_explora.py --brazos FAB,MAL14,MALINF,RES,VER,VER_MAL,VER_RES,APR,APR_RES --desde 24001 --n 6 --T 30000 --tag i2`
Identidad previa: 12/12 OK (W0, W2, WP, WV == FAB; WA == APR; RESP == RES; semillas 24098–24099).

| brazo | R0 real | persisten | vida | muertes | mord. B+D | pasos sin nada bueno | gana a FAB |
|---|---|---|---|---|---|---|---|
| FAB | 0.149 | 1/54 | 66 | 116 | 465 | 0.000 | — |
| MAL14 (no muerde lo malo si r < 1.4) | 0.097 | 2/54 | 200 | 42 | 45 | 0.127 | 0/6 |
| MALINF (nunca muerde lo malo) | 0.133 | 2/54 | 200 | 44 | 41 | 0.126 | 2/6 |
| RES (neo 0.5, mal 1.45, limpia ≥ 1.45) | 0.116 | 7/54 | 200 | 47 | 52 | 0.082 | 0/6 |
| VER (objetivo por valor) | 0.136 | 2/54 | 77 | 114 | 468 | 0.001 | 2/6 |
| VER_MAL | 0.110 | 2/54 | 200 | 44 | 43 | 0.178 | 1/6 |
| VER_RES | 0.089 | 8/54 | 200 | 49 | 52 | 0.109 | 1/6 |
| APR | 0.118 | 6/54 | 66 | 110 | 453 | 0.001 | 1/6 |
| APR_RES | 0.116 | 7/54 | 200 | 48 | 52 | 0.082 | 0/6 |

Lectura:
- **Ninguna variante le gana a FABRICA en R0 real.**
- **Las reglas que vetan lo malo sí cumplen lo que prometen, pero el mundo se tapa.** Bajan las mordidas malas a la décima parte y
  las muertes a menos de la mitad. Sin mordidas de lo malo, nada lo quita del mundo (sólo el olvido): hasta el 18 % de los pasos no
  hay nada bueno en ninguna parte. El cuerpo muere de hambre a los 200 pasos exactos: una mordida mala al nacer lo deja en 0.2, y
  0.2 / 0.001 = 200.
- **VER no reduce las mordidas malas.** En un anillo, el camino hacia lo bueno pasa por encima de lo malo, y la boca con hambre lo
  muerde igual.
- **La limpieza es un bien público.** FABRICA muerde todo: mantiene el mundo limpio y muere joven. Si veta lo malo, se muere de hambre.
  O1 lo resuelve limpiando sólo cuando no queda nada útil y el golpe es costeable. Eso se prueba en i3 con el valor aprendido del
  bicho (`carros_limpia.py`).

**Tanda i3: limpieza costeable** (03:44–04:00 UTC; `carros_limpia.py`; identidad previa: WL == FAB OK):
`python experimentos/exploratorio_nube_20260924/corre_explora.py --brazos FAB,LIMC,MALC,RESC,VER_RESC,O1 --desde 24001 --n 6 --T 30000 --tag i3`

| brazo | R0 real | **linajes que persisten** | vida | muertes | mord. B+D | pasos sin nada bueno | gana a FAB |
|---|---|---|---|---|---|---|---|
| FAB | 0.149 | 1/54 | 66 | 116 | 465 | 0.000 | — |
| LIMC (FABRICA + limpieza costeable) | 0.154 | 0/54 | 67 | 106 | 444 | 0.000 | 4/6 (+0.006) |
| MALC (veta lo malo salvo limpieza costeable) | 0.112 | 5/54 | 200 | 51 | 59 | 0.087 | 2/6 |
| **RESC** (neo 0.5 + MALC) | 0.146 | **17/54** | 200 | 49 | 54 | 0.062 | 3/6 |
| VER_RESC | 0.101 | 14/54 | 200 | 50 | 58 | 0.120 | 2/6 |
| O1 | 0.775 | 20/54 | 3454 | 5 | 106 | 0.036 | 6/6 |

Lectura:
- **En R0 real, la limpieza costeable no cambia nada.** Se usa poco: 4–40 limpiezas por corrida, porque "no queda nada útil en el
  mundo" casi nunca se cumple.
- **La regla completa de la reserva (RESC) sí cambia la PERSISTENCIA.** Pasa de 1/54 a 17/54 linajes-semilla sin fundadores tras
  t = 10 000 (ENMIENDA 6), cerca de O1 (20/54). El resultado es BIMODAL: un tercio de los linajes se estabiliza; el resto muere como
  FABRICA (vida 200: una mordida mala al nacer, y hambre). La mediana del R0 no lo ve.
- **Siguiente:** medir RESC con T = 100 000, el horizonte de la carrera, contra FAB, APR y O1.
  - Mirar por linaje: ¿los linajes estables son los que aprendieron A/C antes de probar lo malo?
  - Candidato a la pieza "neofobia regulada por la reserva" del informe de v14.3.

### (i) sobre el candidato v14.3: la pieza que su creador propuso (neofobia regulada por la reserva)
El INFORME de v14.3 (`experimentos/tronco_v14_3/INFORME_v143.md`, "Qué queda") propone como pieza que falta *"neofobia regulada por la
reserva: la boca se contiene ante un código poco familiar (ncod bajo y valor lento ≈ 0) cuando min(E, Ag) es bajo"*. Se probó sin tocar
V143.py: `carros_v143_reserva.py` lo carga por ruta y corrige la decisión ya tomada por su boca (no consume rng). Arnés: WV143 == V143 bit a
bit en la física de los 9 linajes y la pista (24098 y 24099). Dos definiciones de "desconocido":
- NEO5 (la del creador, por cuerpo): ninguna fila familiar por la vía rápida y |valor| < 0.3 en las dos filas; veta si r = min(E, Ag) < 0.5.
- NEOL5 (por linaje): la letra nunca fue sentida por el linaje (no está en la tabla `_adS` de APR); veta si r < 0.5.
- NEOINF: control de NEO5 que veta siempre, sin reserva.
En los tres, si la letra es mala conocida del linaje decide la opción TD de APR y la regla no la pisa.

`python experimentos/exploratorio_nube_20260924/corre_explora.py --brazos V143,V143_NEO5,V143_NEOL5,V143_NEOINF,O1,FAB --desde 24011 --n 2 --T 100000 --tag v143a`
(y `--desde 24013 --tag v143b`, `--desde 24015 --tag v143c`; 10:15–10:34 UTC, tres procesos). Semillas 24011–24016, T 100 000.

| brazo | R0 real (mediana) | por semilla | linajes que persisten | vida | fundadores | gana a V143 |
|---|---|---|---|---|---|---|
| FAB | 0.149 | 0.160 · 0.141 · 0.160 · 0.149 · 0.148 · 0.145 | 0/54 | 66 | 318 | 0/6 |
| **V143** | **0.587** | 0.396 · 0.784 · 0.593 · 0.564 · 0.580 · 0.641 | 37/54 | 600 | 19.5 | — |
| V143_NEO5 | 0.449 | 0.597 · 0.323 · 0.482 · 0.181 · 0.416 · 0.585 | 31/54 | 366 | 30.5 | 1/6 (−0.138) |
| V143_NEOL5 | 0.420 | 0.422 · 0.419 · 0.221 · 0.644 · 0.210 · 0.947 | 33/54 | 400 | 25 | 3/6 (−0.169) |
| V143_NEOINF | 0.000 | (todas 0: muere de hambre sin probar nada) | 0/54 | 600 | 166 | 0/6 |
| O1 | 0.944 | 0.944 · 0.944 · 0.952 · 0.950 · 0.941 · 0.933 | 47/54 | 3293 | 0 | 6/6 (+0.360) |

**Lectura (exploratoria): la pieza propuesta NO ayuda a v14.3; lo empeora.**
- V143 en estas semillas reproduce lo del PC (0.587 contra 0.63 en la serie 14301).
- NEO5 baja el R0 a 0.449 y gana en 1 de 6; NEOL5, a 0.420. Suben los fundadores (30.5 y 25 contra 19.5): más linajes se extinguen.
- Por qué, probablemente (no medido por tipo de cuerpo): para un fundador limpio TODO es desconocido, incluida la comida; un hijo sólo
  sabe lo que le enseña el nodo del linaje (las últimas 20 mordidas de cada cuerpo muerto, leídas por la vía lenta), y por H-NEUTRAS las
  entradas neutras del nodo cancelan parte de eso. La neofobia frena también probar A y C cuando la reserva baja de 0.5, y el que nace
  con dote 0.6 llega ahí en 100 pasos. NEOINF lo muestra en el extremo: sin probar nada, todos mueren de hambre.
- O1 no tiene ese problema porque aprende cada letra de UNA mordida y lo guarda en el linaje. Lo que le falta a v14.3 no parece ser
  contención ante lo nuevo, sino saber desde el nacimiento qué es qué. Eso es lo que midió n10c (la familia pasa lo que importa). Siguiente
  exploratorio: `carros_v143_familia.py` (nodo sin neutras; tabla del padre con y sin neutras; control barajado). Arnés WF143 == V143 OK.

## Revisión de la alarma del §8 de n10b (RES > ORÁCULO 20/20 en la serie 12701–12720)
`python experimentos/exploratorio_nube_20260924/revisa_n10b_oraculo.py --desde 12794 --n 4` (02:35–02:57 UTC). Semillas de práctica de
n10b 12794–12797, T 100 000. Es `corre_n10b.tarea` sin tocar; sólo cambia el módulo del carro.
JSON: `datos/revisa_n10b_oraculo_s12794-12797_T100000_20260924_023525.json`.
El script se amplió después (brazos por argumento, RES_SIN0). Con los 4 brazos por defecto da lo mismo; este es el comando para
reproducirlo: `--brazos NADA,RES,ORACULO,ORA_SIN0 --desde 12794 --n 4`.

| carro | R0 de nacidos (mediana) | por semilla |
|---|---|---|
| NADA | 0.094 | 0.098 · 0.104 · 0.084 · 0.089 |
| ORÁCULO (tabla verdadera, 8 entradas) | 0.530 | 0.529 · 0.477 · 0.532 · 0.538 |
| RES (tabla de la familia) | 0.714 | 0.801 · 0.644 · 0.782 · 0.646 |
| **ORA_SIN0 (tabla verdadera SIN las 4 entradas neutras)** | **0.997** | 0.962 · 1.019 · 0.995 · 1.000 |

Pareados: ORA_SIN0 > ORÁCULO 4/4 (+0.46) · ORA_SIN0 > RES 4/4 (+0.28) · RES > ORÁCULO 4/4 (+0.21).

**Lectura (exploratoria):** H-NEUTRAS se sostiene.
- **El ORÁCULO no era un techo.** La tabla verdadera daña por sus entradas neutras. Quitadas, el mismo conocimiento verdadero lleva el
  R0 de los nacidos a ~1.0 en el mundo de flujo fijo (el de ERR-104, donde el 23-sep ningún carro persistía).
- **La alarma del §8 de n10b tiene explicación mecánica, no de instrumento.** RES le gana al ORÁCULO porque sus tablas incompletas
  (6–7 claves) suelen no traer las neutras.
- **Ojo a dos números redondos, pendientes de revisar.**
  - La vida mediana de los nacidos muertos es 600 en RES (dos semillas). Es lo que vive un recién nacido que nunca come (0.6 / 0.001).
  - En ORA_SIN0 es ~1401.
- **Siguiente:** RES_SIN0 (la familia pasa lo que vivió, sin lo neutro), en semillas exploratorias 24001–24004. Si se acerca a ORA_SIN0,
  la familia se sostiene con su propio conocimiento: candidato a preregistro (n10c).

### RES_SIN0: la familia pasa lo que vivió, sin lo neutro
`python experimentos/exploratorio_nube_20260924/revisa_n10b_oraculo.py --brazos NADA,RES,RES_SIN0,ORA_SIN0 --desde 24001 --n 4`
(02:57–03:23 UTC). Semillas exploratorias 24001–24004, T 100 000. RES_SIN0 es FAMB_RES, cuya `nace` descarta las entradas con R = 0 de
la tabla recibida.

| semilla | NADA | RES | **RES_SIN0** | ORA_SIN0 |
|---|---|---|---|---|
| 24001 | 0.064 | 0.651 | **0.911** | 0.985 |
| 24002 | 0.131 | 0.794 | **0.960** | 0.947 |
| 24003 | 0.092 | 0.692 | **0.974** | 1.003 |
| 24004 | 0.092 | 0.551 | **0.960** | (ver el JSON) |

**Lectura (exploratoria):**
- **RES_SIN0 > RES en 4/4, todas ≥ 0.91, y ≈ ORA_SIN0.** La familia, con lo que ella misma vivió, transmite casi lo mismo que la verdad
  cuando no pasa lo neutro. Lo hace en el mundo de flujo fijo.
- **Mecanismo propuesto:** transmitir sólo lo que tiene consecuencia conserva la generalización protectora.
- **No medido aún:** la persistencia del carro (`persiste_carro`) y el MIX.
- **Candidato a preregistro (n10c):**
  - brazos: RES_SIN0 contra RES, BAR_SIN0 (control de contenido que puede ganar), NADA y ORA_SIN0;
  - MIX;
  - semillas nuevas, serie y réplica;
  - la persistencia como medida co-principal.

## (ii) Aprender prediciendo
Idea: aprender sin morder, prediciendo el mundo. El carro `CarroPred` (`carros_predice.py`) lleva un órgano que observa, para cada letra
a la vista, cuánto tarda en desaparecer (tasa de riesgo por letra, media exponencial, ETA_H 0.01). Una letra que desaparece más rápido que
la media (ρ ≥ 1.25) es una que los otros comen; una que se queda (ρ ≤ 0.80), una que los otros evitan. El órgano sólo corrige la
neofobia de RES: permite probar lo desconocido que "los otros comen" aunque la reserva esté baja (pred_permite) y veta lo desconocido que
"los otros evitan" (pred_veta). Controles: RESP (el órgano observa pero no se lee: == RES bit a bit, arnés) y PRED_BAR (letras permutadas
en la lectura del órgano: control de contenido).

`python experimentos/exploratorio_nube_20260924/corre_explora.py --brazos FAB,RESP,PRED,PRED_BAR,O1 --desde 24001 --n 3 --T 30000 --tag ii1a`
y la misma con `--desde 24004 --tag ii1b` (09:45–09:57 UTC, dos procesos). Semillas 24001–24006, T 30 000.
JSON: `datos/explora_ii1a_…_094529.json` y `datos/explora_ii1b_…_094529.json`.

| brazo | R0 real (mediana) | por semilla | linajes que persisten | pasos sin nada bueno en el mundo |
|---|---|---|---|---|
| FAB | 0.149 | 0.152 · 0.144 · 0.164 · 0.147 · 0.167 · 0.120 | 1/54 | 0.000 |
| RESP (== RES) | 0.116 | 0.125 · 0.085 · 0.078 · 0.139 · 0.127 · 0.106 | 7/54 | 0.082 |
| **PRED** | **0.086** | 0.091 · 0.081 · 0.122 · 0.082 · 0.077 · 0.103 | **0/54** | 0.112 |
| PRED_BAR | 0.049 | 0.016 · 0.094 · 0.032 · 0.111 · 0.046 · 0.053 | 6/54 | 0.067 |
| O1 | 0.775 | 0.833 · 0.667 · 0.833 · 0.800 · 0.500 · 0.750 | 20/54 | 0.036 |

Pareados contra RESP: PRED gana 1/6 (−0.019); PRED_BAR gana 1/6 (−0.050).

**Lectura (exploratoria): negativo en este diseño.**
- Predecir qué comen los otros no ayuda: PRED queda por debajo de RES y no persiste ningún linaje (0/54 contra 7/54).
- El contenido sí importa (PRED_BAR es el peor en R0), pero en la dirección que daña: el órgano veta más de lo que permite (pred_veta
  533–744 por corrida contra pred_permite 126–159, 6 semillas) y el mundo se tapa más (0.112 de pasos sin nada bueno contra 0.082).
- La razón probable: en esta pista lo que desaparece rápido no es sólo lo bueno. Morder lo malo también lo quita (es limpieza), y
  FABRICA muerde mucho lo malo. La señal "los otros lo comen" está contaminada por la conducta de los otros.
- No se sigue por aquí esta noche. Si se retoma, la predicción tendría que ser de la consecuencia (ΔE del que muerde, visible), no de la
  desaparición.

## (iii) Propio
_(pendiente)_
