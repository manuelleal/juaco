# EXPLORATORIO, no es dato

# HALLAZGOS — comité 2, EXPLORADOR FABLE 2: "salir del molde, el LINAJE como unidad" (25-sep-2026, ~15:50–17:40)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

**Veredicto en una línea: NO. Ninguna de las siete ideas de linaje/escudería acerca a V143 a 0.85; la mejor idea (cultura pública por la
pizarra) arregla EXACTAMENTE lo que iba a arreglar —el fundador ciego deja de morir: 0 fundadores tempranos contra 4 de v143— y hunde el R0 real
de 0.619 a 0.211 (0/5 pareadas) porque destapa un segundo muro: en esta pista, quien mantiene el mundo comestible es el fundador ignorante
al morir, y un linaje que sabe lo que es malo deja de limpiar. Es "el veneno tapa el mundo" (carril B, ECO) reproducido dentro del carro.**
Regla de parada: nadie. O1 0.95 en 5/5.

## 0. Qué hay en `comite2/molde/` (sólo copias; sin git; sin Pool; ningún proceso matado; nada fuera de la carpeta)
| archivo | qué es |
|---|---|
| `PREDICCIONES_previas.md` | P1–P11 firmadas antes de correr (se declaran en §5) |
| `construye_molde.py` → `carros/MOLDE.py` | V143.py (2a03048a7f1525e5) + perillas por anclas: PIZ, PIZ_BAR, PIZ_FUND, IMITA, ESPERA (ola 1), PIZ_ADS, BARRE (ola 2). Todas 0 = V143 **bit a bit** (arnés `corre_molde.py --identidad`: física entera de 9 linajes + pista, s 38901, T 3000: OK ×3 reconstrucciones; `revisa_carro` PASA). sha final 1aa0895a59c6dd5f |
| `corre_molde.py` | una corrida por proceso: `pista.py` de la carrera importado tal cual, 9 carros iguales, fundador limpio, T 100 000, pizarra 1, `juez.resumen_linaje` |
| `lanza.py` (+`lanza.log`) | cola, máximo 4 procesos, `subprocess`, sin Pool |
| `lee.py` | tabla por brazo pareada con v143 y o1 con la misma semilla; `--md` |
| `NOTAS_mecanismo.md` | lectura de la telemetría mientras corrían las olas |
| `datos/*.json` | un crudo por corrida (física + `tel` del carro) |
| `identidad_salida*.txt`, `invalidas_borradas.txt` | arneses; y las corridas `*barre*` que corrieron con un carro donde BARRE no había entrado (ver §6) |

Semillas 38001–38005, T 100 000. Medida principal: mediana por semilla del R0 real de los 9 linajes; mediana sobre 5 semillas.
Contabilidad física coherente 45/45 en todos los brazos.

## 1. Las ideas (reglas locales del carro; ninguna copia la regla de O1 ni la de O3; O1 no usa la pizarra)
| brazo | idea de linaje/escudería |
|---|---|
| `piz` | **CULTURA PÚBLICA.** Cada cuerpo publica en la pizarra (canal fijo del REGLAMENTO, 8 números) su tabla SENTIDA: dE, dAg medios por letra según sus propias mordidas, cada 50 pasos o cuando cambia un signo. Todo cuerpo lee cada paso las entradas nuevas de otros y las mete por la VÍA LENTA con la misma rutina con que FABRICA lee el nodo (R = +1 / −3 por signo). El fundador limpio nace sin memoria pero con cultura. |
| `piz_bar` | control de contenido: lee con las letras cruzadas por parejas (A↔B, C↔D) |
| `piz_fund` | dosis: lee sólo mientras el carro no ha sentido nada propio |
| `imita` | imitación sin canal: de la foto `obs['cuerpos']`, "mordió X" → +1 para X (dos filas), "parado sobre X sin morder" → −1; tasa 0.05 |
| `espera` | historia de vida: veta el parto si la cola real ≥ 3 |
| `piz_ads` (ola 2) | `piz` + la cultura también llena la tabla sentida `_adS`, para que la OPCIÓN APRENDIDA de v14.3 (APR) pueda considerar limpiar lo malo |
| `barre`, `piz_barre`, `piz_ads_barre` (ola 2) | **BARRE (nicho, regla mía):** si ≥ 80 % de los objetos a la vista son malos conocidos (mundo tapado) y la necesidad que golpea esa letra está ≥ 0.8, el objetivo pasa a ser el malo pagable más cercano y se muerde aunque el FILTRO lo vete. Declaro la cercanía con la limpieza "costeable" de O1: difiere en el disparador (composición del mundo, no "nada útil a la vista") y en el costo (piso fijo, no la necesidad más llena ni la ventana de parto). |

