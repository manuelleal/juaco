# SUMMARY - Corrida 3: variante de parches (hipotesis aparte)

- **experiment**: variante_parches_A0P_EP_BARAJAP (linea externa, mundo minimo)
- **hypothesis**: E-P sube R0 y baja la extincion respecto de A0-P en >= 60 % de las semillas pareadas; BARAJA-P ~ A0-P (control con la contingencia accion<->recompensa rota).
- **changed_mechanism**: UNA sola modificacion: dos parches de comida (0.42 y
  0.22, media 0.32) mas una accion por ronda (elegir parche). Nada mas cambia.
- **fixed_parameters**: founders 2, initial_energy 10.0, metabolic_cost 0.35,
  food_energy 1.0, reproduction_threshold 9.0, reproduction_probability 0.02,
  reproduction_cost 2.0, newborn_initial_energy 7.5, max_population 12,
  rounds 180. Memoria <= 20 episodios, epsilon 0.10 declarada.
- **number_of_seeds**: 1000 principales (0..999) + 1000 de replica (1000..1999),
  los tres brazos sobre las mismas semillas.
- **R0**: A0-P 0.9555 | E-P 1.8625 | BARAJA-P 0.9240   (replica: 0.9215 | 1.9255 | 0.9165)
- **extinction_rate**: A0-P 0.087 | E-P 0.008 | BARAJA-P 0.092
  (replica: 0.070 | 0.007 | 0.101)
- **mean_final_population**: A0-P 3.012 | E-P 7.623 | BARAJA-P 2.923
- **lineage_statistics**: lineage_survival A0-P 0.708 | E-P 0.908 | BARAJA-P 0.707;
  descendants_per_founder A0-P 1.285 | E-P 3.256 | BARAJA-P 1.237;
  generaciones A0-P 1.267 | E-P 2.124 | BARAJA-P 1.256.
- **result**: **PREDICCION CUMPLIDA Y REPLICADA**. E-P supera a A0-P en R0 en el
  70.8 % de las semillas (replica 74.8 %), por encima del umbral preregistrado
  del 60 %; la extincion cae de 0.087 a 0.008. El control BARAJA-P es
  indistinguible de A0-P (fraccion de semillas mejor 0.333, p = 0.163), lo que
  descarta que el efecto venga de tener memoria y no de USAR la contingencia.
- **limitations**: (1) el pareado es por semilla, no por trayectoria: los brazos
  divergen en el consumo del PRNG desde la primera ronda; (2) el efecto era
  predecible analiticamente (epsilon 0.1 sobre un parche 0.42 lleva la energia
  neta de -0.03 a +0.06 por ronda): esto mide que un bandido de dos brazos se
  resuelve con dos medias, no que haya cognicion; (3) el tope de 12 organismos
  satura con E-P (poblacion final 7.623), asi que R0 esta censurado por arriba y
  el efecto medido es una cota inferior; (4) E-P solo elige el parche rico el
  74.3 % de las veces, muy por debajo del 95 % que permite epsilon: la memoria de
  20 episodios binarios es ruidosa y los recien nacidos nacen sin memoria; (5)
  todo esto sigue siendo una ecologia de juguete, no el organismo JUACO.
- **SHA-256**: ver SHA256.txt y el sha del ZIP en el mensaje de entrega.

## Las cinco preguntas
1. **Prediccion (preregistrada)**: E-P sube R0 y baja la extincion respecto de A0-P en >= 60 % de las semillas pareadas; BARAJA-P ~ A0-P (control con la contingencia accion<->recompensa rota).
2. **Que cambio**: solo la estructura de la comida (dos parches en vez de uno,
   misma media) y la existencia de una accion. La regla de decision distingue los
   tres brazos; el mundo es el mismo para los tres.
3. **Resultado**: E-P R0 1.8625 contra A0-P 0.9555 (delta +0.9070); extincion 0.008
   contra 0.087 (delta -0.079); 70.8 % de semillas con R0 mayor. BARAJA-P se queda
   pegado a A0-P.
4. **Replica**: semillas 1000..1999, efecto del mismo tamano y signo
   (delta R0 +1.0040, delta extincion -0.063, 74.8 % de semillas mejor). No depende
   de unas pocas semillas: el test de signos da p = 1.79e-94 sobre 843 pares
   discordantes.
5. **Explicacion alternativa**: la que mas peso tiene es que E-P no esta
   "recordando" nada interesante, sino estimando dos medias; el resultado es una
   propiedad del bandido, no del organismo. Una segunda alternativa -que el
   beneficio venga del simple hecho de llevar memoria, o de que E-P consuma el
   PRNG de otra forma- queda descartada por BARAJA-P, que lleva exactamente la
   misma memoria, el mismo consumo de PRNG y la misma regla, y no mejora nada.
   Lo que el experimento sostiene es estrictamente esto: cuando existe una accion
   cuyo resultado se puede registrar, registrar la contingencia paga; cuando no
   existe accion (corrida 2), la memoria es literalmente inerte.
