# EXPLORATORIO, no es dato

# HALLAZGOS — comité 2, EXPLORADOR FABLE 2: "salir del molde, el LINAJE como unidad" (25-sep-2026, 15:50–17:40)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

**Veredicto en una línea: NO. Ninguna de las 12 variantes de linaje/escudería acerca a V143 a 0.85 (regla de parada: nadie; O1 0.95 en 5/5).
La mejor idea —cultura pública por la pizarra— arregla EXACTAMENTE lo que iba a arreglar: el fundador ciego deja de morir (0 fundadores antes de
t 1500 en 45/45 linajes, contra 4 de v143) y el control de contenido (pizarra al revés) cae a 0.000. Y sin embargo hunde el R0 real de 0.619 a
0.211 (0/5 pareadas), porque destapa un segundo muro: en esta pista el fundador ignorante que muere era quien mantenía el mundo comestible, y una
escudería que sabe lo que es malo deja de limpiar, pierde la META, apaga su propio FILTRO y muere de hambre. Es "el veneno tapa el mundo" del
carril B (ECO) reproducido dentro del carro. Hay algo que vale como conocimiento, no como pieza.**

## 0. Qué hay en `comite2/molde/` (sólo copias; sin git; sin Pool; ningún proceso matado; nada fuera de la carpeta)
| archivo | qué es |
|---|---|
| `PREDICCIONES_previas.md` | P1–P11 (antes de correr), P12–P15 (ola 2, tras leer la ola 1), P16–P18 (ola 3, tras el humo T 3000). Se declaran en §5 |
| `construye_molde.py` → `carros/MOLDE.py` | V143.py (2a03048a7f1525e5) + perillas por anclas: PIZ, PIZ_BAR, PIZ_FUND, IMITA, ESPERA, PIZ_ADS, BARRE, BARRE_V2. **Todas 0 = V143 bit a bit** (arnés `corre_molde.py --identidad`: física entera de 9 linajes + pista, s 38901, T 3000: OK en las 3 reconstrucciones; `revisa_carro` PASA). sha final 9454cbfd1b78bcf6 |
| `corre_molde.py` | una corrida por proceso: `carrera_escuderias/pista.py` importado tal cual, 9 carros iguales, fundador limpio, T 100 000, pizarra 1, `juez.resumen_linaje` |
| `lanza.py` (+`lanza.log`) | cola con `subprocess`, máximo 4 procesos, sin Pool |
| `lee.py` | tabla por brazo pareada con v143 y o1 con la misma semilla (`--md`) |
| `NOTAS_mecanismo.md` | lectura de la telemetría escrita mientras corrían las olas |
| `tabla_final.md`, `tabla_ola1.md`, `tabla_ola2.md` | salidas de `lee.py` |
| `datos/*.json` | 65 crudos válidos (13 brazos × 5 semillas), física + telemetría del carro |
| `identidad_salida*.txt`, `invalidas_borradas.txt`, `_parche_v2.py` | arneses; corridas inválidas borradas (§6); parche del constructor |

Semillas 38001–38005, T 100 000, ~180–420 s por corrida. Medida principal: mediana por semilla del R0 real de los 9 linajes; mediana sobre semillas;
pareado CON contra SIN (v143) con la misma semilla. Contabilidad física coherente 45/45 en los 13 brazos.

