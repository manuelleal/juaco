# EXPLORATORIO, no es dato

# Predicciones del EXPLORADOR B (ecología y vida en grupo) ANTES de correr — 25-sep-2026

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas); el método manda sobre el cómo.

## Lo que ya vi antes de escribir esto (declarado, humos de calibración, semilla de práctica 34901)
- Motor: copia de `juaco_eco/motor_eco3.py` → `motor_ecologia.py` (solo rutas cambiadas hasta ahora). Bicho: `FABRICA_ECO` (el
  bicho real, `hereda='nada'`), genoma de fábrica, `p_mut = 0`, **sin vivero** (`refunda=0`) desde el paso 0, quimiostato (`fija`).
- w9 (9 fundadores, L 360): extinto en t 1 689; 5 nacidos, R0 nacidos 0.0; vida media 663; causas veneno 5 / sal 9 (100 %).
  Mordidas: A 76, B 32, C 78, D 51 (35 % malas). El mundo termina lleno de B/D (composición media B 5.5, D 8.6 contra A 1.9, C 1.8).
- w9 con reposición inmediata (referencia, no mecanismo): extinto en 2 979; igual de mal. w30: extinto en 5 351; 14 nacidos, R0 0.0.
- Lectura: el bicho de fábrica muere por VENENO, no por falta de comida: cada cuerpo nace sin memoria y paga otra vez la lección
  (0.4 por mordida de B o D), en un mundo que se va llenando de lo que nadie come.

## Mecanismos (todos reglas locales en el MUNDO o en el parto; el cerebro del bicho no cambia de reglas)
| clave | qué hace | de dónde sale |
|---|---|---|
| SIN | control: nada | — |
| ENSENA | el padre pasa su tabla al hijo en el parto (`FAMB_ORG_ECO` con `ensena` prendido; con `ensena` apagado es FABRICA bit a bit) | ficha "familia comparte lo aprendido", órgano ya construido |
| ENSENA_F0 | ENSENA + el hijo quita lo neutro (`filtra0`) | gramática FIJO:filtra0 (persistió 20/20 con vivero) |
| VIDA | enseñar EN VIDA: cada paso, un cuerpo con un pariente MAYOR a ≤ R celdas mueve su vía lenta (Wps, Wns) hacia la del mayor con tasa λ = 0.1 | Prometeo "enseñar durante la vida" |
| CADAVER | al morir, el cuerpo deja en su celda un objeto con el recurso que le quedaba: 'C' (agua) si murió con E ≤ 0 y Ag ≥ 0.4; 'A' (comida) si murió con Ag ≤ 0 y E ≥ 0.4 | ficha 13 |
| BOLSA | tras los costos, los cuerpos del MISMO linaje a ≤ 1 celda promedian E y Ag | ficha 4 |
| BOLSA_TODOS | control de parentesco: la bolsa entre cuerpos de CUALQUIER linaje a ≤ 1 celda (Hamilton dice que esto no debería ayudar más que la de parientes) | ficha 4, control |
| NICHO | construcción de nicho: la llegada del quimiostato cae a ≤ 10 celdas de donde alguien mordió B/D en los últimos 200 pasos (la comida de un sitio es de quien lo limpia); el flujo total NO cambia | ficha "localidad y territorio" |
| NICHO_AZAR | control: la llegada cae a ≤ 10 celdas de un cuerpo vivo al azar (regalo de cercanía sin limpiar) | control |
| combinaciones | ENSENA+CADAVER, ENSENA+CADAVER+BOLSA, ENSENA_F0+CADAVER, VIDA+ENSENA | — |

No se prueba (declarado): vejez/apoptosis regulada. Con vidas de 650 pasos y R0 0, quitar viejos no tiene a quién ayudar; queda
para cuando algo persista.

## Medidas
Por corrida (misma semilla CON y SIN): `persiste` (vivos en T), `vivos_T`, `max_vivos`, nacidos, **R0 nacidos** = hijos medios de los
cuerpos NO fundadores nacidos hasta T − 10 000, vida media, causas, mordidas por letra, composición del mundo, cadáveres puestos.
Mundos: w9 (rápido, 9 fundadores) para barrer; w30 (30 fundadores, el mundo de ECO) para lo que prometa. T = 30 000.
Semillas: 34001–34005; confirmación 34011–34015. Regla de parada: un mecanismo con persistencia ≥ 4/5 y R0 ≥ 0.90 donde SIN no lo
logra → confirmar con 5 más y parar.

