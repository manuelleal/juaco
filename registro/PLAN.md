# PLAN — Traspaso a Claude Code y etapas siguientes

## Fase 0 — Validar el traspaso (primera sesión, ~20 min)
1. `git init`, commit inicial con este bundle. Etiquetar `v6-baseline`.
2. `cd organismo && python3 bateria.py 6` → todo PASA. Luego `python3 bateria.py 20`.
3. Reproducir `datos/baseline_v6.csv`: 20 semillas, A_sin y B_aprende. Comparar medianas con el registro
   (comida 1400/338, veneno Q4 370/13, muertes 218/142, W_A +1.00, W_B −3.00). Si coincide, el traspaso está validado.
4. Añadir al registro una línea: "Traspaso validado en Claude Code, fecha, hash".

## Fase 1 — Infraestructura mínima (una sesión)
- `experimentos/run_etapa.py --etapa <nombre> --semillas N` que llama a `organismo_v6.run` con el escenario, escribe
  `datos/<etapa>_<fecha>.csv` y `.json` (por semilla: mord, vis, W, comp, deaths, log), y añade una línea al registro con hash.
- Paralelizar semillas con `multiprocessing` (una semilla por proceso). 100 semillas × 100k pasos debe caber en minutos.
- Script `analiza.py`: medianas, rangos, tasas por visita, y la comparación con el baseline.
- Convención: nunca sobrescribir un CSV; cada corrida tiene fecha.

## Fase 2 — Cerrar lo abierto de la Etapa 2
### 2L → v7 (PRIMERO)
`cd organismo && python3 bateria_v7c.py 20`. Si todo PASA (incluido divisiones=0 en etapas normales), renombrar a organismo_v7.py,
hash, commit `v7`. Luego repetir baseline 20 semillas con v7 y comparar con v6. Si algo falla, 2L vuelve a hipótesis.

### 2K-bis — Capacidad representacional (hipótesis derivada del organismo)
Pregunta: qué ocurre cuando la demanda de representación se aproxima al techo.
Condiciones (un cambio por corrida, 20 semillas): D∩B = 0,1,2,3 con clip=3; y D∩B=1,2 con clip=1.5.
Predicción: degradación graduada creciente con solapamiento (ya medida: W_B −3.00/−2.9/−2.78 en 0/1/2 celdas);
con 3 celdas (códigos idénticos) W_D y W_B convergen al mismo valor intermedio (fallo completo); con clip reducido
el fallo aparece a menor solapamiento. Refutación: si con 3 celdas los valores se separan, hay un mecanismo no identificado.
Métricas: W_D, W_B por cuarto; Wp/Wn de ambos; celdas al tope; tasas por visita; muertes.

### 2P — Política bajo hambre (NO recalibrar α a ciegas)
Antes de correr: decidir el criterio (adoptado: tasa por visita condicionada al hambre) y escribir la función objetivo
de la política (p.ej. minimizar muertes sujeto a no dejar de comer). Luego barrer α, β=hambre_boca y b=+0.5 como
hipótesis explícitas, 20 semillas, y reportar la superficie completa, no el mejor punto.

### Semilla congelada de v4
Con v6 no reaparece en 20 semillas. Correr 100 semillas de E1 y contar fallos (comida<100). Si 0/100, cerrar.

## Fase 3 — Etapa 3: Generalización (plan original, punto 10)
Hipótesis: el organismo aprendió "estos píxeles = comida" y no una característica abstracta.
Pruebas: patrones con 1 píxel cambiado (ruido), patrones desplazados, combinaciones. Medir W del patrón nuevo ANTES de
la primera mordida (valor a priori) y cuántas mordidas tarda en converger. Predicción con Kenyon: generalización
proporcional al solapamiento de códigos, no a la similitud visual — eso es una predicción falsable y distintiva.

## Fase 4 — Etapa 4: Memoria (punto 11)
Comparar memoria cero / parcial / heredada tras muerte. Ya sabemos: olvido 5% por muerte × 400 muertes = amnesia total.
Barrer olvido_muerte ∈ {0, .01, .05} y medir recuperación.

## Fase 5 — Población (puntos 12–14), solo cuando el individuo esté cerrado
Retomar `poblacion2.py` con v6. Cambios ya identificados (uno por vez): renacer heredando Wp/Wn del mejor (no en blanco);
score que pese el veneno; compartir solo el canal aversivo vs solo el apetitivo. Pregunta: ¿acumula la población algo que un
individuo no alcanza en una vida? Criterio de emergencia (punto 14): propiedad ausente en el individuo, presente en el grupo,
no programada, reproducible, y que desaparece al romper la estructura.

## Fase 6 — Publicación
- Repo público con README que reproduzca el baseline en un comando.
- Texto de ~3 páginas: la cadena 2A→2G como "un organismo que pide la teoría a golpes", con la limitación metodológica.
- Figura 1: valores W_A, W_B por cuarto en E1/E2 (12 semillas). Figura 2: interferencia vs solapamiento (0/1/2 celdas).
- Venue candidato: ALIFE / Artificial Life journal / arXiv q-bio.NC. No prometer más de lo que la batería demuestra.

## Reglas de sesión en Claude Code
Empezar cada sesión con la batería. Terminar cada sesión con una línea en el registro. Nunca dos cambios a la vez.
Traer el registro al chat de diseño cuando haya que decidir qué hipótesis sigue.