## 1. Las ideas (reglas locales del carro; ninguna copia la regla de O1 ni la de O3; O1 no usa la pizarra)
| brazo | idea de linaje/escudería |
|---|---|
| `piz` | **CULTURA PÚBLICA.** Cada cuerpo publica en la pizarra (canal fijo del REGLAMENTO, 8 números) su tabla SENTIDA —dE, dAg medios por letra según sus propias mordidas— cada 50 pasos o cuando cambia un signo. Todo cuerpo lee cada paso las entradas nuevas de otros y las mete por la VÍA LENTA con la misma rutina con que FABRICA lee el nodo (R = +1 / −3 por signo). El fundador limpio nace sin memoria pero con cultura. |
| `piz_bar` | control de contenido: lee con las letras cruzadas por parejas (A↔B, C↔D) |
| `piz_fund` | dosis: lee sólo mientras el carro no ha sentido nada propio |
| `imita` | imitación sin canal: de la foto `obs['cuerpos']`, "mordió X" → +1 para X en las dos filas, "parado sobre X sin morder" → −1; tasa 0.05 |
| `espera` | historia de vida "vivir más, parir menos": veta el parto si la cola real ≥ 3 |
| `piz_ads` | `piz` + la cultura también llena la tabla sentida `_adS`, para que la OPCIÓN APRENDIDA de v14.3 (APR) pueda considerar limpiar lo malo. Cero reglas nuevas |
| `barre`, `piz_barre`, `piz_ads_barre` | **BARRE dosis 1 (nicho, regla mía):** si ≥ 80 % de los objetos a la vista son malos conocidos (mundo tapado) y la necesidad que golpea esa letra está ≥ 0.8, el objetivo es el malo pagable más cercano y se muerde aunque el FILTRO lo vete |
| `barre2`, `piz_barre2` | **BARRE dosis 2:** además sólo si el mundo está tapado en ese paso, fuera de la ventana de parto (E o Ag < 1.0) y a lo sumo una mordida cada 200 pasos |

Declaro la cercanía de BARRE con la limpieza "costeable" de O1: difiere en el disparador (composición del mundo, no "nada útil a la vista") y en el
costo (piso fijo / fuera de la ventana, no "la necesidad más llena"). No es la regla de O1, pero vive en el mismo barrio.

No se pudo probar, y por qué: **compartir energía entre hermanos vivos** (en esta pista hay UN cuerpo vivo por linaje: el hermano vivo no existe);
**apoptosis del viejo / roles por cola** (terreno de O3: muerte programada y limpieza por existencias, ERR-102); **vida rápida** (dote y rep_X son
costos del mundo, REGLAMENTO §4).

