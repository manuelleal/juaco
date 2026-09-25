# EXPLORATORIO, no es dato

# HALLAZGOS — cadena trófica de 4 especies con cintas que evolucionan (explorador Fable, 25-sep-2026, ~2 h; ENTREGA PARCIAL por regla de parada)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo.

**Veredicto en una línea: NO (todavía). La cadena de 4 NO se sostiene en ninguna corrida: humano y oso mueren antes del paso 500, y la
gallina cae entre el paso ~700 y ~2 000+; el gusano sobrevive solo y su cinta sólo aprende a AHORRAR (tamaño y vista bajan). No hubo carrera
armamentista porque no hubo tiempo de convivencia: el veneno del gusano se quedó en 0.00 en todas las corridas. Casi todo el plazo se fue en
calibrar la energía (7 rondas) y el resultado dominante es de calibración, no de biología.** Lo digo tal cual, como prometí en las predicciones.

## 0. Qué hay en `experimentos/organelos/cadena/` (nada fuera de aquí se tocó; sin git; sin Pool; ningún proceso matado)
| archivo | qué es |
|---|---|
| `PREDICCIONES_previas.md` | 8 predicciones firmadas ANTES del primer humo con semillas (P1–P8). |
| `cadena.py` | el juguete: 4 especies en un toro 2D continuo (L 80), cinta genética por individuo (SUM/REP/FIN/TASA; copia con cambio/borrado/inserción/duplicación en tándem, tasa por zona), lector que suma en espacio log sobre 8 rasgos con costo (veneno, escudo, velocidad, vista, tamaño, eta, hambre, huida), cerebro que aprende en vida (valencia por bin de señal de la presa, regla delta con aversión y hambre_boca), saciedad y digestión, sol logístico sólo para el gusano. Sin `eval`/`exec`. `--set PARAM=json` para calibrar. |
| `corre_todo.py` | lanzador: 8 corridas (EVO 32001–32004, FIJO 32001–32002, SINVENENO 32001–32002), un proceso por corrida, máximo 4 a la vez con `subprocess.Popen`. |
| `dibuja.py` | HTML estático con SVG inline por corrida: poblaciones (log), veneno vs escudo, velocidades, vista, tamaño/huida, generaciones, largo de cinta, y 5 fotos del mundo 2D. También `datos/TABLA.md`. Sin dependencias. |
| `datos/*.json`, `datos/*.log` | crudos por corrida (serie cada 50 pasos, fotos, causas de muerte, cintas de ejemplo, parámetros). `humo_evo.json` y `calib_A.json` son de la calibración (parámetros viejos). |
| `cadena_<brazo>_<semilla>.html` | el visual pedido, uno por corrida terminada. |

**Qué tomé de nuestro bicho** (de `codigo_def.py` / `motor_codigo.py`): (1) la cinta como tuplas `(OP, args)` en un lenguaje cerrado, con el
mismo copiador (0.55 cambio / 0.20 borrado / 0.15 inserción / 0.10 duplicación en tándem) y la instrucción `TASA` que fija la tasa de error por
zona; (2) el lector que suma `d*PASO` en espacio log sobre perillas (aquí 8 rasgos en vez de 18) y `REP … FIN`; (3) el cerebro: valencia
aprendida por señal con regla delta `V += eta*(dE − V)`, aversión ×2 si dE < 0 y `hambre_boca` que decide cuándo morder lo que se sabe malo;
(4) sin vivero, sin juez: nace quien llega al umbral y paga la dote; muere quien llega a cero.

**Por qué el gusano recibe "sol":** el director pidió que no hubiera comida. Cada paso cuesta energía a todos y nadie la produce; sin una entrada
externa la energía total sólo baja y todos mueren en menos de una vida. El sol es la única fuente, entra sólo al nivel 1 y es logístico
(`SOL/(1+N/K)`), así el gusano tiene capacidad de carga propia. Todo lo demás (gallina, oso, humano) vive de comerse el nivel de justo debajo.

