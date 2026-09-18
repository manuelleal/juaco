# Auditoría — bloques del día 7 (XOR 3d/3e, escala del mapa, allostasis, rodeo, réplicas con gemelos) — 17 sep 2026

Leídos `registro/EQUIPO.md` y el bloque "Estado (día 5)" de `CLAUDE.md` antes de auditar. No edité ni corrí nada;
todo lo de abajo se verificó leyendo preregistro + instrumento + runner + JSON/log de `datos/`, no sólo la prosa del
registro. Ningún hallazgo es bloqueante: los cinco bloques tienen identidad (perillas apagadas) 100 % en sus JSON,
construcción por anclas con conteo exacto y `SystemExit` si falla (`construye_xor_3d.py:19-26`,
`construye_allostasis.py:22-31`, `construye_rodeo.py` análogo), acierto balanceado con empate = 0.5 donde aplica
(`corre_xor_3d.py:54-60`), y ningún `humo()` de los cinco abre `Pool` (regla 3). Los gemelos numba reusados en las
réplicas (`mundo_mapa_rapido.py`, `mundo_temporal_k_rapido.py`) no tienen recursión con `cache=True` y usan
`_psum`/`_psum_bloque` por pares (regla 9 de `EQUIPO.md`). Las cuatro trampas están revisadas por escrito en los
cinco preregistros y las defensas están implementadas de verdad, no sólo declaradas: SINMAPA de rodeo nunca lee
`pos` (`mundo_mapa_rodeo.py`, política alimentada sólo por retina), la sonda de XOR se calcula antes de
`tipos.extend(test)` (`organismo_v13q3.py:125-131`), el control barajado de escala del mapa usa RNG propio
`seed+950000` sin tocar el orden de inyección (`PREREGISTRO_escala_mapa.md:150-151`).

## Hallazgos

1. **[IMPORTANTE] Bloque 2 ter — el registro diagnostica mal su propio fallo de la puerta K0: no es "0.700 == 0.7 con
   redondeo", es una constante‑ancla truncada.** `experimentos/nivel8_escala_mapa/corre_escala.py:30` fija
   `K0 = {'V13_adq': 0.887, 'MAPA_adq': 0.700, 'MAPA_comida_q4': 971.0}` y `:191` compara con
   `abs(k0[k]-K0[k]) < 1e-9`. El JSON real (`datos/escala_s81-100_20260917_230039.json` →
   `meta.veredictos.K0_medido`) da `V13_adq = 0.8875` contra el ancla `0.887` (diferencia real `5e-4`, no ruido de
   punto flotante); `MAPA_adq` (`0.7` vs `0.7`) y `MAPA_comida_q4` (`971.0` vs `971.0`) sí coinciden exactamente. El
   número `0.887` fue copiado de la impresión a tres decimales del log anterior
   (`datos/novedad_alta_s81-100_20260917_221523.log:14`, que muestra "0.887" porque usa formato `.3f`) en vez del
   valor JSON de precisión completa; comprobado: `f"{0.8875:.3f}"` da `"0.887"` en Python. La comparación en sí
   (`abs(...)<1e-9`) está bien escrita — el defecto es el origen del ancla. `registro/REGISTRO_etapas_1_2.md:3561-3563`
   atribuye la alarma al campo equivocado (MAPA/0.7) y la cierra como "defecto menor del runner"; la conclusión de
   fondo (no hay sospecha real, P1–P4 no usan `V13_adq`) es correcta, pero por el motivo equivocado. **Cambio
   propuesto:** corregir esas líneas del registro (el campo que falló fue `V13_adq` por precisión del ancla, no
   `MAPA_adq`); capturar anclas `K0` siempre desde el JSON de precisión completa, nunca desde una línea de log
   formateada; si la intención real es "igual a tres decimales", comparar `round(x,3)==round(y,3)` en vez de un
   épsilon de `1e-9` contra una constante truncada a mano.

