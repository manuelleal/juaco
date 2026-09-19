# SUMMARY - Corrida 1: calibracion

- **experiment**: calibracion_barrido_food_probability (linea externa, mundo minimo)
- **hypothesis**: con food_probability = 0.32 el mundo queda en R0 ~ 1 y extincion
  < 0.50, y se reproducen los numeros de la referencia externa.
- **changed_mechanism**: ninguno respecto del protocolo; solo se barre
  food_probability para verificar y despues se congela en 0.32.
- **fixed_parameters**: founders 2, initial_energy 10.0, metabolic_cost 0.35,
  food_energy 1.0, reproduction_threshold 9.0, reproduction_probability 0.02,
  reproduction_cost 2.0, newborn_initial_energy 7.5, max_population 12,
  rounds 180.
- **number_of_seeds**: 1000 (0..999) por cada valor del barrido.
- **R0** (0.32 congelado): 0.9415 (SEM 0.0227)
- **extinction_rate** (0.32): 0.078
- **mean_final_population** (0.32): 2.978
- **lineage_statistics** (0.32): lineage_survival 0.714 (fraccion de linajes con al
  menos un vivo al final), descendants_per_founder 1.243, generaciones medias 1.226,
  tiempo medio de supervivencia 125.96 rondas.
- **result**: el barrido es monotono y cruza R0 = 1 entre 0.32 y 0.33. En 0.32 se
  reproduce la referencia dentro de ~1.1 errores estandar en R0 y menos de 0.5 en
  extincion y poblacion. Mundo CONGELADO en 0.32.
- **limitations**: (a) no hay reproduccion bit a bit posible sin el codigo
  original; (b) el protocolo no fija si los pasos 2..6 van por fases o por
  organismo, ni si el recien nacido actua en su ronda de nacimiento, ni si la
  tirada de reproduccion se consume cuando no hay espacio: se declararon D1..D4 en
  el encabezado del motor y cambiarlas mueve el R0 en el tercer decimal; (c) 1000
  semillas dejan un SEM de ~0.023 en R0, asi que "R0 = 0.9665" y "R0 = 0.9415" no
  son distinguibles con esta N.
- **SHA-256**: ver SHA256.txt y el sha del ZIP en el mensaje de entrega.

## Las cinco preguntas
1. **Prediccion (escrita antes)**: el barrido sera monotono creciente en R0 y
   decreciente en extincion; 0.32 dara R0 cerca de 1 y extincion < 0.1.
2. **Que cambio**: solo food_probability, un valor por arm. Nada mas.
3. **Resultado**: monotonia confirmada; 0.32 -> R0 0.9415, extincion 0.078,
   poblacion 2.978. Compatible con la referencia.
4. **Replica**: el barrido completo es determinista y se rehace ejecutando
   `python run_calibracion.py`; la replica con semillas nuevas se hace en la
   corrida 3 (variante de parches, semillas 1000..1999).
5. **Explicacion alternativa**: la coincidencia con la referencia puede deberse a
   que el mundo es poco sensible a los detalles de implementacion en este rango
   (cualquier lectura razonable del protocolo daria numeros parecidos), no a que
   hayamos reconstruido exactamente el codigo original. Esto NO es evidencia de
   que la implementacion sea la misma.