Lo que NO se pudo probar y por qué: **compartir energía entre hermanos vivos** (en esta pista hay UN cuerpo vivo por linaje: no existe el
hermano vivo); **apoptosis del viejo / roles por cola** (es el terreno de O3: muerte programada y limpieza por existencias, ERR-102);
**vida rápida** (dote y rep_X son costos del mundo, REGLAMENTO §4).

## 2. Tabla ola 1 (5 semillas; CON contra SIN con la misma semilla) — `lee.py --semillas 38001-38005 --md`
| brazo | R0 real med | por semilla | ≥.85 | cruzan | persist | establ (R0 est) | fund med | fund=0 | muertes | vida | B+D causa | fund: n/vida/sin parir | hijos: n/vida/sin parir/hijos | vs v143 gana/dif | vs o1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **o1** | **0.950** | 0.90, 0.947, 0.95, 0.95, 0.958 | 5/5 | 35/45 | 39/45 | 39/45 (0.95) | 0 | 36/45 | 22 | 3330 | 0.73 | 1334/200/0.964 | 769/3247/0.35/2.31 | 5/5 +0.283 | – |
| **v143** | **0.619** | 0.619, 0.544, 0.667, 0.766, 0.397 | 0/5 | 15/45 | 31/45 | 31/45 (0.868) | 15 | 11/45 | 46 | 600 | 0.92 | 8003/44/0.988 | 1213/1488/0.462/1.7 | – | 0/5 −0.283 |
| piz_fund | 0.216 | 0.216, 0.209, 0.187, 0.225, 0.22 | 0/5 | 0/45 | 0/45 | 0/45 | 75 | 0/45 | 97 | 595 | 0.66 | 3481/600/0.818 | 939/200/0.968/0.04 | 0/5 −0.403 | 0/5 −0.738 |
| **piz** | **0.211** | 0.22, 0.234, 0.2, 0.206, 0.211 | 0/5 | 0/45 | 0/45 | 0/45 | 64 | 0/45 | 86 | 600 | 0.53 | 2968/600/0.824 | 804/200/0.908/0.12 | **0/5 −0.399** | 0/5 −0.744 |
| imita | 0.190 | 0.19, 0.238, 0.189, 0.13, 0.215 | 0/5 | 2/45 | 3/45 | 3/45 (0.943) | 135 | 0/45 | 167 | 194 | 0.87 | 5894/92/0.928 | 1395/600/0.705/0.6 | 0/5 −0.429 | 0/5 −0.743 |
| espera | 0.067 | 0.067, 0.076, 0.147, 0.057, 0.033 | 0/5 | 3/45 | 9/45 | 9/45 (0.867) | 190 | 4/45 | 210 | 54 | 0.97 | 9774/46/0.984 | 547/600/0.598/0.65 | 0/5 −0.52 | 0/5 −0.871 |
| piz_bar | 0.000 | 0 ×5 | 0/5 | 0/45 | 0/45 | 0/45 | 375 | 0/45 | 375 | 200 | 0.93 | 16820/200/1.0 | 1/741/1.0/0 | 0/5 −0.619 | 0/5 −0.95 |

Mundo (composición media de 36 objetos, y fracción de pasos sin NINGÚN objeto bueno): v143 A 1.5 / C 1.6 / B 16.5 / D 16.2, 2.8 %;
**piz A 0.7 / C 1.2 / B 18 / D 16, 12–14 %**; o1 4.7 %. Fundadores antes de t 1500 (mediana por linaje): v143 4, **piz 0**, o1 0;
después de t 1500: v143 10, **piz 64**, o1 0.

## 3. Tabla ola 2 (5 semillas; `PIZ_ADS` y `BARRE`) — se completa abajo (§3b) con lo que alcanzó a correr
Ver §3b.

