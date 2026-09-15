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

## Estado (día 3 — repo en Claude Code, 15 sep 2026)
- **Traspaso VALIDADO**: batería 20/20, baseline reproducido bit a bit (259/260 celdas; la única diferencia es
  redondeo del CSV viejo). Repo git con tag `v6-baseline`. `.gitattributes` con `* -text`: sin eso, git convierte
  LF→CRLF y **rompe los 55 hashes sha256 en cualquier clon**.
- Etapa 1 (aprende A/B): cerrada, 20/20 en v6.
- Etapa 2 (inversión, extinción, estímulo nuevo, valencias opuestas): cerrada en valor. Ver registro.
- Problema abierto de conducta: política bajo hambre (mordidas de veneno 1–4% por visita en inanición). Fase 2P.
- **v7 NO congelado.** Pasa 20/20 todos los criterios científicos, pero falla `splits==0` en E2I (19/20).
  El criterio estaba mal escrito (ERR-06): E2I deja C∩A y C∩B libres, no es una etapa sin error crónico.
  Criterio v2 preregistrado en el registro; pendiente volver a correr. v6 sigue siendo el tronco.
- **Umbral de división 2L en 2 celdas compartidas**: con 0 o 1 nunca dispara, con 2 o 3 siempre. Seis condiciones
  independientes. Dos vías de disparo: representación (solapamiento) y valor (inversión).
- **Fase 1 hecha**: `experimentos/run_etapa.py` + `analiza.py`, paralelo 6.3×, equivalencia 20/20 bit a bit.
  Desbloquea las 100 semillas del punto 8 del brief.
- **Etapa 3 (generalización): predicción sostenida al 100%**, residuo exactamente 0.000 en 1.280 pares.
  Alcance nulo: 15.9% de los patrones reciben W=0 exacto. PERO el diseño era demasiado fácil (la identidad es
  mecánica con A∩B=0); la versión dura está preregistrada y sin correr.
- Variabilidad y diversidad medidas por primera vez: **sd(W_A)=0.0000** — el valor aprendido no tiene diversidad
  entre semillas; la conducta sí (CV 7–9%).
- 2K-bis redefinida por decisión del director: capacidad = nº de estímulos y celdas gastadas por estímulo.
- Rama 2M (pulpo/distribución): refutada a 6 estímulos; especialización emerge. NO tocar salvo decisión explícita.
- Bug de sincronía sensor-acción corregido en v6; cifras anteriores a v6 se reproducen aproximadamente, no exactamente.
- Seis errores de instrumento documentados. Cuando algo se vea raro: primero el instrumento, siempre.

## Comandos
```
# IMPORTANTE en Windows: la consola es cp1252 y revienta al imprimir ≈ → ∩ (UnicodeEncodeError).
PYTHONIOENCODING=utf-8 python bateria.py 6     # (desde organismo/) regresión rápida
PYTHONIOENCODING=utf-8 python bateria.py 20    # regresión completa
python organismo/bateria_v7.py 20              # examen de congelación de v7 (ya trae reconfigure utf-8)

python experimentos/run_etapa.py --etapa E1 --semillas 20        # paralelo, ~13 s
python experimentos/run_etapa.py --etapa E1 --semillas 20 --verificar-equivalencia
python experimentos/analiza.py --etapa E1 --baseline

python -c "import organismo_v6 as o; print(o.run(1))"   # una corrida (~4 s)
```
