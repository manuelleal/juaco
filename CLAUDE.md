# Proyecto: Organismo artificial mínimo (Artificial Life)

Investigación reproducible sobre si un organismo artificial simple, con reglas locales y sin backpropagation,
puede aprender, desaprender, generalizar y (más adelante) transmitir conocimiento. Dirección: Christiam Puentes.
Colaborador técnico: Claude. Todo corre en CPU con Python 3 + NumPy.

## Fuente de verdad
- `registro/REGISTRO_etapas_1_2.md` — historial completo, criterios preregistrados, resultados, errores. LEER PRIMERO.
- `registro/HANDOFF.md` — narrativa completa de lo hecho y por qué.
- `registro/PLAN.md` — qué sigue y cómo.
- **`organismo/organismo_v8.py` — EL TRONCO desde el 16 sep 2026** (dca7d5c3a162f5d4, tag `v8-tronco`).
  v8 = v6 + 2L plasticidad estructural + drenaje de la parte común de Wp/Wn (`lam=0.05`). Pasó la prueba de coste
  y el examen criterio v3, 20/20. `organismo/bateria_v8.py` (8de16b2e97de8312) es su examen y su regresión.
- `organismo/organismo_v6.py` — tronco anterior, congelado como referencia (5f38f83cf49248a3). `organismo/bateria.py`.
- `organismo/organismo_v7.py` — instrumentación inerte de v7 (3db0475ef0ea95ce). **NO sobrescribir nunca**: de él
  dependen bateria_v7/v7b, los controles de inercia de BUG-01 y el ancla del sandbox. v7c/bateria_v7c: históricos.
- `datos/` — CSV/JSON de cada experimento. `datos/baseline_v6.csv` es el baseline de referencia.
- **`sandbox/` (fuera del repo, en `JUACO/sandbox/`) es de un ejecutor externo sin juicio; sus resultados son
  hipótesis, nunca datos.** Regla de cruce completa en `sandbox/README.md` y en el registro: nada entra aquí
  sin verificar hashes, reproducir en repo, pasar `bateria.py 20` y `manifiesto.py`, y etiquetar el origen.

## Reglas de trabajo (no negociables)
1. Antes de tocar nada: `cd organismo && python3 bateria.py 6` **y** `python bateria_v8.py 6` (tronco).
   Debe salir todo PASA (y `manifiesto.py --check` intacto). Si no, detenerse.
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
10. **Todo script de más de un minuto: una línea de progreso por etapa con marca de tiempo, y salida a
    archivo DESDE EL ARRANQUE, no sólo al final.** Un script sano que calla seis minutos es indistinguible
    de uno colgado, y esa ambigüedad ya costó una salida entera (día 3). Referencia: `corre_ahorro.py`.
11. **Repo y sandbox nunca corren a la vez; el repo tiene prioridad.** El sandbox arranca sólo con el repo
    parado y con `Pool(6)`, no 16. El tiempo de pared es un dato y se contamina al solapar.

## Estado (día 4 — 16 sep 2026). Manda sobre el bloque del día 3 cuando se contradigan
- **v8 ES EL TRONCO (tag `v8-tronco`).** Pasos 2 y 3 fundidos por dirección: examen criterio v3 20/20
  (`experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md`, datos `examen_v8_20260916_145204`).
  - 4c: C∩B=3 de misma valencia → **0 divisiones**, y C hereda `W=−3.00` sin experiencia propia.
  - 4b: sin conflicto no hay división, 61/61.
  - En las seis etapas v8 no trunca nunca (ahí es v7); lo que lo distingue es la prueba de coste.
- **v7 NO se congeló nunca como tronco y `organismo_v7.py` no se toca.** Hay una copia externa del repo
  (`PROYECTOS/Nueva carpeta/bundle`) que afirma "v7 congelado": es **falsa** y no se fusiona nunca
  (`registro/AUDITORIA_copia_antigravity_20260916.md`).
- **ERR-12:** "ley de disparo `err>0.6`, 320/320" era una **identidad del código** (la división compara la misma
  cantidad), y "con solapamiento 0 no puede disparar" es **falso**: E2 divide con A∩B=0 por conflicto temporal.
  No citar esa concordancia como evidencia.
