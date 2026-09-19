# SUMMARY - Corrida 2: A0 contra E (mundo congelado)

- **experiment**: A0_vs_E_mundo_congelado (linea externa, mundo minimo)
- **hypothesis**: (preregistrada, del coordinador) A0 == E en todas las metricas,
  semilla a semilla, porque en este mundo no hay accion que la memoria informe.
- **changed_mechanism**: una sola modificacion: memoria episodica minima
  {state, action, reward, outcome}, local, <= 20 episodios, solo registro,
  sin consumo adicional de PRNG.
- **fixed_parameters**: mundo congelado completo (food_probability 0.32,
  metabolic_cost 0.35, threshold 9.0, p_rep 0.02, coste 2.0, hijo 7.5,
  max_population 12, rounds 180, founders 2).
- **number_of_seeds**: 1000 (0..999), pareadas.
- **R0**: A0 0.9415 | E 0.9415 (delta 0.0000)
- **extinction_rate**: A0 0.078 | E 0.078 (delta 0.000)
- **mean_final_population**: A0 2.978 | E 2.978 (delta 0.000)
- **lineage_statistics**: lineage_survival A0 0.714 / E 0.714;
  descendants_per_founder A0 1.243 / E 1.243; generaciones A0 1.226 / E 1.226.
- **result**: **IDENTIDAD EXACTA** en las 1000 semillas y en la genealogia completa
  (1000/1000 genealogias identicas, 0 discrepancias). La prediccion se cumplio.
  No hay efecto de la memoria, y no podia haberlo.
- **limitations**: el resultado no dice nada sobre el valor de la memoria
  episodica. Dice que el banco de pruebas elegido es incapaz de medirla. Un
  experimento que no puede fallar tampoco puede confirmar. Ademas la identidad
  depende de que E no consuma PRNG: es una propiedad de esta implementacion, no
  una garantia general.
- **SHA-256**: ver SHA256.txt y el sha del ZIP en el mensaje de entrega.

## Las cinco preguntas
1. **Prediccion**: A0 == E en todas las metricas, semilla a semilla, porque en este mundo no hay accion que la memoria pueda informar. Si difieren es un error de implementacion (PRNG), no un efecto.
2. **Que cambio**: solo se anadio memoria episodica de registro a E. Nada mas.
3. **Resultado**: identidad exacta semilla a semilla, incluida la genealogia.
   delta_R0 = 0.0000, delta_extincion = 0.000.
4. **Replica**: trivialmente replicable (determinista). Se replica ademas con
   semillas 1000..1999 dentro de la corrida 3.
5. **Explicacion alternativa**: ninguna compite. La identidad es analitica, no
   empirica: la memoria no entra en ninguna rama de la dinamica ni toca el PRNG.
   La unica alternativa era un bug, y la comparacion campo a campo mas la
   genealogia lo descartan. Advertencia: si alguien presentara esta identidad
   como "la memoria no dana", seria una lectura tramposa; lo correcto es decir
   que el experimento estaba vacio por construccion.
