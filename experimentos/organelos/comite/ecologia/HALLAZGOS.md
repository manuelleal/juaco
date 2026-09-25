# EXPLORATORIO, no es dato

# HALLAZGOS — comité de exploración, carril B: LA VIDA EN GRUPO Y EL CICLO DE LA MATERIA (explorador B, 25-sep-2026, ~2 h)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas); el método manda sobre el cómo.

**Veredicto en una línea: HAY ALGO (exploratorio, no es dato). El bicho real sin vivero, sin fundadores repuestos y sin mutación se
sostiene con R0 de nacidos ≥ 1.0 cuando el mundo cierra el ciclo de la materia (lo tóxico se descompone en comida, COMPOST) y el padre
le pasa la tabla al hijo con filtro (ENSENA_F0): 5/5 en w9, CONFIRMADO en 5 semillas nuevas, y 5/5 en w30 con el linaje CRECIENDO
(75 cuerpos desde 30 fundadores, R0 1.19–1.28), donde el control sin mecanismo da 0/15. Sólo la descomposición, sin nada social,
rescata a veces (3/10 en w9; en w30 persiste 5/5 pero al filo). El doble de comida (control de regalo) NO rescata al ignorante (0/10)
y no hace crecer al que sabe (max vivos = fundadores). Lo que mata al linaje no es la falta de comida ni la ignorancia por sí solas: es
que **nadie come el veneno y el veneno tapa el mundo**.**

## 0. Qué hay en `comite/ecologia/` (sólo copias; sin git; sin Pool; ningún proceso matado; nada fuera de la carpeta se tocó)
| archivo | qué es |
|---|---|
| `PREDICCIONES_previas.md` | predicciones firmadas ANTES de cada tanda (P1–P9 antes de todo; P10–P14 tras el barrido w9 y antes de la descomposición; P15–P18 antes de la confirmación y w30). Se declaran una a una en §5. |
| `motor_ecologia.py` | COPIA de `juaco_eco/motor_eco3.py` con dos rutas cambiadas y los mecanismos marcados `# ECOLOGIA`, todos apagados por defecto (con `social=None` es motor_eco3 bit a bit: comprobado con la misma semilla, t_ext 1689 y 5 nacidos, antes y después de cada cambio). Sin `eval`/`exec`. |
| `corre_ecologia.py` | una corrida (un proceso): `MEC seed esc T`. Bicho `FAMB_ORG_ECO` con los órganos apagados (= `FABRICA_ECO` bit a bit: comprobado, misma semilla, mismos números), genoma de fábrica, `p_mut 0`, `refunda 0` (sin vivero desde el paso 0), quimiostato `fija` (r_rep 0.03·esc). |
| `lanza.py` | lanzador: `subprocess.Popen`, máximo 6 a la vez, salta lo ya hecho. |
| `lee.py` | tabla por mecanismo (CON contra SIN, misma semilla). `--md`, `--detalle`. |
| `datos/w9/`, `datos/w9_confirma/`, `datos/w30/`, `datos/humo/` | un JSON por corrida (`MEC_wESC_sSEMILLA.json`) + `.out` + `lanza.log`. |

**Medidas:** `persiste` = cuerpos vivos en T; **R0 nacidos** = hijos medios de los cuerpos NO fundadores nacidos hasta T − 10 000
(cohorte cerrada); **PARADA** = persiste y R0 ≥ 0.90; `max vivos`; vida media; causas de muerte; composición del mundo; llegadas
perdidas del quimiostato (el mundo lleno rechaza la comida que llega). Semillas 34001–34005 (barrido), 34011–34015 (confirmación),
34901 (práctica). T = 30 000 en w9 (9 fundadores, L 360, 36 objetos); T = 20 000 en w30 (30 fundadores, L 1 200, 120 objetos).