## 2. Tabla (5 semillas por brazo; CON contra SIN con la misma semilla) — `tabla_final.md`
| brazo | R0 real med | por semilla | ≥.85 | cruzan | persist | fund med | fund=0 | muertes | vida | B+D causa | fund: n/vida/sin parir | hijos: n/vida/sin parir/hijos | vs v143 gana/dif | vs o1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **o1** | **0.950** | 0.90, 0.947, 0.95, 0.95, 0.958 | 5/5 | 35/45 | 39/45 | 0 | 36/45 | 22 | 3330 | 0.73 | 1334/200/0.964 | 769/3247/0.35/2.31 | 5/5 +0.283 | – |
| barre2 | 0.621 | 0.33, 0.697, 0.30, 0.721, 0.621 | 0/5 | 10/45 | 28/45 | 21 | 7/45 | 48 | 600 | 0.91 | 8279/46/0.985 | 1076/1410/0.486/1.74 | 2/5 −0.045 | 0/5 −0.337 |
| **v143** | **0.619** | 0.619, 0.544, 0.667, 0.766, 0.397 | 0/5 | 15/45 | 31/45 | 15 | 11/45 | 46 | 600 | 0.92 | 8003/44/0.988 | 1213/1488/0.462/1.7 | – | 0/5 −0.283 |
| piz_fund | 0.216 | 0.216, 0.209, 0.187, 0.225, 0.22 | 0/5 | 0/45 | 0/45 | 75 | 0/45 | 97 | 595 | 0.66 | 3481/600/0.818 | 939/200/0.968/0.04 | 0/5 −0.403 | 0/5 −0.738 |
| **piz** | **0.211** | 0.22, 0.234, 0.20, 0.206, 0.211 | 0/5 | 0/45 | 0/45 | 64 | 0/45 | 86 | 600 | 0.53 | 2968/600/0.824 | 804/200/0.908/0.12 | **0/5 −0.399** | 0/5 −0.744 |
| imita | 0.190 | 0.19, 0.238, 0.189, 0.13, 0.215 | 0/5 | 2/45 | 3/45 | 135 | 0/45 | 167 | 194 | 0.87 | 5894/92/0.928 | 1395/600/0.705/0.6 | 0/5 −0.429 | 0/5 −0.743 |
| piz_ads | 0.186 | 0.217, 0.163, 0.182, 0.186, 0.186 | 0/5 | 0/45 | 0/45 | 65 | 0/45 | 80 | 600 | 0.48 | 2958/600/0.837 | 688/600/0.885/0.14 | 0/5 −0.402 | 0/5 −0.768 |
| piz_barre2 | 0.179 | 0.188, 0.165, 0.171, 0.232, 0.179 | 0/5 | 0/45 | 0/45 | 66 | 0/45 | 83 | 600 | 0.36 | 3081/600/0.838 | 709/600/0.904/0.12 | 0/5 −0.431 | 0/5 −0.779 |
| espera | 0.067 | 0.067, 0.076, 0.147, 0.057, 0.033 | 0/5 | 3/45 | 9/45 | 190 | 4/45 | 210 | 54 | 0.97 | 9774/46/0.984 | 547/600/0.598/0.65 | 0/5 −0.52 | 0/5 −0.871 |
| barre | 0.000 | 0 ×5 | 0/5 | 0/45 | 0/45 | 342 | 0/45 | 342 | 84 | 0.83 | 14529/81/1.0 | 3/424/1.0/0 | 0/5 −0.619 | 0/5 −0.95 |
| piz_ads_barre | 0.000 | 0 ×5 | 0/5 | 0/45 | 0/45 | 53 | 0/45 | 53 | 1201 | 0.26 | 2394/1212/0.997 | 6/660/1.0/0 | 0/5 −0.619 | 0/5 −0.95 |
| piz_barre | 0.000 | 0 ×5 | 0/5 | 0/45 | 0/45 | 54 | 0/45 | 55 | 1194 | 0.25 | 2380/1188/0.998 | 5/600/1.0/0 | 0/5 −0.619 | 0/5 −0.95 |
| piz_bar | 0.000 | 0 ×5 | 0/5 | 0/45 | 0/45 | 375 | 0/45 | 375 | 200 | 0.93 | 16820/200/1.0 | 1/741/1.0/0 | 0/5 −0.619 | 0/5 −0.95 |

**El mundo y la limpieza, por brazo** (A+C medios de 36 objetos · fracción de pasos sin NINGÚN bueno · mordidas B+D por linaje (mediana) ·
fundadores por linaje antes / después de t 1500):
| brazo | A+C | sin bueno | mord B+D | fund ≤1500 / >1500 | lectura |
|---|---|---|---|---|---|
| v143 | 3.1–3.4 | 2.4–3.2 % | 64–195 | 4 / 10 | los fundadores ciegos limpian al morir |
| o1 | 1.8–2.3 | 3.1–4.9 % | 326–390 | 0 / 0 | mundo MÁS tapado que v143 y sostiene 0.95: limpia a propósito y coordina quién va a qué |
| piz | 1.8–1.9 | 12–14 % | 96–121 | **0 / 64** | nadie limpia; sin META el FILTRO se apaga; hambre a los 600 |
| piz_barre2 | 1.9–2.1 | 10–13 % | 151–164 | 0 / 66 | 8–32 barridas por instancia: los hambrientos casi nunca tienen la reserva 0.8 |
| barre2 | 3.8–4.2 | 1.3–2.0 % | 151–269 | 4 / 15 | limpia más (570–720 barridas; 22 000 vetos de ventana) y el mundo mejora; R0 no se mueve |
| barre (dosis 1) | 9.6–10.0 | 0.0 % | 12 600–13 000 (total) | 2 / 340 | el mundo más limpio de todos y **cero partos**: muerde cada malo que pisa y nunca junta 500 pasos ≥ 1.0 |