## Predicciones firmadas (probabilidad de que se cumpla lo escrito)
| # | predicción | p |
|---|---|---|
| P1 | SIN: 0/5 persisten en w9 y 0/5 en w30 (ya lo vi en una semilla de práctica, así que esto casi no es predicción). | 0.90 |
| P2 | ENSENA solo: persiste en ≥ 3/5 en w30, pero R0 nacidos < 0.90 en la mayoría (persistir no es lo mismo que R0 ≥ 0.9). En w9 ≤ 2/5. | 0.45 |
| P3 | CADAVER solo NO rescata (≤ 1/5): la muerte es por veneno, no por falta de materia. | 0.70 |
| P4 | BOLSA sola NO rescata (0/5): sin hijos casi no hay parientes juntos. BOLSA_TODOS tampoco. | 0.80 |
| P5 | VIDA sola: ≤ 1/5 en w9. Los fundadores no tienen mayores de quien aprender y no llegan a la segunda generación. | 0.60 |
| P6 | NICHO no se distingue de NICHO_AZAR ni de SIN (diferencia ≤ 1/5): el problema no es dónde cae la comida. | 0.60 |
| P7 | ENSENA+CADAVER es lo mejor de todo: ≥ 4/5 persisten en w30 con R0 ≥ 0.90 (la parada). | 0.35 |
| P8 | Si ENSENA persiste, agregar CADAVER SUBE `max_vivos` (capacidad de carga) en ≥ 4/5 pares (misma semilla). | 0.60 |
| P9 | Miedo declarado: que el efecto de "enseñar" ya conocido (FIJO:ensena) sea lo único que mueve la aguja y que lo ecológico (cadáver, bolsa, nicho) no agregue nada medible. | 0.50 |

## Agregado DESPUÉS del barrido w9 (13:46) y ANTES de correr la descomposición y w30 (declarado)
Lo que vi en w9 (semillas 34001–34005, T 30 000): SIN 0/5; ENSENA 0/5 (t_ext mediana 7 996); **ENSENA_F0 2/5 con R0 ≈ 1.0 en las que
persisten**; CADAVER solo 0/5 (alarga la vida del linaje: t_ext 3 317 contra 1 963); BOLSA, NICHO, VIDA 0/5. En ENSENA_F0 el mundo queda
lleno de B/D (31 de 36 objetos) y las llegadas del quimiostato se pierden: **nadie come lo tóxico y lo tóxico tapa la comida**.
Mecanismo nuevo: **COMPOST** (un B/D con ≥ 500 pasos de edad se vuelve A/C: el ciclo de la materia) y su control **BORRA** (el B/D
desaparece: sólo libera la celda). Zona gris declarada: es una propiedad del mundo (más comida efectiva), no del bicho.
| # | predicción | p |
|---|---|---|
| P10 | COMPOST solo NO rescata al bicho de fábrica (0/5 en w9): sigue muriendo por morder B/D antes de aprender. | 0.65 |
| P11 | ENSENA_F0+COMPOST persiste ≥ 4/5 en w9 con R0 ≥ 0.90 (la parada en w9). | 0.45 |
| P12 | BORRA ayuda MENOS que COMPOST (ENSENA_F0+BORRA persiste menos veces que ENSENA_F0+COMPOST): el cuello es la comida, no sólo la celda. | 0.55 |
| P13 | En w30 (30 fundadores), ENSENA_F0 solo ya persiste ≥ 3/5 (más fundadores, menos azar), pero con R0 < 0.90 en la mitad. | 0.50 |
| P14 | CADAVER sobre ENSENA_F0 sube `max_vivos` en ≥ 3/5 pares en w30 (P8 reescrita para el bicho que sí persiste). | 0.55 |

## Agregado tras el barrido w9 completo (13:51), ANTES de la confirmación (34011–34015), de los controles de flujo y de w30
Visto: COMPOST solo 3/5 (R0 0.93) → **P10 refutada**; ENSENA+COMPOST, ENSENA_F0+COMPOST, ENSENA_F0+BORRA y ENSENA_F0+CADAVER+COMPOST
5/5 con R0 ≥ 1.0 → P11 acertó y **P12 refutada en w9** (BORRA rescata igual que COMPOST cuando hay enseñanza; COMPOST da más
cuerpos: max 27 contra 19). Regla de parada disparada → confirmar con 34011–34015 y parar.
Control nuevo **FLUJO2** (r_rep 0.06 = doble llegada, sin descomposición): ¿COMPOST es sólo "más comida"?
| # | predicción | p |
|---|---|---|
| P15 | Confirmación w9 (34011–34015): ENSENA_F0+COMPOST ≥ 4/5 con R0 ≥ 0.90; SIN 0/5. | 0.75 |
| P16 | FLUJO2 solo rescata al bicho de fábrica MENOS que COMPOST (≤ 1/5 contra 3/5): el doble de flujo también trae el doble de veneno y el mundo se tapa igual. | 0.55 |
| P17 | ENSENA_F0+FLUJO2 persiste ≥ 3/5 pero con menos cuerpos que ENSENA_F0+COMPOST (max_vivos menor en ≥ 4/5 pares). | 0.55 |
| P18 | En w30 (T 20 000) ENSENA_F0+COMPOST 5/5 y COMPOST solo ≥ 3/5; SIN 0/5. | 0.65 |