## 1. Los mecanismos (reglas locales del mundo o del parto; las reglas del cerebro NO cambian)
| clave | qué hace | de dónde |
|---|---|---|
| SIN | control | — |
| ENSENA | el padre pasa su tabla al hijo en el parto (órgano `ensena` de FAMB_ORG_ECO, ya construido) | "familia comparte lo aprendido" |
| ENSENA_F0 | ENSENA + el hijo quita lo neutro de la tabla (`filtra0`) | gramática FIJO:filtra0 |
| VIDA | enseñar EN VIDA: parientes a ≤ 3 celdas; el mayor "enseña": los otros mueven su vía lenta (Wps, Wns) hacia la del mayor con λ 0.1 cada paso. Toca el ESTADO del carro desde el mundo (declarado). | Prometeo |
| CADAVER | el muerto deja en su celda (o la libre más cercana a ≤ 3) un objeto con el recurso que le quedaba: 'C' si murió sin E con Ag ≥ 0.4; 'A' si murió sin Ag con E ≥ 0.4 | ficha 13 |
| BOLSA / BOLSA_TODOS | tras los costos, cuerpos del mismo linaje (o de cualquiera) a ≤ 1 celda promedian E y Ag | ficha 4 + control de parentesco |
| NICHO / NICHO_AZAR | la llegada del quimiostato cae a ≤ 10 celdas de donde alguien mordió B/D en los últimos 200 pasos / de un cuerpo vivo al azar. El flujo total no cambia. | localidad y territorio + control |
| **COMPOST** | un objeto B/D con ≥ 500 pasos de edad se vuelve A/C (B→A, D→C): el ciclo de la materia. Agregado tras ver que en ENSENA_F0 el mundo se llena de B/D (predicciones P10–P12 firmadas antes de correrlo). **Zona gris declarada:** propiedad del mundo, no del bicho; da más comida efectiva. Por eso lleva dos controles: | ficha 13 llevada al veneno |
| BORRA | control: el B/D viejo desaparece (sólo libera la celda; no da comida) | control |
| FLUJO2 | control de regalo: el doble de llegadas (r_rep 0.06), sin descomposición. Si esto rescata igual, COMPOST es sólo "más comida". | control |

Apoptosis / vejez regulada: **no se probó** (declarado). Con el bicho de fábrica muriendo a los 600 pasos y R0 0, quitar viejos no
tiene a quién ayudar; queda para el bicho que ya persiste.