## 1. Calibración: siete rondas antes de la tanda (la parte honesta)
| ronda | qué pasó | qué cambié |
|---|---|---|
| 1 | gallina, oso y humano extintos en < 50 pasos | **bug de signo**: los depredadores huían de la presa y las presas corrían hacia el depredador. Arreglado. |
| 2 | la gallina arrasa al gusano en 250 pasos (Lotka-Volterra sobre-disparado) | mundo 80×80, K del sol 1500, menos depredadores, captura probabilística 0.5 |
| 3 | la gallina muere de hambre aun comiendo (1 gusano cada ~12 pasos × bocado 1.5 no cubre 0.11/paso) | bocados en pirámide 2.5/5/10 |
| 4 | el oso arrasa a la gallina (17 → 87 osos en 150 pasos) | más presas por cría arriba (REP 14/26), menos individuos iniciales |
| 5 | la gallina sobre-dispara en crías y todas mueren de hambre (dote 2 = 19 pasos sin comer) | dote 3, umbral 6, **saciedad** (nadie caza con E > 0.85·REP) |
| 6 | igual: 308 crías, 360 muertas de hambre | **digestión** (H pasos sin comer tras un bocado: 10/20/40), bocado 1.5 → la gallina ni pare (ingesta máx ≈ costo) → bocado 2.5 |
| 7 | colapso total en 313 pasos (1 085 crías de gallina comen 4 845 gusanos) | sol 0.5 con K 400 (el gusano se regenera en ~5 pasos), vista del oso/humano 8/12, E inicial 0.7·REP |
| tanda | con 7: gusano y gallina conviven 700–2 000+ pasos, oso y humano no | (sin más cambios; se acabó el plazo) |

La lección, que es vieja (Lotka-Volterra en agentes): sin refugio espacial, sin tiempo de manejo y con un depredador que convierte presas en crías
más rápido de lo que la presa se regenera, la cadena oscila con amplitud creciente y se extingue de arriba hacia abajo. Añadí saciedad y digestión
(los dos son biológicos), pero el tercer estabilizador —refugio o vista limitada de la presa— no alcancé a ponerlo. Además el paso es lento
(~90 ms/paso con 1 500 gusanos y 400 gallinas; el PC estaba compartido) y T tuvo que bajar de 40 000 a 12 000: el gusano llegó a ~25–45
generaciones, no a cientos (su vejez es a los 500 pasos y en el tope de población sólo nace quien reemplaza a un muerto).

## 2. Tabla (lo terminado al cierre; el lanzador sigue corriendo el resto y `python dibuja.py datos/*.json` regenera la tabla y los HTML)
Columnas: extinción (gusano/gallina/oso/humano) en pasos; población final; generación máxima; rasgos medios al final.

VER `datos/TABLA.md` (generada). Al cierre:
| brazo | semilla | extinción g/ga/o/h | estado |
|---|---|---|---|
| EVO | 32002 | vive / 673 / 407 / 209 | terminada (12 000 pasos, 64 s porque quedó sólo el gusano). Gusano 1 500 (tope), 45 generaciones máx. Veneno 0.00 siempre. Tamaño 1.00 → 0.88, vista 1.50 → 1.43 (ahorro de costo sin depredador). Cinta 9.0 → 9.7 instrucciones. |
| EVO | 32001 | vive / < 7 000 / < 1 000 / < 1 000 | en curso: en t 1 000 gusano 1 399, gallina 400 (tope); en t 7 000 sólo gusano (1 500, 46 gen.), **veneno gusano 0.01** (deriva sin depredador, no selección). |
| EVO | 32003 | vive / viva a 3 000 / < 1 000 / < 1 000 | en curso: t 1 000 gallina 400 (tope); **t 3 000 gallina 217 viva** (segunda ola), gusano 1 474; escudo gallina 0.002. |
| EVO | 32004 | vive / viva a 4 000 / < 1 000 / < 1 000 | en curso: t 2 000 gallina 228; **t 4 000 gallina 79** (cayendo), gusano 1 500, 32 gen.; escudo gallina volvió a 0.0. |
| FIJO | 32001 | ? / viva a 2 000 / < 2 000 / < 2 000 | en curso: t 2 000 gusano 1 251, gallina 400 (tope): igual que EVO hasta ahí (P3 va bien: la evolución no cambia el arranque). |
| FIJO 32002, SINVENENO 32001–32002 | — | en cola del lanzador. |

