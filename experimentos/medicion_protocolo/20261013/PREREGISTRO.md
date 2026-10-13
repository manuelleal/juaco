# PREREGISTRO — Medición del protocolo con errores sembrados (13-oct-2026)

Commiteado antes de sembrar y antes de auditar. Nada de lo de abajo se cambia después de ver datos; si hay que cambiarlo, es un ERR numerado.

## Pregunta
¿Qué fracción de los errores de un bloque atrapa el auditor del protocolo cuando no sabe que hay errores sembrados, y cuántas falsas alarmas da?

Motivo: "105 de 120 errores no alteraron una conclusión" cuenta sólo los errores que alguien encontró. No es una tasa de detección. Esta es la primera medida directa.

## Diseño
- **Unidad:** una copia de un bloque cerrado. Cada copia tiene cero o un defecto sembrado.
- **Bloques:** 10 carpetas de `experimentos/` con veredicto registrado y con PREREGISTRO, corre_*.py y JSON de resultados presentes. El sembrador las elige con `random.Random(20261013)` sobre las filas de `experimentos/INDICE.md` que cumplan eso, y escribe la lista en `siembra/SELECCION.md` antes de sembrar.
- **Siembra:** 40 copias con defecto + 20 copias limpias = 60 copias. Distribución de los 40, proporcional al registro (`informe/resumen_errores.md`): 18 criterio, 16 instrumento, 6 lectura u otro. Un defecto por copia. Cada defecto debe ser detectable leyendo los archivos de la copia, sin correr la serie.
- **Sellado:** `CLAVE.csv` queda fuera del repo; su sha256 se commitea en `siembra/CLAVE.sha256` antes de la auditoría.
- **Auditoría:** `metodo-auditor-ciego` (Sonnet) recibe las 60 carpetas en orden barajado con la misma semilla, sin la clave ni este preregistro, y entrega `HALLAZGOS.csv`.
- **Puntaje:** `siembra/puntua.py` (escrito por el sembrador, revisado antes de correr) cruza HALLAZGOS contra CLAVE. Un acierto = la copia con defecto tiene al menos una fila con `defecto=si` cuyo archivo coincide con el de la clave. Falsa alarma = copia limpia con alguna fila `defecto=si` de confianza alta o media.

## Métricas
- Sensibilidad total y por tipo (criterio, instrumento, lectura/otro), con intervalo de Wilson al 95 %.
- Tasa de falsas alarmas sobre las 20 limpias.
- Tiempo del auditor por copia (de sus notas).

## Predicciones (escritas antes de correr)
- P1: sensibilidad total entre 0,40 y 0,70.
- P2: instrumento se atrapa más que criterio (los ERR de instrumento tienen archivo:línea obvio; los de criterio exigen leer el preregistro contra el JSON).
- P3: falsas alarmas ≤ 3 de 20.

## Criterios de decisión (se escriben ahora)
- Si sensibilidad en instrumento < 0,50: el auditor NO cuenta como control para errores de instrumento; el protocolo pasa esas comprobaciones a código (fase 2, punto 1 del plan).
- Si falsas alarmas > 5 de 20: el formato de hallazgos se cambia para exigir "dato que confirma" obligatorio antes de contar.
- Si sensibilidad total < 0,30: FUNCIONA NO para el auditor de lectura; el protocolo depende de los controles automáticos y se dice así en público.
- Si ≥ 0,70 en todos los tipos y falsas alarmas ≤ 3: FUNCIONA. Entre medio: HAY ALGO MODESTO.

## Réplica
Si el resultado cruza un umbral de decisión por una sola copia, se repite con 20 copias nuevas (semilla 20261014) antes de declarar.

## Lo que esta medición NO dice
- No mide errores que ningún sembrador imaginó.
- Los defectos sembrados por un agente Claude los audita otro agente Claude: puede haber sesgo compartido. Se repetirá con un auditor de otra familia cuando esté conectado (fase 2).
- Es un solo proyecto y un solo auditor.

## Siguiente ERR libre
ERR-196.
