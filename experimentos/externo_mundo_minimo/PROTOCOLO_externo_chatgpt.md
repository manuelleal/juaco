# PROTOCOLO EXTERNO (ChatGPT, entregado por el director el 18 sep 2026, 19:15) — mundo mínimo, calibración y A0 contra E

Texto del protocolo tal como llegó (resumen fiel; el original está en la conversación del director):

## Parámetros congelados del mundo (A0)
founders = 2 · initial_energy = 10.0 · metabolic_cost = 0.35 por ronda · food_probability = 0.32 · food_energy = +1.0 ·
reproduction_threshold = 9.0 · reproduction_probability = 0.02 · reproduction_cost = 2.0 · newborn_initial_energy = 7.5 ·
max_population = 12 · rounds = 180 · seeds = 0 … 999. Muerte: si energy <= 0 muere de inmediato e irreversiblemente.

## Dinámica por ronda
1. Mezclar al azar el orden de los organismos. 2. Cada organismo paga energy -= 0.35. 3. Con probabilidad 0.32 recibe energy += 1.0.
4. Si energy <= 0 muere. 5. Si sigue vivo y energy >= 9.0 puede reproducirse con probabilidad 0.02 si hay espacio (población < 12).
6. Al reproducirse: parent.energy -= 2.0; el hijo nace con energy = 7.5. 7. El hijo hereda sólo el identificador de linaje. 8. ID nuevo.

## Linajes
founder 0 → lineage 0; founder 1 → lineage 1; los descendientes conservan el linaje; la genealogía debe reconstruirse.

## R₀ (definición operacional)
NO usar births/deaths. R₀ = media, sobre 1000 semillas, de (hijos directos del fundador 0 + hijos directos del fundador 1) / 2.

## Extinción
Semilla extinta si population == 0 al final de las 180 rondas. extinction_rate = extinct_seeds / 1000. Objetivo: R₀ ≈ 1 y extinción < 0.50.

## Referencia a reproducir
food_probability = 0.32 → R0 = 0.9665, extinction_rate = 0.082, mean_final_population = 3.028.
SHA-256 del reporte externo: 4af8d5eea3d6309b16851202c7c24f12584f2f1076fbc28777f0139afcb1d833.

## Reproducibilidad
PRNG determinista; semillas exactamente 0..999; guardar código, parámetros, resultados por semilla, resumen, genealogía y SHA-256.

## Calibración previa
Barrer food_probability ∈ {0.29, 0.30, 0.31, 0.32, 0.33, 0.34} sólo para verificar; elegir 0.32 y CONGELAR el mundo.

## Principio: una sola modificación por experimento
No cambiar a la vez reproducción, metabolismo, alimento, mortalidad, tamaño poblacional, fundadores ni rondas.

## Siguiente experimento: A0 contra E (memoria episódica mínima)
E = A0 + memoria episódica {state, action, reward, outcome}, local, limitada, sin acceso global, sin futuro, sin otros organismos;
sin backprop, sin gradientes globales, sin supervisor. Mismas semillas 0..999, comparación pareada. Métricas primarias: R0,
extinction_rate, lineage_survival, descendants_per_founder; secundarias: mean_final_population, mean_survival_time,
number_of_generations, memory_usage. Criterio de éxito: no basta mean_R0(E) > mean_R0(A0); exige extinción ≤, ventaja
reproducible en semillas nuevas, efecto consistente (no de pocas semillas), genealogía real, muerte real, sin información global,
sin intervención externa. Si E no cumple: REGISTRAR FALLA.

## Programa posterior
A0 → E → S → E+S → E+S+R → E+S+R+X; después W, C, comunicación, herencia, planificación. Pregunta evolutiva posterior: A (sin
herencia), B (representación semántica heredada), C (episodios heredados), D (representación + regla de plasticidad), E
(representación + política de replay).

## Regla científica
No demostrar que funciona: intentar romperlo. Cada experimento contesta: predicción, qué cambió, resultado, réplica, explicación
alternativa. FAIL es resultado válido; si funciona, REPLICATE con semillas nuevas.

## Entregables por corrida
README.md, PARAMETERS.json, RESULTS.json, PER_SEED_RESULTS.json, GENEALOGY.json, SUMMARY.md, SHA256.txt y un ZIP reproducible.
El resumen indica: experiment, hypothesis, changed_mechanism, fixed_parameters, number_of_seeds, R0, extinction_rate,
mean_final_population, lineage_statistics, result, limitations, SHA-256.

---

## Nota del coordinador (antes de correr, 19:20)
1. Este mundo NO es el organismo JUACO (sin retina, sin valor, sin código): es una ecología de juguete. Se corre como línea externa
   (`experimentos/externo_mundo_minimo/`) y sus números no entran en la escalera del proyecto; sirven para calibrar la idea de R₀.
2. En este mundo el organismo no toma NINGUNA acción: la comida es una moneda al aire independiente del organismo. Por construcción,
   una memoria episódica no puede cambiar nada (no hay decisión que informar). Predicción escrita antes: A0 ≡ E en todas las
   métricas, semilla a semilla. Si E difiere, es un error de implementación (rng consumido de forma distinta), no un efecto.
3. Corrección mínima que se prueba como HIPÓTESIS APARTE (una sola modificación): dos parches con probabilidades de comida
   distintas (0.42 y 0.22; media 0.32, la misma que el mundo congelado) y una acción por ronda: elegir parche. A0 elige al azar
   (media 0.32); E recuerda (parche, resultado) y elige el parche con mejor recompensa media reciente (memoria de ≤ 20 episodios).
   Predicción: E sube R₀ y baja la extinción respecto de A0 en esa variante; control BARAJA (E con la memoria barajada) ≈ A0.
