# EXPLORATORIO, no es dato

# PREDICCIONES previas — comité de exploración, EXPLORADOR A (trasplantes). 25-sep-2026, escritas ANTES de correr nada.

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

## Qué voy a medir
- Pista de la carrera (`carrera_escuderias/pista.py` vía `organelos/cruce/motor_cruce.py`, que con `cruce` es la pista bit a bit), 9 carros iguales,
  L 360, 36 objetos, T 100 000, **fundador limpio** (ENMIENDA 5), `juez.resumen_linaje` (sólo física).
- Métrica que decide: **R0 real** = nacimientos reales / (muertes + 1) por linaje-semilla; `cruza_real` = evaluable (≥ 5 muertes) y R0 real ≥ 0.90 y
  0 fundadores tras t 10 000. Una semilla "cruza" si más de la mitad de los 9 linajes cruzan. Reporto además persistencia (ENMIENDA 6), vida
  mediana, fundadores, causas.
- Semillas **33001–33005** (primera ola), 33006–33010 (confirmación si algo llega a ≥ 0.85 en 3/5). Siempre contra v14.3 fijo con la misma
  semilla; O1 como techo en las 5 primeras.

## Lo que ya sé antes de correr (leído de los crudos de la serie 14301–14320, `tronco_v14_3/datos`)
- v14.3: R0 real mediano 0.536 (réplica 0.63). **Mueren 34 171 fundadores contra 4 239 hijos.** El fundador vive 45 pasos, muere de sal o
  veneno y 98.8 % no pare. El hijo vive 1 401, 48.6 % muere sin parir, deja 1 hijo (mediana).
- O1: 0.9375. Sus fundadores también son malos (vida 200, 97.7 % sin parir) pero son pocos (fund med 0): el hijo vive 3 749 y deja 2.
- La palanca está en el HIJO establecido (que no se extinga el linaje) y en que el fundador ciego no muerda lo malo dos veces. El mundo
  no está sucio (2.4 % de pasos sin nada bueno): no es un problema de bien público.

## Las piezas como genes del cableado de `cruce/carros/CRUCE.py` (PASO_BOCA 1 → el gen suma al logit de morder; señales en [0, 1])
Escala: logit de FABRICA = Vb/0.3 con Vb = 1.2·valor + 2.0·hambre + 0.5. Sobre lo desconocido a E 0.6 vale ≈ +4.3; a E 0.2, ≈ +7. Por eso
uso genes **fuera del rango evolutivo [−4, 4]** (el motor no los recorta; lo declaro). ENSEÑA no es un gen: es un carro copia
(`carros/TRASP.py`, por anclas desde CRUCE.py; con ENSENA 0 es CRUCE bit a bit).

| brazo | qué | genes / perilla |
|---|---|---|
| v143 | el bicho real (genoma 0) | — |
| sac2 | saciedad literal de Prometeo s30006 (`CABLE reserva→boca −2`) | boca_{bueno,neutro,malo}_reserva −2 |
| sac6 | saciedad fuerte | boca_{bueno,neutro,malo}_reserva −6 |
| margen | O1 MARGEN: no come lo bueno cuando está lleno | boca_bueno_sesgo +6, boca_bueno_reserva −12 (cero en min(E,Ag) 0.75) |
| nomalo | la boca nunca muerde lo que ya sabe malo (SIEMPRE sólo en la boca) | boca_malo_sesgo −8 |
| limpia | O1 costeable: lo malo sólo si la otra necesidad está llena | boca_malo_sesgo −6, boca_malo_otra +8 (cero en max(E,Ag) 1.125) |
| neofobia | O1 PRUEBA: lo desconocido sólo con reserva | boca_neutro_sesgo −6, boca_neutro_reserva +15 (cero en min(E,Ag) 0.6) |
| patas | O1: va a lo que le sirve, no a lo más cercano | pata_act_sesgo +2, pata_otra_sesgo +1 |
| o1genes | O1 escrito en genes: margen + limpia + neofobia + patas | la suma de las cuatro filas |
| ensena1 | `ensena` (nacer/todo/hijo/copiar) sobre las dos filas lentas: el hijo nace con los valores de letra del padre | ENSENA 1 |
| ensena2 | `ensena` total: el hijo nace con todo el cerebro aprendido del padre (filas, Kenyon, ncod, patas) | ENSENA 2 |
| o1 | techo | carro O1 |

No se prueban, y digo por qué: **vida rápida** (menos dote, parir antes) son costos del MUNDO (`M['dote']`, `rep_X`), prohibidos por el
REGLAMENTO §4; **ojo/vista** es inerte en esta pista (el carro ya ve el anillo entero, opción A); **contención (APR)** ya está dentro de
v14.3 (OPCION 1) y se midió (SINTD).

## Predicciones firmadas (mediana sobre 5 semillas de la mediana por semilla del R0 real de los 9 linajes; v143 esperado 0.50–0.65)
| # | predicción | p |
|---|---|---|
| A1 | v143 en [0.45, 0.70] | 0.80 |
| A2 | O1 ≥ 0.85 | 0.90 |
| P1 | sac2 ≈ v143 (|dif pareada| ≤ 0.05) | 0.60 |
| P2 | sac6 < v143 en ≥ 4/5 (la saciedad tapa la limpieza y el comer antes del parto) | 0.50 |
| P3 | margen ≈ v143 (|dif| ≤ 0.05) | 0.60 |
| P4 | nomalo < v143 en ≥ 4/5 (precedente SIEMPRE) | 0.55 |
| P5 | limpia > v143 en ≥ 4/5 con dif ≥ 0.05 | 0.35 |
| P6 | neofobia > v143 en ≥ 4/5 con dif ≥ 0.05 (por los fundadores) | 0.35 |
| P7 | patas > v143 en ≥ 4/5 con dif ≥ 0.05 | 0.40 |
| P8 | o1genes es el mejor de los brazos de sólo genes, en [0.60, 0.80] | 0.50 |
| P9 | ensena1 > v143 en ≥ 4/5 con dif ≥ 0.10 | 0.55 |
| P10 | ensena2 es el mejor de todos, en [0.70, 0.85] | 0.45 |
| P11 | **ninguna combinación llega a R0 real ≥ 0.85 en ≥ 3/5 semillas** (regla de parada) | 0.70 |
| P12 | ninguna llega a ≥ 0.90 en ≥ 3/5 | 0.85 |
| P13 | en el mejor brazo, los fundadores siguen muriendo con vida < 100 y > 95 % sin parir (nada legal arregla al fundador ciego) | 0.75 |

Segunda ola (si hay tiempo): el mejor gen + ensena2; confirmación 33006–33010 sólo si algo cumple la regla de parada.
