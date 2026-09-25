# EXPLORATORIO, no es dato

# Predicciones del explorador Fable ANTES de correr la cadena trófica (25-sep-2026, escritas antes del primer humo con semillas)

Misión: llegar a la AGI por este camino; el método manda sobre el cómo. Esto es un juguete de 2 horas, 4 semillas, sin valor de veredicto.

Diseño que voy a correr: 4 especies (gusano, gallina, oso, humano) en un toro 2D continuo, cada una con cinta genética (SUM/REP/FIN/TASA),
copia con errores, rasgos con costo (veneno, escudo, velocidad, vista, tamaño, eta, hambre, huida), cerebro que aprende valencias por
señal de la presa con regla delta. Brazos: EVO (cintas evolucionan), FIJO (cintas copiadas sin error), SINVENENO (evolucionan pero el
veneno se fuerza a 0). Semillas 32001–32004. T objetivo 40 000 pasos (~300+ generaciones del gusano).

| # | predicción | mi probabilidad |
|---|---|---|
| P1 | La cadena NO se sostiene completa: el HUMANO se extingue primero (antes del paso 8 000) en ≥ 3/4 semillas de EVO; el OSO le sigue. El gusano nunca se extingue. | 0.75 |
| P2 | Con evolución, el veneno medio del gusano sube por encima de 0.3 en ≥ 3/4 semillas antes del paso 15 000; el escudo de la gallina sube DESPUÉS (rezago ≥ 2 000 pasos) y nunca alcanza al veneno. | 0.55 |
| P3 | FIJO colapsa igual o antes que EVO (misma orden de extinción). La evolución no salva a nadie de arriba; a lo sumo alarga la vida de la gallina. | 0.6 |
| P4 | Ciclos depredador-presa gusano–gallina visibles a ojo (≥ 3 picos alternados con desfase) en ≥ 2/4 semillas. | 0.6 |
| P5 | Velocidad: la gallina sube su velocidad (x_vel > +0.3 en log) y el gusano también pero menos; el oso y el humano no viven lo suficiente para fijar nada. | 0.5 |
| P6 | SINVENENO: la gallina vive MÁS que en EVO (el veneno del gusano es lo que la mata en EVO). | 0.55 |
| P7 | Rareza esperada: en alguna semilla el veneno del gusano extingue a la gallina y luego el veneno DECAE (costo sin depredador). | 0.4 |
| P8 | El cerebro (valencias) hará que las gallinas eviten a los gusanos con veneno alto: la correlación entre veneno del gusano y probabilidad de ser comido será negativa a partir del paso ~5 000. | 0.5 |

Lo que más miedo me da: calibrar la energía para que 4 niveles vivan a la vez sin vivero. Es probable que gaste la mitad del tiempo en eso
y que el reporte diga "colapsó por calibración, no por biología". Lo diré tal cual si pasa.