- **La prueba de AHORRO del día 3 SÍ corrió** y su lectura es nula por ERR-11.
- **Paso 1, prueba de coste con el techo mordiendo: PASA**, con 14/14 predicciones preregistradas
  (`experimentos/bug01/PREREGISTRO_coste_techo.md`, datos `coste_techo_20260916_142116`).
  - Antes de la primera truncación del clip, `lam=0` y `lam=0.05` son **idénticos** (20/20).
  - Después, el control no reaprende nunca; el arreglo tiene ahorro 0 y coste 0 en todos los ciclos.
  - **La objeción de "memoria latente" queda respondida:** no hay nada a la venta.
- **BUG-01 también aparece sin código compartido:** siete inversiones seriadas con A∩B=0 dan `W=0` y canales
  9/9 (derivado antes y medido 20/20).
- **Corrección de 2K-bis:** el rango dinámico explica el colapso a W=0 y la capacidad útil (M_max 4 → 8), no el
  techo N* a 20k (igual en 19/20).
- **Fase 4, 3T confirmatorio sobre v8: SÍ** (`experimentos/3T_confirmatorio/`, datos
  `3T_confirmatorio_20260916_150727`).
  - Con v8, la regla 2L separa sola el canal temporal: `sep` 3.97 y `lift_q4` 0.34 en 20/20. El control de ruido
    no lo logra.
  - **Predicción exacta:** v8 reproduce PH3 del día 3 semilla a semilla (C3 20/20). El único bloqueo de 3T era
    BUG-01.
  - **REPLICADO en semillas nuevas 21–40** (`datos/3T_replica_s21-40_20260916_151902`), con el comparador
    corregido **antes** de verlas: E 20/20 y 14/14, `sep` 3.99, `lift` 0.35.
  - **ERR-13 (el comparador distinguía `0.0` de `-0.0`) queda CERRADO:** el SÍ ya no depende de esa corrección.
  - Alcance: memoria de una mordida.
- **Etapas del brief (punto 16):** 1 cerrada; 2 cerrada en valor (falta 2P, conducta bajo hambre);
  **3 generalización A MEDIAS** (falta la versión dura, preregistrada para v6: hay que revisarla para v8 antes de
  correr); 4 memoria persistente, parcial.
- **Siguiente (sin fijar):** 2P, política bajo hambre; A5 corregida; Etapa 3 versión dura; 3F, fusión. Lo decide
  dirección.
- **Primitivo nuevo:** "mordida del techo" = **truncación** del clip, no el valor del canal. Tocar 3.0 no es morder.

## Estado (día 3 — repo en Claude Code, 15 sep 2026)
- **Traspaso VALIDADO**: batería 20/20, baseline reproducido bit a bit (259/260 celdas; la única diferencia es
  redondeo del CSV viejo). Repo git con tag `v6-baseline`. `.gitattributes` con `* -text`: sin eso, git convierte
  LF→CRLF y **rompe los 55 hashes sha256 en cualquier clon**.
- Etapa 1 (aprende A/B): cerrada, 20/20 en v6.
- Etapa 2 (inversión, extinción, estímulo nuevo, valencias opuestas): cerrada en valor. Ver registro.
- Problema abierto de conducta: política bajo hambre (mordidas de veneno 1–4% por visita en inanición). Fase 2P.
- **v7 NO congelado**, tras dos exámenes con criterio preregistrado. Los criterios científicos pasan 20/20 en
  las seis etapas y el control negativo es válido (0/20); lo que falla es el criterio de disparo en E2I.
  v6 sigue siendo el tronco.
- **Ley de disparo de 2L, definitiva: `err_max > 0.6`.** Concordancia 320/320 sin excepción, frontera de
  cuchillo (0.5996 no divide, 0.6003 sí), y derivación cerrada: `err_max = 0.147509·|R|`, así que cruzar θ
  exige `|R|` efectivo > 4.068 — imposible sin recompensas de signo opuesto sobre la misma celda.
  **Con solapamiento 0 la regla no puede disparar.** Las dos leyes previas del día 3 ("umbral en 2 celdas" y
  "valencia opuesta") están REFUTADAS como enunciados generales: con A∩B=1 co-aprendido desde t=0 dividen
  8/20, y con solapamiento 2 de misma valencia dividen 0/20. El recuento de celdas era un proxy.
- **BUG-01, bloqueo real del tronco y lo más importante pendiente**: bajo refuerzo contradictorio sobre un
  código compartido, `Wp` y `Wn` corren los DOS al techo (9.0/código) y su diferencia se anula exactamente;
  a partir de ahí no se aprende nada en esas celdas. Reproducible sin tocar nada:
  `organismo_v7.run(1, plast=False, solap_AB=3)` → `comp A=(9.0, 9.0)`, `W=0.0`.
  Es el "v6 colapsa: W=0" de 2L, el "ambos canales saturan" de 2F y los "canales inflados" de 2J/2K.