## 2. Tabla w9 (semillas 34001–34005, T 30 000; CON contra SIN, misma semilla). Generada por `lee.py datos/w9 --md`.
| mecanismo | n | persisten | R0>=0.9 | PARADA | R0 med | t_ext med | max vivos med | vivos T med | nacidos med | vida med | gen max med | fraccion mordidas malas | vive mas que SIN (misma semilla) | seg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SIN | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 2825 | 9 | 0 | 5 | 598 | 1 | 0.38 | 0/5 | 6 |
| BOLSA | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 2179 | 9 | 0 | 4 | 560 | 1 | 0.39 | 0/5 | 4 |
| BOLSA_TODOS | 5 | 0/5 | 0/5 | 0/5 | 0.25 | 2837 | 9 | 0 | 4 | 838 | 2 | 0.38 | 3/5 | 6 |
| BORRA | 5 | 0/5 | 0/5 | 0/5 | 0.25 | 10585 | 9 | 0 | 21 | 674 | 2 | 0.23 | 3/5 | 12 |
| CADAVER | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 3317 | 9 | 0 | 6 | 624 | 1 | 0.37 | 3/5 | 5 |
| CADAVER+COMPOST | 5 | 1/5 | 1/5 | 1/5 | 0.59 | 8976 | 9 | 0 | 22 | 768 | 4 | 0.21 | 5/5 | 20 |
| **COMPOST** | 5 | **3/5** | 3/5 | **3/5** | 0.93 | 30000 | 9 | 1 | 76 | 707 | 4 | 0.18 | 5/5 | 29 |
| ENSENA | 5 | 0/5 | 0/5 | 0/5 | 0.33 | 5592 | 9 | 0 | 10 | 720 | 3 | 0.34 | 3/5 | 8 |
| ENSENA+BOLSA | 5 | 0/5 | 1/5 | 0/5 | 0.20 | 3882 | 9 | 0 | 8 | 718 | 2 | 0.38 | 4/5 | 12 |
| ENSENA+CADAVER | 5 | 0/5 | 0/5 | 0/5 | 0.40 | 3978 | 9 | 0 | 10 | 667 | 2 | 0.36 | 4/5 | 8 |
| ENSENA+CADAVER+BOLSA | 5 | 0/5 | 0/5 | 0/5 | 0.44 | 4990 | 9 | 0 | 9 | 868 | 3 | 0.35 | 4/5 | 13 |
| **ENSENA+COMPOST** | 5 | **5/5** | 5/5 | **5/5** | 1.03 | 30000 | 10 | 6 | 160 | 879 | 21 | 0.23 | 5/5 | 94 |
| ENSENA+NICHO | 5 | 0/5 | 0/5 | 0/5 | 0.43 | 3558 | 9 | 0 | 7 | 706 | 2 | 0.37 | 4/5 | 7 |
| ENSENA+VIDA+CADAVER | 5 | 0/5 | 0/5 | 0/5 | 0.17 | 4821 | 9 | 0 | 10 | 628 | 2 | 0.35 | 3/5 | 7 |
| ENSENA_F0 | 5 | 2/5 | 2/5 | 2/5 | 0.86 | 13731 | 9 | 0 | 22 | 1374 | 8 | 0.25 | 5/5 | 32 |
| **ENSENA_F0+BORRA** | 5 | **5/5** | 5/5 | **5/5** | 1.10 | 30000 | 19 | 13 | 179 | 1671 | 16 | 0.15 | 5/5 | 160 |
| ENSENA_F0+CADAVER | 5 | 3/5 | 3/5 | 3/5 | 0.94 | 30000 | 9 | 2 | 60 | 1390 | 12 | 0.20 | 4/5 | 34 |
| **ENSENA_F0+CADAVER+COMPOST** | 5 | **5/5** | 5/5 | **5/5** | 1.10 | 30000 | 27 | 22 | 294 | 1739 | 16 | 0.14 | 5/5 | 247 |
| **ENSENA_F0+COMPOST** | 5 | **5/5** | 5/5 | **5/5** | 1.13 | 30000 | 27 | 18 | 276 | 1728 | 17 | 0.14 | 5/5 | 234 |
| ENSENA_F0+FLUJO2 | 5 | 4/5 | 4/5 | 4/5 | 1.00 | 30000 | 9 | 2 | 58 | 1376 | 14 | 0.19 | 4/5 | 38 |
| FLUJO2 | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 2053 | 9 | 0 | 4 | 575 | 1 | 0.36 | 2/5 | 5 |
| NICHO | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 2018 | 9 | 0 | 3 | 587 | 1 | 0.40 | 2/5 | 5 |
| NICHO_AZAR | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 2113 | 9 | 0 | 5 | 632 | 1 | 0.38 | 2/5 | 5 |
| VIDA | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 2322 | 9 | 0 | 5 | 632 | 1 | 0.38 | 1/5 | 5 |
| VIDA+ENSENA | 5 | 0/5 | 0/5 | 0/5 | 0.10 | 4752 | 9 | 0 | 10 | 669 | 2 | 0.36 | 4/5 | 6 |

Detalle que sostiene la lectura (de `lee.py datos/w9 --detalle`, semillas que persisten):
- **SIN:** vida 540–850; causas veneno/sal 100 %; 38 % de las mordidas son B/D; máximo 10 nacidos; generación máxima 1.
- **ENSENA_F0 (2 que persisten):** el mundo queda con **B 17 + D 14 de 36 objetos** y el quimiostato pierde **6 364 de 8 100 llegadas
  (79 %)**: la comida llega y no cabe. Vivos en T: 3–4. Es persistir a duras penas.
- **ENSENA_F0+COMPOST:** las llegadas perdidas bajan a ~3 000 (38 %); 260–290 nacidos; 16–20 vivos en T; máximo 26–29; 15–19
  generaciones; vida media 1 600–1 800; sólo 13–15 % de mordidas malas. Aun así las muertes siguen siendo por sal/veneno (el hambriento
  muerde lo que sabe malo) y ahora aparece la sed (26–53 por corrida): el agua es el cuello siguiente.