## 4. Lo mejor, en humano
1. **La métrica escrita como cuenta del linaje.** Con fundador limpio, cada muerte es un nacimiento real o un fundador, así que
   **R0 real = (D − F)/(D + 1)**. Los 11 linajes de v143 con F = 0 dan 0.968; los 36 de O1 con F = 0 dan 0.951. **Todo el hueco entre V143
   y O1 es F**, no el hijo: el hijo de v143 ya rinde como el de O1 cuando su linaje no se extingue. Corolarios que la ola 1 confirmó:
   vetar partos (`espera`) baja D y además vacía la reserva del linaje (la cola pasa de 11–16 a ≤ 3): 0.067; y "hermanos vivos" no existe.
2. **El fundador de v143 muere por hambre-en-la-boca, no por ignorancia pura.** Nace a 0.6 sin saber nada; muerde lo primero (p 0.99); si
   fue malo queda a 0.2 con hambre 0.8, y la aversión de una sola mordida (−1.35 en la vía lenta) no le gana al empuje del hambre (+1.6):
   re-muerde B con p ≈ 0.83. El FILTRO con META, la pieza más valiosa de v14.3, está apagado justo ahí porque META exige conocer algo bueno.
   La cultura pública lo arregla del todo: **0 fundadores antes de t 1500** en 45/45 linajes (v143: mediana 4), y `piz_bar` (cultura al revés)
   se va a 375 fundadores por linaje y R0 0.000: **el contenido de la pizarra es lo que actúa** (P5 se cumple con margen).
3. **Y entonces aparece el segundo muro: el linaje que sabe deja de limpiar.** En esta pista lo bueno se come en ~10 pasos y lo malo sólo sale
   por mordida u olvido (9 × 0.003 por paso). Cuenta de servilleta: 9 cuerpos comen ~0.09 buenos por paso → nacen ~0.045 malos por paso; el
   olvido saca 0.027; el resto (~0.018 por paso ≈ **200 mordidas malas por linaje cada 10⁵ pasos**) alguien tiene que morderlo. En v143 esas
   mordidas las hacen los **fundadores ignorantes al morir** (3 900 + 4 000 muertes por sal/veneno en 45 linajes) más APR (20–160 por linaje).
   Con cultura nadie muerde lo malo: el mundo queda con 0.7 A y 1.2 C de 36, los cuerpos mueren de hambre a los **600 pasos exactos** (la dote
   sin comer nada) y, sin META (no hay A a la vista), el FILTRO vuelve a apagarse y el hijo nacido a 0.6 muerde lo malo y muere a los 200.
   **La ignorancia de v143 era un bien público**: sostenía el mundo a costa de la mitad del R0.
4. **La imitación sin consecuencia es ruido** (P8 refutada): al principio todos muerden de todo y reparten +1 a todas las letras; el "−1 por
   pararse sin morder" llega tarde y mezclado con los rechazos de A/C por saciedad. 108–168 fundadores por linaje.
5. **Lo que sí distingue a O1 es que su linaje hace las dos cosas a la vez:** no muere de ignorancia (prueba una letra sólo si puede pagarla) y
   **limpia** (374 mordidas malas por linaje contra 90 de v143 y 104 de `piz`) sin morirse de eso (73 % de sus muertes son por hambre/sed a los
   3 300 pasos). Esa limpieza es el bien público que la ecología de esta pista exige, y es lo que S-SIN-LIMPIEZA ya había mostrado por el otro lado.