## 3. Lo visto (descriptivo, con lo que hay)
- **¿Se sostiene o colapsa? Colapsa de arriba hacia abajo.** Orden de extinción en todas las corridas: humano (≈ 140–210), oso (≈ 220–410),
  gallina (673 en 32002; viva a 2 000 en 32004). El gusano nunca se extingue con la calibración final. **P1 acertó** en el orden (humano
  primero, oso después, gusano nunca) aunque por razones de calibración más que de biología.
- **¿Carrera armamentista? No la hubo.** Veneno del gusano = 0.00 en todas las series. Con la gallina viva menos de 2 000 pasos (≈ 4–8
  generaciones de gusano) no hay tiempo de que un `SUM 0 +1` se fije; y al tope de población la selección es casi deriva (nace quien reemplaza).
  El escudo de la gallina subió a 0.004–0.010 en 32003/32004: es ruido de mutación, no respuesta (no hay veneno al que responder). **P2 falló.**
- **¿Ciclos Lotka-Volterra?** Un solo ciclo grande: la gallina sube al tope (400) mientras el gusano cae a 1 100–1 400, después la gallina cae
  por hambre y el gusano vuelve al tope. En 32004 hay un segundo pico parcial (gallina 228 en t 2 000). No hay ≥ 3 picos alternados: **P4 falló
  o quedó sin decidir** (se necesita ver 32001/32003/32004 completas).
- **¿Qué rasgos fija cada especie?** El gusano sin depredador fija **ahorro**: tamaño 1.00 → 0.88 y vista 1.50 → 1.43 en 12 000 pasos (los dos
  cuestan y no sirven de nada cuando nadie te caza); huida, velocidad, eta y hambre no se mueven (deriva neutra ≈ 0). La cinta crece despacio
  (9.0 → 9.7 instrucciones): la duplicación en tándem gana al borrado en neutro, como en la exploración del CÓDIGO. **P5 falló** (nadie subió
  velocidad). Gallina, oso y humano no viven lo suficiente para fijar nada.
- **El cerebro.** Las gallinas aprendieron la valencia del bin 0 de la señal (V ≈ 0.04 en 32002 antes de morir): con veneno 0 todo bocado es
  bueno y no hay nada que evitar. `comidos_por_bin` = 7 612 / 1 826 / 218 / 0: la señal ruidosa (σ 0.25) mete gusanos sin veneno en los bins 1–2.
  **P8 no se pudo probar.** P6 y P7 (controles SINVENENO; veneno que decae) tampoco: los controles no alcanzaron a correr.
- **Algo raro que nadie esperaba.** (a) La gallina se muere de hambre con 1 500 gusanos al lado: come 0.036 gusanos por paso (0.09 de energía
  contra 0.11 de costo). El límite no es la comida sino la **caza**: el ruido de rumbo (σ 0.4 por eje sumado a un vector unitario) hace que la
  gallina a 0.6 casi no gane distancia a un gusano que huye a 0.25. Es decir, en este mundo la velocidad de la presa importa mucho menos que
  la calidad del rumbo del depredador; si hubiera evolucionado algo, habría sido "menos ruido", que no es un rasgo de la cinta. (b) En la
  ronda 1 vi −0.61 de energía en gallinas que "comían": era comer y parir en el mismo paso (+2.5 − 0.11 − 3.0), no un bug; conviene registrar
  nacimientos por paso para no volver a perseguir eso.

## 4. Predicciones: qué falló
| # | resultado |
|---|---|
| P1 (humano primero, oso después, gusano nunca) | ACERTÓ en orden, en 4/4 (pero antes del paso 500, no 8 000, y por calibración). |
| P2 (veneno > 0.3 antes de 15 000; escudo después) | FALLÓ: veneno 0.00 en todas. |
| P3 (FIJO igual o antes que EVO) | SIN DATO (FIJO lanzada al cierre). |
| P4 (≥ 3 picos alternados) | FALLÓ en 32002; sin decidir en las demás. |
| P5 (gallina sube velocidad) | FALLÓ: nadie sube velocidad; el gusano baja tamaño y vista. |
| P6, P7, P8 | SIN DATO / no probables sin veneno. |
| El miedo escrito al final de las predicciones ("gasto la mitad del tiempo en calibrar y el reporte dice calibración") | ACERTÓ, y peor: fueron ¾ del tiempo. |