- **COMPOST solo (3 que persisten):** 76–78 nacidos, R0 0.93–1.04, pero 1–2 vivos en T y vida media 520–810: el linaje va al filo. El
  mundo queda equilibrado (A 8, B 10, C 8, D 10): el compost repone A/C tanto como el flujo.
- **FLUJO2 (doble comida, sin compost): 0/5**, t_ext mediana 2 053: peor que SIN en la mediana. El doble de flujo trae el doble de veneno.
- **ENSENA_F0+FLUJO2:** persiste 4/5 con R0 1.00, pero **max vivos 9, 2 vivos en T**: no crece. COMPOST con la misma enseñanza: 27.

## 3. Confirmación (semillas nuevas 34011–34015, w9, T 30 000) y w30 (34001–34005, T 20 000)

### 3a. Confirmación w9, semillas 34011–34015 (`lee.py datos/w9_confirma --md`)
| mecanismo | n | persisten | R0>=0.9 | PARADA | R0 med | t_ext med | max vivos med | vivos T med | nacidos med | vida med | gen max med | fraccion mordidas malas | vive mas que SIN (misma semilla) | seg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SIN | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 1502 | 9 | 0 | 3 | 605 | 1 | 0.42 | 0/5 | 4 |
| BORRA | 5 | 1/5 | 1/5 | 1/5 | 0.17 | 6584 | 9 | 0 | 11 | 727 | 2 | 0.26 | 4/5 | 13 |
| COMPOST | 5 | 1/5 | 1/5 | 0/5 | 0.81 | 11970 | 9 | 0 | 28 | 773 | 6 | 0.20 | 5/5 | 24 |
| ENSENA+COMPOST | 5 | 4/5 | 4/5 | 4/5 | 0.98 | 30000 | 10 | 6 | 160 | 871 | 16 | 0.24 | 5/5 | 89 |
| ENSENA_F0 | 5 | 4/5 | 4/5 | 4/5 | 1.02 | 30000 | 9 | 3 | 61 | 1373 | 12 | 0.19 | 5/5 | 45 |
| **ENSENA_F0+BORRA** | 5 | **5/5** | 5/5 | **5/5** | 1.10 | 30000 | 19 | 11 | 184 | 1621 | 17 | 0.15 | 5/5 | 156 |
| **ENSENA_F0+CADAVER+COMPOST** | 5 | **5/5** | 5/5 | **5/5** | 1.09 | 30000 | 28 | 22 | 300 | 1648 | 16 | 0.14 | 5/5 | 242 |
| **ENSENA_F0+COMPOST** | 5 | **5/5** | 5/5 | **5/5** | 1.06 | 30000 | 29 | 16 | 283 | 1792 | 17 | 0.14 | 5/5 | 251 |
| ENSENA_F0+FLUJO2 | 5 | 1/5 | 1/5 | 1/5 | 0.50 | 3891 | 9 | 0 | 6 | 898 | 4 | 0.31 | 4/5 | 20 |
| FLUJO2 | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 2120 | 9 | 0 | 5 | 493 | 1 | 0.40 | 5/5 | 5 |