- **La regla de división no selecciona por dirección, selecciona por parada** (rama 3T): `P − mu[c]` es
  distintividad no supervisada y el control de ruido separa MÁS que la señal. Lo que selecciona es el error
  que dispara y apaga la división.
- Rama 3T (composición temporal, nivel 7): **NO** con las constantes actuales. Post-hoc, levantando sólo el
  techo de BUG-01, sí emerge 20/20 — no cuenta hasta repetirlo con criterio escrito antes.
- Rama 3K (¿debe aprender el Kenyon?): **NO, basta el azar** para características lineales. Aprender KW mejora
  la representación y no mejora la generalización: descorrelacionar códigos ≠ representar la característica.
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
- **BUG-01 exp. 2 (decaimiento de la parte común, `organismo_v7e.py`): mecanismo CONFIRMADO, criterios míos
  refutados.** Techo despejado 20/20 con λ_c ≥ 0.0125 (frontera derivada a priori: 0.01125), `Wp`/`Wn` en
  1.77/3.04 contra 1.8/2.8 predichos, `W_A=+1.000` y `W_B=−3.000` **exactos** (P3), ley de disparo intacta
  (P4), seis etapas 20/20. **`W` sale idéntico a tres decimales para λ_c en un rango de 24×: el arreglo no
  cuesta nada en valor neto.** P1 cae sólo por la dispersión de `W` (supuse mezcla 50/50; la fija la política).
  **v7e NO se congela. v6 sigue siendo el tronco.**
- **λ_c es un INTERRUPTOR, no una perilla** (decisión de dirección, 15 sep). Por encima de la frontera
  derivada (0.01125) el resultado no depende de su valor: `W` sale idéntico a tres decimales en todo el
  rango probado. **No se vuelve a barrer.** Lo único que elige λ_c es dónde queda el equilibrio de `Wp`/`Wn`,
  y eso sólo importa para el miedo latente — que lo mide la prueba de ahorro, no un barrido.
- **Prueba de AHORRO preregistrada y SIN correr** (`experimentos/bug01/PREREGISTRO_ahorro.md`): mide si el
  arreglo vende el miedo latente que compró 2F. Exigida por dirección antes de congelar nada. Criterio: si el
  ahorro cae bajo el 50% del de v6, no se congela por defecto. Ojo: `Wp`/`Wn` sólo cambian dentro de
  `if mordio:`, así que **con `A∩B=0` la recuperación espontánea es imposible por construcción**.
- **Diez errores de instrumento documentados** (ERR-09: la comprobación de inercia comparaba dicts que
  incluían la clave `lam`, era `False` por construcción; ERR-10: "sin conflicto" definido como solapamiento
  espacial final, ignora el conflicto temporal de E2 y el 3→0 de E2L). Diez de diez anomalías del proyecto
  han sido del instrumento. Cuando algo se vea raro: primero el instrumento, siempre.
- **El patrón que más caro sale, tres veces ya** (ERR-06, ERR-08, ERR-10): escribir un criterio que no dice lo
  que quiero decir, y descubrirlo sólo al correrlo. Antes de correr, releer el criterio preguntando qué
  escenario lo haría pasar por la razón equivocada.

## Comandos
```
# IMPORTANTE en Windows: la consola es cp1252 y revienta al imprimir ≈ → ∩ (UnicodeEncodeError).
PYTHONIOENCODING=utf-8 python bateria.py 6     # (desde organismo/) regresión rápida
PYTHONIOENCODING=utf-8 python bateria.py 20    # regresión completa de v6 (referencia)
python bateria_v8.py 6                         # (desde organismo/) regresión rápida del TRONCO v8, ~2 min
python bateria_v8.py 20 --log                  # examen completo de v8, log y json en datos/
python organismo/bateria_v7.py 20              # examen de congelación de v7 (ya trae reconfigure utf-8)

python experimentos/run_etapa.py --etapa E1 --semillas 20        # paralelo, ~13 s
python experimentos/run_etapa.py --etapa E1 --semillas 20 --verificar-equivalencia
python experimentos/analiza.py --etapa E1 --baseline

python -c "import organismo_v6 as o; print(o.run(1))"   # una corrida (~4 s)
```