## 5. Predicciones: qué falló (`PREDICCIONES_previas.md`)
| # | predicción | resultado |
|---|---|---|
| P1 | v143 en [0.45, 0.72] | se cumple (0.619; por semilla 0.40–0.77: una fuera por debajo) |
| P2 | o1 ≥ 0.85 en ≥ 4/5 | se cumple (5/5) |
| **P3** | `piz` > v143 en ≥ 4/5 con dif ≥ +0.10 (p 0.60) | **REFUTADA al revés: 0/5, −0.40** |
| P4 | `piz` fundadores por linaje ≤ 3 contra ≥ 10 de v143 | **REFUTADA** (64 contra 15): baja F sólo antes de t 1500 (0 contra 4) y lo multiplica después. Mi lectura de la métrica no estaba mal: estaba incompleta (faltaba el mundo). |
| P5 | `piz_bar` < v143 en ≥ 4/5 | se cumple (5/5; 0.000) |
| P6 | `piz_fund` dentro de ±0.05 de `piz` | se cumple (0.216 contra 0.211): el hijo no necesita la cultura; pero ambos se hunden |
| **P7** | vida del hijo de `piz` en 1000–2000 | **REFUTADA**: 200 (muerde lo malo sin META en un mundo sin A y muere) |
| **P8** | `imita` > v143 en ≥ 3/5 | **REFUTADA** (0/5, −0.43); "peor que piz" se cumple por poco |
| P9 | `espera` < v143 en ≥ 4/5 | se cumple en el signo (5/5) y **falla en la magnitud**: no −0.1, sino −0.52: el veto vacía la cola (reserva del linaje) |
| P10 | nadie ≥ 0.90 en ≥ 3/5 salvo o1 | se cumple |
| P11 | en `piz` los fundadores antes de t 1000 no llegan a 0 en todas | **REFUTADA**: llegan a 0 en 45/45 linajes. El cuerpo de t = 0 (1.0/1.0) aguanta la primera mordida ciega y a los ~10 pasos ya lee la cultura |
| P12 (ola 2, firmada en NOTAS antes de correr) | `piz_ads` ≈ `piz` (APR no limpia lo suficiente) | ver §3b |
| P13 (ola 2) | `piz_barre` > `piz` en 5/5 y `barre` > v143 en ≥ 3/5 | ver §3b |

## 6. Lo que no funcionó (y lo que declaro)
- **Error de instrumento propio (declarado y corregido):** en la ola 2 reconstruí `MOLDE.py` con las perillas nuevas; dos anclas de BARRE
  (objetivo y boca) no entraron al primer intento y la constante `BARRE_FRAC` tampoco. Las corridas `*barre*` lanzadas con ese carro (sha
  cf4e44c66645a610) eran `piz`/`v143` con otro nombre; se detectaron por el sha del carro en el JSON, se borraron (lista en
  `invalidas_borradas.txt`) y se relanzaron con el carro correcto (1aa0895a59c6dd5f), tras repetir el arnés de identidad (OK). Además la
  ola 1 corrió con dos shas del carro (065877aff063694b y cf4e44c66645a610), ambos idénticos en física con perillas 0 (arnés OK ×2).
- `_mol_msg` aplica el decaimiento LAM del nodo por cada mensaje: con 9 mensajes por paso es más frecuente que en el nodo. No lo ajusté.
- La pizarra guarda medias sentidas (`_adS` de APR), que existen porque V143 lleva OPCION 1; en un FABRICA puro habría que llevar la cuenta aparte.
- Un solo carro por escudería (monocultivo). No corrí `piz` con rivales de fábrica ni el SOLO: con el hundimiento en 0/5 no tenía sentido.
- T = 100 000 en todo; ~200–420 s por corrida; 35 + 20 corridas válidas en ~1 h 40 de reloj con 4 procesos.

## 7. ¿Merece preregistro?
**No como está.** Lo que sí sale de aquí y vale para el director:
1. **Una ecuación de la letra:** R0 real = (D − F)/(D + 1). Con fundador limpio, cruzar 0.90 exige F ≤ (D − 9)/10: un linaje con 40 muertes
   tolera 3 fundadores. Es útil para leer cualquier carro y separa "establecerse" de "no extinguirse".
2. **Dos muros, no uno, y se tapan mutuamente.** Muro A (fundador): sin conocer nada bueno, el hambre gana a la aversión. Muro B (mundo): sin
   mordidas malas el mundo se tapa. Cualquier pieza que baje A destapa B. La pizarra como cultura resuelve A por completo (0 fundadores tempranos,
   control de contenido en 0.000): es replicable y barato, pero sólo sirve acompañado de algo que pague B. Preregistro **posible y chico** si la
   ola 2 muestra que una regla de nicho (BARRE) o la opción aprendida con conocimiento (PIZ_ADS) paga B: «cultura pública + destape del mundo»,
   20 semillas, brazos piz, piz_barre, barre, piz_bar, v143, o1, con las predicciones de §3b como letra. Si la ola 2 no lo muestra, no hay
   preregistro: hay un hallazgo de ecología (el mismo del carril B) y una pregunta para el mundo, no para el bicho.
3. **Para JUACO en general:** es el segundo carril (tras ECO) donde "aprender a no morder lo malo" mata al linaje por vía ecológica. Vale
   escribirlo como regla del método: toda mejora de la boca se mide junto con la composición del mundo (`comp_mundo`, `frac_sin_bueno_mundo`).
