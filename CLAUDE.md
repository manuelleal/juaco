# Proyecto: Organismo artificial mínimo (Artificial Life)

Investigación reproducible sobre si un organismo artificial simple, con reglas locales y sin backpropagation,
puede aprender, desaprender, generalizar y (más adelante) transmitir conocimiento. Dirección: Christiam Puentes.
Colaborador técnico: Claude. Todo corre en CPU con Python 3 + NumPy.

## Fuente de verdad
- `registro/REGISTRO_etapas_1_2.md` — historial completo, criterios preregistrados, resultados, errores. LEER PRIMERO.
- `registro/HANDOFF.md` — narrativa completa de lo hecho y por qué.
- `registro/PLAN.md` — qué sigue y cómo.
- `organismo/organismo_v6.py` — organismo congelado (hash 5f38f83cf49248a3). `organismo/bateria.py` — regresión.
- `organismo/organismo_v7c.py` — CANDIDATO v7 = v6 + 2L plasticidad estructural (212f0746d52577c7). `bateria_v7c.py` (21b97967e48ed971).
  Se congela como v7 SOLO si pasa `python3 bateria_v7c.py 20` en este repo.
- `datos/` — CSV/JSON de cada experimento. `datos/baseline_v6.csv` es el baseline de referencia.

## Reglas de trabajo (no negociables)
1. Antes de tocar nada: `cd organismo && python3 bateria.py 6`. Debe salir todo PASA. Si no, detenerse.
2. Un cambio por experimento. Cada experimento es una hipótesis con: qué cambia, predicción numérica,
   criterio de refutación y métricas — escritos ANTES de correr, en el registro.
3. Nunca recalibrar un parámetro a posteriori para que el criterio pase. Si el criterio estaba mal, se registra
   el error y se decide un criterio nuevo antes de volver a correr.
4. Distinguir siempre tres capas: representación (códigos Kenyon), valor aprendido (Wp−Wn), política (decisión bajo hambre).
   Un fallo de conducta no es un fallo de aprendizaje hasta que se demuestre.
5. Ante una anomalía, la primera hipótesis es el instrumento (criterio, unidades, aliasing, disponibilidad).
   Tres de tres anomalías del proyecto fueron del instrumento.
6. Semillas fijas (1..N), T=100000 salvo indicación. Reportar medianas y rangos, nunca solo medias.
7. Guardar cada resultado en `datos/` con nombre de etapa, y añadir una línea al registro con hash (sha256 corto) del script.
8. No declarar AGI, conciencia ni inteligencia general por ningún resultado. Vocabulario permitido: aprende, revierte,
   extingue, generaliza, transfiere — solo cuando el criterio preregistrado lo respalde.
9. Preferencia del director: preguntarle y proyectar hacia adelante, no frenarlo; discrepar con datos, no con cautela genérica.

## Estado al traspaso (16 sep 2026)
- Etapa 1 (aprende A/B): cerrada, 20/20 en v6.
- Etapa 2 (inversión, extinción, estímulo nuevo, valencias opuestas): cerrada en valor. Ver registro.
- Problema abierto de conducta: política bajo hambre (mordidas de veneno 1–4% por visita en inanición).
- 2L (plasticidad estructural) pasa la batería con 6 semillas; pendiente 20 semillas para congelar v7.
- 2K-bis (capacidad) parcialmente respondida por 2L: con plasticidad el techo se resuelve dividiendo. Redefinir antes de correr.
- Rama 2M (pulpo/distribución): refutada a 6 estímulos; especialización emerge. NO tocar salvo decisión explícita.
- Bug de sincronía sensor-acción corregido en v6; cifras anteriores a v6 se reproducen aproximadamente, no exactamente.

## Comandos
```
cd organismo && python3 bateria.py 6          # regresión rápida (~1 min)
cd organismo && python3 bateria.py 20         # regresión completa
python3 -c "import organismo_v6 as o; print(o.run(1))"   # una corrida
```