**Las 10 semillas juntas (w9, PARADA = persiste y R0 ≥ 0.90):**
| mecanismo | PARADA /10 | lectura |
|---|---|---|
| SIN | **0/10** | el bicho de fábrica sin vivero muere siempre antes de 6 000 pasos |
| FLUJO2 (doble comida) | 0/10 | más comida sin descomposición no hace nada |
| BORRA (lo tóxico desaparece) | 1/10 | liberar la celda sin dar comida casi no ayuda al ignorante |
| COMPOST (lo tóxico se vuelve comida) | 3/10 (persiste 4/10; una con R0 0.98 murió en 24 719) | rescata a veces, al filo: 1–2 vivos |
| ENSENA_F0 (padre pasa la tabla filtrada) | 6/10 | persiste a duras penas: 3–4 vivos, mundo tapado, 79 % de la comida perdida |
| ENSENA_F0+FLUJO2 | 5/10 | el doble de comida no le agrega nada a la enseñanza (max vivos 9) |
| ENSENA+COMPOST (sin filtro) | 9/10 | |
| ENSENA_F0+BORRA | **10/10** | con enseñanza, basta con que lo tóxico deje de tapar (19 cuerpos) |
| ENSENA_F0+COMPOST | **10/10** | lo mismo y el mundo se puebla: 27–29 cuerpos, 17 generaciones, R0 1.06–1.13 |
| ENSENA_F0+CADAVER+COMPOST | **10/10** | el cadáver no agrega nada medible sobre lo anterior (max 28 contra 29) |

Regla de parada: **cumplida** por ENSENA_F0+COMPOST (y por ENSENA_F0+BORRA) en 5/5 + 5/5 contra SIN 0/5 + 0/5. Se paró el barrido
en w9 y se dejó w30 sólo para ver si el mundo grande cambia el cuadro.

### 3b. w30 (30 fundadores, T 20 000, semillas 34001–34005; `lee.py datos/w30 --md`)
| mecanismo | n | persisten | R0>=0.9 | PARADA | R0 med | t_ext med | max vivos med | vivos T med | nacidos med | vida med | gen max med | fraccion mordidas malas | vive mas que SIN (misma semilla) | seg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SIN | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 5140 | 30 | 0 | 16 | 566 | 1 | 0.35 | 0/5 | 14 |
| COMPOST | 5 | 5/5 | 2/5 | 2/5 | 0.79 | 20000 | 30 | 4 | 132 | 717 | 8 | 0.17 | 5/5 | 70 |
| ENSENA_F0 | 5 | 5/5 | 4/5 | 4/5 | 1.08 | 20000 | 30 | 9 | 118 | 1285 | 11 | 0.20 | 5/5 | 104 |
| ENSENA_F0+BORRA | 5 | 5/5 | 5/5 | 5/5 | 1.18 | 20000 | 47 | 40 | 371 | 1547 | 13 | 0.16 | 5/5 | 307 |
| **ENSENA_F0+COMPOST** | 5 | **5/5** | 5/5 | **5/5** | **1.23** | 20000 | **75** | **58** | **602** | 1630 | 14 | 0.14 | 5/5 | 505 |
| ENSENA_F0+FLUJO2 | 5 | 5/5 | 5/5 | 5/5 | 1.10 | 20000 | 30 | 11 | 113 | 1270 | 10 | 0.20 | 5/5 | 100 |
| FLUJO2 | 5 | 0/5 | 0/5 | 0/5 | 0.00 | 2904 | 30 | 0 | 14 | 558 | 1 | 0.39 | 2/5 | 14 |

Lectura de w30: con 30 fundadores el azar de extinción baja y **enseñar con filtro ya persiste solo 5/5** (4/5 con R0 ≥ 0.9), pero no
crece: `max vivos` = 30 = los fundadores, 9 vivos en T, mundo tapado (B 56 + D 46 de 120 objetos). El doble de comida (FLUJO2) le da
exactamente lo mismo (max 30, 11 vivos): más flujo no cabe. **Sólo cerrar el ciclo hace crecer al linaje: ENSENA_F0+COMPOST llega a
75 cuerpos (2.5× los fundadores), 600 nacidos, R0 1.19–1.28 en las 5, 14 generaciones.** COMPOST solo: 5/5 persisten pero al filo
(3–9 vivos, R0 0.56–1.03): sin la tabla heredada el bicho sigue pagando la lección (veneno/sal = 100 % de las causas). En
ENSENA_F0+COMPOST aparecen muertes por **sed** (72–88 por corrida) y hambre (12–29): con el veneno bajo control, el cuello siguiente
es el agua ('C' escasea: 8 de 120 objetos).