## 3. Lo mejor, en humano
1. **La métrica escrita como cuenta del linaje.** Con fundador limpio, cada muerte es un nacimiento real o un fundador, así que
   **R0 real = (D − F)/(D + 1)**. Los 11 linajes de v143 con F = 0 dan 0.968; los 36 de O1 con F = 0 dan 0.951. **Todo el hueco entre V143 y O1
   es F, no el hijo**: el hijo de v143 rinde como el de O1 cuando su linaje no se extingue. De ahí salen tres cosas que la ola 1 confirmó:
   vetar partos (`espera`) baja D y además vacía la reserva del linaje (la cola pasa de 11–16 a ≤ 3): 0.067; "hermanos vivos" no existe; y para cruzar
   0.90 hace falta F ≤ (D − 9)/10 (un linaje con 40 muertes tolera 3 fundadores).
2. **El fundador de v143 muere de hambre-en-la-boca, no de ignorancia pura.** Nace a 0.6 sin saber nada; muerde lo primero (p 0.99); si fue malo
   queda a 0.2 con hambre 0.8, y la aversión de una mordida (−1.35 en la vía lenta) no le gana al empuje del hambre (+1.6): re-muerde B con p ≈ 0.83.
   El FILTRO con META, la pieza que más pesa en v14.3, está apagado justo ahí porque META exige conocer algo bueno. **La cultura pública lo arregla
   del todo**: 0 fundadores antes de t 1500 en 45/45 linajes (v143: 4), y el control de contenido `piz_bar` se va a 375 fundadores y 0.000: es el
   contenido de la pizarra lo que actúa. El cuerpo de t = 0 (1.0/1.0) aguanta la primera mordida ciega y a los ~10 pasos ya lee.
3. **Y aparece el segundo muro: la escudería que sabe deja de limpiar y se apaga su propio filtro.** En esta pista lo bueno se come en ~10 pasos y
   lo malo sólo sale por mordida u olvido (9 × 0.003 por paso). Cuenta de servilleta: 9 cuerpos comen ~0.09 buenos por paso → nacen ~0.045 malos;
   el olvido saca 0.027; el resto (~200 mordidas malas por linaje cada 10⁵ pasos) alguien tiene que morderlo. En v143 lo hacen los fundadores
   ignorantes al morir (7 900 muertes por sal/veneno en 45 linajes). Con cultura nadie muerde lo malo: el mundo baja a 1.8 buenos de 36, hay 13 %
   de pasos sin ninguno, y entonces **META falla (no hay A a la vista cuando hay hambre), el FILTRO se apaga y el cuerpo que SABE que B es malo lo
   muerde igual** (hijos con vida 200: nacen a 0.6, muerden, quedan a 0.2 y mueren "de veneno"). Los fundadores pasan de morir a los 45 pasos por
   veneno a morir a los 600 de hambre. **La ignorancia de v143 era un bien público**: sostenía el mundo a costa de la mitad del R0.
4. **Limpiar a propósito no alcanza si limpiar rompe la ventana.** BARRE dosis 1 deja el mundo impecable (10 buenos de 36, 0 % sin bueno) y
   esteriliza a la escudería (desc 0 en 45/45: muerde cada malo que pisa con reserva ≥ 0.8 y nunca junta 500 pasos ≥ 1.0). Dosis 2 (fuera de la
   ventana, refractario) sin cultura mejora el mundo (4.0 contra 3.3) y no mueve el R0 (0.621 contra 0.619, 2/5); con cultura casi no barre
   (8–32 mordidas por instancia: el hambriento no tiene la reserva). Y `piz_ads` (dar la tabla a la opción aprendida de v14.3) da 0.186 ≈ `piz`:
   la Q de APR se borra con cada fundador limpio y no aprende a limpiar en su vida.