2. **[IMPORTANTE] Nivel 6 rodeo — la Enmienda 1 (análisis del subconjunto válido) nunca se implementó antes de
   correr 61–80: la serie ya corrió sin ella y quedó sin veredicto útil.** `PREREGISTRO_rodeo.md:135-143` (Enmienda 1,
   fechada "23:30") promete, para la serie nueva, un análisis sobre el subconjunto con V0∧V1 válidos (≥12 semillas,
   mediana R1≥0.70 y pareado ≥75 % del subconjunto). Cronología de archivos: `corre_rodeo.py` sin modificar desde
   `23:23:15`; `PREREGISTRO_rodeo.md` guardado `23:26:48`; `datos/rodeo_s61-80_20260917_232711.log` corre de
   `23:27:11` a `23:29:37` — la serie se lanzó con el runner viejo. Confirmado en código: `corre_rodeo.py:178-197` no
   tiene ninguna lógica de "subconjunto"/"válidas"/"75 %" (grep vacío); es exactamente `V0 = v0n >= 18` del
   preregistro original, sin la enmienda. El JSON (`datos/rodeo_s61-80_20260917_232711.json` →
   `meta.veredictos`: `V0: false, V0_n: 16`) reproduce el mismo patrón de invalidez que 41–60 (`V0_n: 15`) y termina
   otra vez en "*** OJO: validez caída, no se interpreta" (`rodeo_s61-80_20260917_232711.log`, última línea), sin que
   se haya calculado el análisis que se preregistró justamente para rescatar esa situación. El JSON ya trae `v_A`,
   `v_B`, `R1`, `R2` por semilla para 41–60 y 61–80, así que el análisis no exige nueva simulación. Sobre la pregunta
   del encargo — ¿es legítima la Enmienda 1 o es recalibración encubierta? — **es legítima tal como está escrita**:
   usa los mismos umbrales del criterio original (mediana ≥0.70, pareado ≥75 %), el umbral de V0 salió de la
   geometría (potencias de 0.9) antes de cualquier dato (`PREREGISTRO_rodeo.md:39,85-92`), no toca el veredicto de
   41–60 ("nada se recalibra sobre 41–60") y promete reportar siempre el conjunto completo junto al subconjunto. El
   único matiz real es que condicionar en V0 se decidió después de ver que V0 fue la puerta que falló (ver hallazgo 4).
   **Cambio propuesto:** calcular el análisis del subconjunto sobre los JSON ya existentes de 41–60 y 61–80 antes de
   que el cronista escriba la entrada de 61–80; que el registro no diga "se aplicó la enmienda" si no se calculó.

3. **[MENOR] ERR-24 (control SINCOMIDA de bajo n efectivo) debilita en retrospectiva también las dos series
   anteriores del mapa, no sólo `mapa_s41-60`.** El diagnóstico del equipo (`REGISTRO_etapas_1_2.md:3489-3496`) es
   correcto — confirmado leyendo `spawn()`/`_pend`/`ciego_al_llegar` en `mundo_mapa.py`: el control cuenta sólo
   ~12 decisiones reales de 40 posibles por semilla. Pero `corre_mapa.py:128` (`C3 = 0.40 <= mediana <= 0.60`) ya
   venía evaluando ese mismo control de bajo n efectivo en series previas (0.534 y 0.500, citadas en
   `REGISTRO_etapas_1_2.md:3489`) sin que se hubiera notado entonces: esos "pasa" eran de poca potencia, no
   confirmaciones fuertes, y ahora que una tercera serie cae a 0.621 se ve que el control podía haber fallado antes
   por el mismo motivo, por puro ruido de muestreo. No cambia el hallazgo central del mapa (que no depende de C3).
   **Cambio propuesto:** al corregir el control (más pasos mínimos, o sustituir por SINMAPA como ya recomienda el
   registro), anotar que las dos "confirmaciones" previas de C3 no cuentan como replicación independiente de ese
   control específico.

4. **[MENOR] Patrón repetido: las "enmiendas" de subconjunto (mapa 2 bis, ahora rodeo) se deciden caso por caso
   después de ver qué puerta de validez falló.** Cada una es defendible por separado (mismos umbrales, no
   recalibra los datos ya vistos), pero repetirlo ad hoc dos veces sugiere fijar una regla estándar en
   `EQUIPO.md`: si una puerta de validez falla por debajo de su umbral pero por encima de, p. ej., el 60 % de las
   semillas, la analítica de subconjunto con los mismos umbrales del criterio original es automática y se reporta
   siempre junto al conjunto completo — así deja de parecer una decisión de diseño nueva cada vez.

## Verificado sin hallazgos