## 4. Lo mejor, en humano
1. **El veneno tapa el mundo.** En el quimiostato lo bueno se come y lo malo se queda. Un bicho que aprende a no morder B/D deja el
   mundo lleno de B/D, y la comida que llega se pierde porque no hay celda libre (79 % del flujo perdido en ENSENA_F0). El que no
   aprende (SIN) "limpia" mordiendo, y se muere de eso. Es la tragedia de los comunes al revés: limpiar cuesta 0.4 y el beneficio es de
   todos. Por eso el cruce H-1 dependía de la reposición INMEDIATA (ERR-104): allí morder B fabricaba comida al instante.
2. **Cerrar el ciclo de la materia rescata al linaje.** Si lo tóxico se descompone en comida (COMPOST), el bicho de fábrica tal cual,
   sin enseñanza y sin mutación, persiste 3/5 con R0 ≈ 1; con el padre que pasa la tabla filtrada, 5/5 y el mundo se puebla (27
   cuerpos, 17 generaciones). No es "más comida": el doble de flujo sin descomposición da 0/5. Lo que importa es que lo tóxico deje de
   ocupar el mundo (BORRA, que sólo libera la celda, da 5/5 con enseñanza pero no sin ella: la comida extra del compost sí pesa cuando
   el bicho es ignorante).
3. **Enseñar en el parto es necesario pero no basta, y enseñar en vida no ayuda.** ENSENA solo: 0/5; con filtro (F0): 2/5. El filtro
   importa (repite la gramática). VIDA (el mayor enseña a los cercanos cada paso) es neutro o daña: borra lo que el joven aprendió por su
   cuenta (la "sabia mentirosa" de la escuela de abejas).
4. **Lo que no pesa aquí:** bolsa común (nunca hay parientes juntos si no hay hijos; entre extraños alarga la vida 560→838 pero no salva),
   cadáver (alarga el linaje ~1 000 pasos, da +1 persistencia sobre ENSENA_F0, pero no cierra el ciclo porque la comida ya sobraba: se
   perdía por falta de celda), nicho (dónde cae la comida no importa si no cabe).

## 5. Predicciones: qué falló
| # | resultado |
|---|---|
| P1 SIN 0/5 | ACERTÓ (w9). |
| P2 ENSENA solo persiste ≥ 3/5 en w30, ≤ 2/5 en w9 | w9 0/5 acertó; w30 (ver §3). |
| P3 CADAVER solo ≤ 1/5 | ACERTÓ (0/5). |
| P4 BOLSA y BOLSA_TODOS 0/5 | ACERTÓ. |
| P5 VIDA ≤ 1/5 | ACERTÓ (0/5); peor: con ENSENA daña. |
| P6 NICHO = NICHO_AZAR = SIN | ACERTÓ (0/5 los tres). |
| P7 ENSENA+CADAVER ≥ 4/5 con R0 ≥ 0.9 en w30 (la parada) | **REFUTADA en w9** (0/5); w30 no se corrió con esa combinación: la parada la dio otro mecanismo. |
| P8 CADAVER sube max_vivos sobre ENSENA | REFUTADA: max 9 en ambos. |
| P9 (miedo) sólo enseñar mueve la aguja | **REFUTADA**: lo ecológico (COMPOST) mueve más que enseñar, y solo. |
| P10 COMPOST solo no rescata (0/5) | **REFUTADA**: 3/5 con R0 0.93. |
| P11 ENSENA_F0+COMPOST ≥ 4/5 | ACERTÓ (5/5). |
| P12 BORRA ayuda menos que COMPOST | **REFUTADA a medias**: con enseñanza igual (5/5 y 5/5; COMPOST da más cuerpos, 27 contra 19); sin enseñanza acertó (BORRA 0/5, COMPOST 3/5). |
| P13 ENSENA_F0 solo en w30 ≥ 3/5 pero R0 < 0.9 en la mitad | ACERTÓ en persistencia (5/5); **REFUTADA** en R0 (4/5 ≥ 0.9). |
| P14 CADAVER sube max_vivos sobre ENSENA_F0 en w30 | SIN DATO (no se corrió en w30; en w9 no subió: 9 contra 9). |
| P18 w30: ENSENA_F0+COMPOST 5/5, COMPOST ≥ 3/5, SIN 0/5 | ACERTÓ (5/5; COMPOST persiste 5/5 aunque sólo 2/5 con R0 ≥ 0.9; SIN 0/5). |
| P15 confirmación ≥ 4/5 con SIN 0/5 | ACERTÓ (5/5 y 0/5). |
| P2 (segunda parte) ENSENA solo ≥ 3/5 en w30 | SIN DATO: en w30 corrí ENSENA_F0, no ENSENA. |
| P16 FLUJO2 rescata menos que COMPOST | ACERTÓ (0/5 contra 3/5). |
| P17 ENSENA_F0+FLUJO2 persiste pero con menos cuerpos | ACERTÓ (4/5; max 9 contra 27 en 5/5 pares). |