5. **Lo que O1 hace y v143 no, visto desde el mundo:** O1 vive en un mundo MÁS tapado que v143 (1.8–2.3 buenos, 3–5 % sin bueno) y aun así el hijo
   vive 3 300 pasos y deja 2.3. No es sólo que limpia (380 mordidas malas por linaje, 73 % de sus muertes por hambre/sed): es que **coordina quién
   va a qué** (no persigue lo que otro se va a comer; se coloca en el hueco). Con 2 buenos para 9 cuerpos, v143 con cultura manda a los 9 al mismo
   objeto (robos ≈ 1 100 por linaje) y 8 vuelven con hambre. La pieza que falta a nivel de escudería no es sólo "limpiar": es **repartirse el mundo**.
   No la construí (habría sido copiar el punto 3 de O1) y la dejo como pregunta.
6. **La imitación sin consecuencia es ruido** (`imita` 0.19): al principio todos muerden de todo y reparten +1 a todas las letras; el "−1 por pararse
   sin morder" llega tarde y mezclado con los rechazos de A/C por saciedad.

## 4. Lo que no funcionó (todo)
Ninguna variante superó a v143 en ≥ 3/5 semillas. Orden: barre2 0.621 (2/5, ruido) · v143 0.619 · piz_fund 0.216 · piz 0.211 · imita 0.190 ·
piz_ads 0.186 · piz_barre2 0.179 · espera 0.067 · barre / piz_barre / piz_ads_barre / piz_bar 0.000.

## 5. Predicciones: qué falló (`PREDICCIONES_previas.md`)
| # | predicción | resultado |
|---|---|---|
| P1 | v143 en [0.45, 0.72] | se cumple (0.619; por semilla 0.40–0.77) |
| P2 | o1 ≥ 0.85 en ≥ 4/5 | se cumple (5/5) |
| **P3** | `piz` > v143 en ≥ 4/5 con dif ≥ +0.10 (p 0.60) | **REFUTADA al revés: 0/5, −0.40** |
| **P4** | `piz` fundadores por linaje ≤ 3 contra ≥ 10 | **REFUTADA** (64 contra 15): baja F antes de t 1500 (0 contra 4) y lo multiplica después. La cuenta de la métrica era correcta e incompleta: faltaba el mundo |
| P5 | `piz_bar` < v143 en ≥ 4/5 | se cumple (5/5; 0.000) |
| P6 | `piz_fund` dentro de ±0.05 de `piz` | se cumple (0.216 contra 0.211) |
| **P7** | vida del hijo de `piz` en 1000–2000 | **REFUTADA**: 200 |
| **P8** | `imita` > v143 en ≥ 3/5 | **REFUTADA** (0/5) |
| P9 | `espera` < v143 en ≥ 4/5 | se cumple en el signo (5/5) y **falla en la magnitud** (−0.52, no −0.1): el veto vacía la cola |
| P10 | nadie ≥ 0.90 en ≥ 3/5 salvo o1 | se cumple |
| **P11** | en `piz` los fundadores antes de t 1000 no llegan a 0 en todas | **REFUTADA**: 0 en 45/45 |
| P12 | `piz_ads` ≈ `piz` (±0.05) | se cumple (0.186 contra 0.211) |
| **P13** | `piz_barre` > `piz` en 5/5 con dif ≥ +0.20; `barre` > v143 en ≥ 3/5 | **REFUTADA las dos**: 0.000 y 0.000 (dosis 1 esteriliza) |
| P14 | con BARRE el mundo baja a ≤ 80 % de B+D y sin-bueno ≤ 0.05 | dosis 1: se cumple con exceso (72 %, 0 %); dosis 2 sin cultura: 89 % (falla), 1.5 % (cumple); con cultura: falla las dos |
| P15 | el costo de BARRE se ve en muertes de hijos por veneno/sal ≥ 30 % | **REFUTADA en la forma**: el costo no fue morir sino no parir (desc 0) |
| **P16** | `piz_barre2` > `piz` en ≥ 4/5 pero < v143 | **REFUTADA la primera mitad**: pierde con `piz` 4/5 (0.179 contra 0.211); la segunda se cumple |
| P17 | `barre2` dentro de ±0.10 de v143 | se cumple en la mediana (−0.045) con varianza enorme por semilla (−0.37 a +0.22) |
| P18 | ninguna dosis de BARRE ≥ 0.85 en ≥ 3/5 | se cumple |