**XOR 3d/3e** (`experimentos/nivel7_xor_lectura/`): `organismo_v13q3.py:58-59` bloquea con `ValueError` cualquier
`regla_lenta`/`lectura` mal escrita (no cae en silencio al brazo original); índices del producto correctos por
lectura (`corre_xor_3e.py:36`, `IDX_PROD`); Z1–Z4 y O1 en `corre_xor_3d.py:218-226` y `corre_xor_3e.py:257` calculan
exactamente lo preregistrado — comparé contra los JSON y coinciden dígito a dígito (`Z1_pareado: 5`, `O1_pareado: 13`,
estratos de muestreo 17/3). Inercia de 3e contra 3d verificada en el propio JSON (`INERCIA_3D.inerte: true`).
**Allostasis** (`experimentos/nivel9_allostasis/`): I1/I2/I3 100 %; la guarda G‑b (`corre_allostasis.py:284-287`)
aplicó su tabla de decisión preregistrada en un límite muy cerrado (`razón = 0.9459...` contra el corte `0.95`) sin
ajuste alguno — cae del lado "inconcluso" tal como estaba escrito antes de correr. No se declaró nada más allá de lo
medido, consistente con ser rama exploratoria.

## Vocabulario e identidad — sin hallazgos nuevos

Las entradas del día 7 en `REGISTRO_etapas_1_2.md` (líneas 3470–3654) usan vocabulario ceñido a lo medido en los
cinco bloques ("elige... no planifica", l. 3653; "predice/se sorprende" definidos operacionalmente en el
preregistro de allostasis, no como logro cognitivo, l. 3629; "XOR es representable y legible pero no aprendible",
l. 3604) — no encontré declaraciones infladas. Ninguna de las cinco identidades (perillas apagadas ≡ instrumento de
origen) falló ni se relajó; ninguna "refutación" del día resultó ser, en la lectura de código, un fallo de
instrumento disfrazado de fallo de hipótesis — salvo el matiz de K0 (hallazgo 1), que es al revés: un fallo de
instrumento real que el registro descarta con el diagnóstico equivocado.

## Verificación adicional (00:30): puerta y BUG-01

Encargo del coordinador sobre `PUENTE_creacion.md` §"Creador C". Sólo lectura, sin correr ni editar.

**(a) Qué es BUG-01 y cómo cerró.** `REGISTRO_etapas_1_2.md:469-483,818`: bajo refuerzo contradictorio sobre una
celda compartida, `Wp` y `Wn` suben juntos hasta el tope **por celda** (3.0; "9.0" es la suma sobre las 3 celdas del
código, no 9.0/celda — `REGISTRO_etapas_1_2.md:470`) y `Wp-Wn` se anula exacto, congelando esa celda. Se cerró con
drenaje de la parte común (`lam`: decae `min(Wp,Wn)` tras cada mordida); "el mecanismo está confirmado (techo
despejado...)" (l.818). El drenaje sigue vivo en el tronco: `organismo_v13.py:88`.

**(b) ¿Cierto que desvía la puerta?** **Sí, confirmado en código.** `organismo_v13.py:34` (`puerta=3`) cuenta, de
las 3 celdas del código, cuántas tienen `|Wp-Wn|>0.2` (el mismo umbral que v11 usa para "consolidado", l.9). Una
celda en `Wp=Wn` (tope o no) da `|Wp-Wn|=0` → no cuenta; si las 3 están así, familiar=0<3 → la boca lee la vía
lenta. Real, y no encontré que el preregistro de v13 lo discutiera como riesgo.

**(c) ¿Afecta alguna declaración?** Para Etapa 3/examen v3' (mundo AB, `organismo_v13.py` puro): sin consecuencia
medida — ver (d). Para el mundo de regla (XOR/`bateria_generaliza`, `organismo_v13g.py`/`v13q.py`, mismo campo
heredado en `organismo_v13g.py:68,131,169`): se calcula pero **ningún runner lo imprime ni lo guarda**
(`corre_xor_3d.py`, `organismo/bateria_generaliza.py`: cero referencias a `n_techo`) — la cifra que cita C ahí no es
verificable en ningún artefacto existente; plausible, no confirmada por mí.

**(d) Número medible.** `datos/examen_v13_20260917_165859.log` (criterio v3', semillas 101-120, la batería de
congelación oficial): **`techo=0/20` en las 6 líneas/escenarios** — 0 celdas tocan el tope en 120 corridas del
mundo AB (`bateria_v13.py:103` lo calcula e imprime). `datos/v13_dos_vias_20260917_160541.json` (la corrida que
decidió v13) **no guarda `n_techo`** pese a que `run()` lo devuelve: se descarta al serializar. La cifra de C para
el mundo de regla queda sin verificar por falta de dato guardado, no refutada.