## 6. Lo que no funcionó (y lo que declaro)
- VIDA toca el estado del carro desde el mundo; además fue neutro o dañino. No lo volvería a probar así: si se prueba, que sea el joven
  quien decida de quién aprender (un órgano), no el mundo.
- CADAVER coloca A/C fuera del tope `nobj`; el quimiostato entonces pierde más llegadas. Está declarado en el motor; su efecto neto fue chico.
- La composición del mundo (`comp_mundo`) se divide por T, así que en corridas extintas temprano queda diluida: sólo la leo en las que persisten.
- COMPOST es una propiedad del mundo (zona gris): la sostengo con dos controles (BORRA, FLUJO2) que separan "celda libre" de "más comida".
- Sin mutación (`p_mut 0`) por diseño: quería medir ecología pura. Con selección encima puede mejorar o empeorar; no lo sé.
- w30 con T 20 000 por tiempo: la cohorte de R0 es la de los nacidos hasta 10 000.

## 7. ¿Merece preregistro?
**Sí, uno chico y honesto**, con este nombre: *"el linaje se sostiene sin vivero cuando el mundo cierra el ciclo de la materia"*. Lo que
lo hace preregistrable: es el primer resultado sin vivero, sin fundadores repuestos y sin mutación con R0 de nacidos ≥ 0.9 en 15/15
semillas (w9 ×10, w30 ×5), con el control sin mecanismo en 0/15 y dos controles de regalo (FLUJO2, BORRA) que separan "más comida"
de "el veneno deja de tapar". Lo que hay que escribir antes de correr:
1. **Hipótesis y nula.** H: con COMPOST (B/D de edad ≥ W se vuelven A/C) el linaje del bicho real con `ensena+filtra0` prendidos persiste
   ≥ 15/20 con R0 ≥ 0.90 y `max vivos` > fundadores; nula: FLUJO2 y BORRA no crecen. Predicción que puede fallar: en w30,
   ENSENA_F0+FLUJO2 no pasa de 30 cuerpos en ≥ 15/20 mientras ENSENA_F0+COMPOST pasa de 50 en ≥ 15/20.
2. **La zona gris al frente:** COMPOST es una propiedad del mundo. Lo que se declararía es *"el mundo con ciclo de materia sostiene al
   linaje"*, no *"el bicho aprendió a sostenerse"*. Barrer W (200, 500, 1 000, 2 000): ¿perilla afinada o régimen? (mi apuesta: régimen;
   con W → ∞ es SIN).
3. **Con selección encima (p_mut 0.05, banco y sombras), SIN vivero:** ¿la selección prende `ensena`/`filtra0` sola en este mundo? Es la
   pregunta de ECO v2.1 sin vivero: aquí ya hay sobre quién seleccionar sin reponer fundadores.
4. **El cuello siguiente es el agua** (sed 72–88 por corrida en w30 con compost): medirlo, no arreglarlo.
5. Gemelo numba antes de la serie: 505 s por corrida en w30 T 20 000 con 75 cuerpos en Python; a T 120 000 con Pool 3 son horas.
Lo que NO merece preregistro hoy: bolsa común, nicho, enseñar en vida, cadáver (0/5 solos y sin efecto medible encima de lo demás).