## 6. Errores de instrumento propios (declarados)
- **Anclas que no entraron.** Al agregar BARRE reconstruí `MOLDE.py` dos veces sin que entraran la constante `BARRE_FRAC` ni las dos anclas (objetivo
  y boca): el carro compilaba y las corridas `*barre*` lanzadas con él eran `piz`/`v143` con otro nombre. Se detectó porque `_mol_barre` nunca se
  llamaba (0 llamadas en un humo instrumentado) y porque sus números eran idénticos a `piz`. Corregido; identidad y humo repetidos.
- **El sha del carro se registraba al TERMINAR la corrida** (leyendo el archivo del disco al final), así que dos corridas inválidas llevaban el sha
  del carro correcto. Se identificaron por los números (idénticos a `piz`/`piz_ads`, 760–1036 mordidas B+D contra ~6 000 en las otras semillas),
  se borraron y se repitieron. Runner corregido: el sha se fija antes de correr. Lista completa en `invalidas_borradas.txt`.
- **Borrado de más:** la cadena que limpiaba inválidas comparaba contra un sha fijo y borró también 7 corridas válidas de dosis 1 (mismo código
  efectivo con `BARRE_V2 = 0`). Se repitieron; reprodujeron los mismos valores (deterministas). Costó ~15 min de CPU, no datos.
- `_mol_msg` aplica el decaimiento LAM del nodo por cada mensaje (con 9 mensajes por paso es más frecuente que en el nodo). No lo ajusté.
- La telemetría `molde` del carro es la de la ÚLTIMA instancia del linaje (fundador limpio la reinicia); las mordidas B+D sí son físicas.
- Un solo carro por escudería (monocultivo). No corrí `piz` con rivales de fábrica ni SOLO: con 0/5 no tenía sentido.

## 7. ¿Merece preregistro?
**No como pieza.** Lo que sí sale de aquí y vale para el director:
1. **Una ecuación de la letra:** R0 real = (D − F)/(D + 1). Separa "establecerse" (F) de "no extinguirse" y muestra que en V143 el hueco entero
   con O1 está en el fundador. Cualquier carro se lee con eso.
2. **Dos muros que se tapan mutuamente, y un tercero detrás.** Muro A (fundador): sin conocer nada bueno, el hambre gana a la aversión. Muro B
   (mundo): sin mordidas malas el mundo se tapa, y entonces META falla y el FILTRO de v14.3 se apaga justo cuando más hace falta. Muro C (reparto):
   con 2 buenos para 9 cuerpos, los 9 van al mismo. La cultura pública resuelve A del todo y barato (control de contenido en 0.000) y destapa B y C.
   BARRE paga B sólo si esteriliza. **Lo preregistrable no es un carro: es la medición conjunta**: toda mejora de la boca se mide con
   `comp_mundo`, `frac_sin_bueno_mundo`, robos y `pasos_meta` al lado del R0. Propongo escribirlo como regla del método (ERR de lectura).
3. **Pregunta para el director:** el REGLAMENTO permite leer `cuerpos` y la pizarra. Cultura pública (A) + una regla de reparto entre cuerpos de la
   misma escudería (C) es un preregistro chico y honesto —«la escudería que se enseña y se reparte»— con controles claros (pizarra al revés, reparto
   al azar, rivales de fábrica). No lo construí porque el reparto es el punto 3 de O1 y el encargo prohibía copiarlo; si el director lo autoriza como
   idea (no como código), es la siguiente prueba más barata. Mi predicción honesta: MODESTO con p 0.35 (A + C sin limpieza llegan a ~0.7–0.8); FUNCIONA
   sólo con B además (p 0.15).