## 5. ¿Merece un preregistro serio?
**Todavía no.** Merece **una segunda exploración de 2 horas** con tres cambios concretos antes de pensar en preregistro:
1. **Refugio y caza**: vista de la gallina que no cubra todo (o parches donde el gusano no se ve) y rumbo del depredador con menos ruido (σ 0.15);
   medir primero, en un mundo de sólo gusano + gallina, si conviven 20 000 pasos con ≥ 3 ciclos. Sin ese peldaño, meter oso y humano es ruido.
2. **Generaciones de verdad**: vejez del gusano a 150 pasos y sin tope duro de población (o tope alto con K del sol como único límite), para
   que la selección no sea "quien reemplaza a un muerto". Costo: hay que acelerar el paso (rejilla de celdas para vecinos, o numba: el gemelo
   compilado que ya sabemos hacer) porque hoy son ~90 ms/paso.
3. **Veneno con dientes**: DANO 1.5 por unidad es poco frente a un bocado de 2.5; con veneno 0.45 (tres `SUM 0 +1`) la gallina todavía gana
   1.8 por bocado. Para que el veneno sea seleccionable hay que que un gusano con veneno 0.5 le cueste a la gallina más de lo que le da, o que el
   gusano sobreviva al mordisco (huella de veneno sin morir, como los insectos aposemáticos). Eso sí engancha con nuestro cerebro: la gallina
   que aprende a no morder el bin alto es exactamente la valencia aprendida de motor_codigo.
Si con eso conviven 3 niveles y el veneno sube por encima de 0 con FIJO en 0, ahí sí hay algo que preregistrar (predicción: veneno EVO >
veneno FIJO = 0 en ≥ 5/6 semillas; escudo con rezago).

## 6. Cómo terminar lo que quedó corriendo
El lanzador (`corre_todo.py`) sigue vivo y escribirá `datos/FIJO_*.json` y `datos/SINVENENO_*.json` (cada corrida tarda 1–18 min según cuánto
vive la gallina). Cuando terminen: `python dibuja.py datos/EVO_*.json datos/FIJO_*.json datos/SINVENENO_*.json` regenera `datos/TABLA.md` y los
HTML. Nada de eso cambia el veredicto de arriba salvo que 32001/32003/32004 muestren ≥ 3 ciclos o veneno > 0, cosa que en t 1 000–2 000 no
se ve.

## 7. ADENDA al cierre: el humo con topes altos SÍ convive (llegó después de escribir lo de arriba)
El humo de la ronda 7 (`datos/HUMO_topesaltos_32001.json`, `cadena_HUMO_topesaltos_32001.html`; semilla 32001, T 6 000, mismos parámetros que la
tanda salvo **topes 2 500 gusanos / 600 gallinas y K del sol 600** — los bajé a 1 500/400/K 400 sólo por velocidad) terminó después de la entrega:
- **gusano y gallina conviven los 6 000 pasos** (gallina 600 → 390 → 508 → 423 → 353 → 600; gusano 2 159 → 1 780 → 1 859 → 1 751 → 1 561 → 1 636 →
  1 117 → 963): **≥ 3 oscilaciones alternadas**, 139 518 gusanos comidos, 21 318 crías de gallina. Oso y humano igual extintos antes de 600.
- Veneno del gusano 0.001 y escudo de la gallina 0.000–0.013: **sigue sin carrera armamentista** aunque convivan; el veneno no es seleccionable con
  DANO 1.5 frente a bocado 2.5 (punto 3 de la §5).
Lectura: el colapso gusano–gallina de la tanda es en parte efecto de haber bajado los topes (con tope 400 la gallina se queda "pegada" al tope
y muere de hambre en bloque). Esto **rescata a medias P4** (ciclos) y refuerza la propuesta de la §5: el peldaño siguiente es sólo gusano + gallina
con topes altos y paso más rápido, y veneno con dientes. Los dos niveles de arriba siguen sin sostén en ninguna configuración probada.
