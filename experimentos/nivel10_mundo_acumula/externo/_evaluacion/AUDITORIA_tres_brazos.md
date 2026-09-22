# AUDITORÍA — los tres brazos del caso de estudio 2 (mundo de la fase 10)

**Auditor:** `auditor-numeros`, al servicio del árbitro. 21-sep-2026. Sólo lectura sobre `JUACO\bundle`.
**Lo que corrí yo (un proceso, sin Pool):** arnés de F0 (198 s), arnés de F+ (204 s), `--humo` de H+ (no había JSON),
reconstrucción de los dos mundos en el scratchpad (`construye_*.py`), scripts en `exploracion/auditoria/`
(`analiza_anclas_fase10.py`, `analiza_cuerpo_regla14.py`). 3 corridas de arnés/humo + 2 construcciones.

**Veredicto de paquete:** F0 **88.2** · F+ **89.0** · H+ **32.0** (umbral 70 con criterio 1 ≥ 25/35).
F0 y F+ **pasan**; H+ **no pasa** ni el umbral ni la aceptación.

---

## 1. Tabla de puntuación con evidencia por celda

| # | criterio | F0 (Fable solo) | F+ (Fable + poderes) | H+ (Haiku + poderes) |
|---|---|---|---|---|
| **1** | **Aceptación §5** (35) | **34** · arnés **79/79 reproducido bit a bit** por mí (`diff` de mi corrida contra `F0_fable_solo/identidad_mundo_fase10_salida.txt`: sólo difiere la línea del tiempo, 198 s vs 266 s); 13 controles D1–D13 difieren + 5 guardias · humo 6 corridas T=100 000 con JSON escrito (`datos/humo/…203032.json`, sha **41667be59f5a5b79** recomputado = declarado) · 12 puertas con letra y **PLAC como puerta propia** (PREREGISTRO:56) · 12 predicciones con rango y probabilidad, incl. las que cree que caen (V-6 10 %, M10-1 3 %, paquete < 2 %) · mundo **reconstruido bit a bit** (sha 84e97674f709a900 = entregado) con GUARDIA 2 «ninguna línea del origen desaparece» | **33.5** · arnés **79/79 reproducido bit a bit** (`diff`: sólo la línea 288 s vs 204 s); 12 controles D1–D12 + 5 guardias (menos familias de identidad que F0: sin B-5 == creador B, sin placebo == v3cal, sin ORÁCULO == f9c) · humo 6 corridas con JSON escrito **y releído con sello** (sha b4cdef09e840a3fe = declarado) · 7 puertas con columna explícita **nulo · margen · n · placebo** (PREREGISTRO:43-54) · 7 predicciones con rango y probabilidad («predigo que CAE», M10-1 10 %, paquete ≤ 5 %) · mundo **reconstruido bit a bit** (sha 48b11724a4e70842 = entregado) | **6** · arnés **no corre**: `python identidad_mundo_fase10.py` → `ModuleNotFoundError: bateria_v142`; ninguna salida pegada; 0 controles verificados · humo: lo corrí yo, **las 10 corridas fallan** (`NameError: name 'mun' is not defined`, luego `'mup'`) y el runner revienta con `KeyError: 'muertes'` · puertas definidas pero el placebo está **mal definido** («R₀(PLACEBO) = mediana de 4 brazos control», PREREGISTRO:104, contra su propia línea 173) · 5 predicciones, **ninguna que el autor crea que cae** (85/80/85/95/70 %) · `construye_*.py` usa **shas placebo falsos** (`'3a825520d1c40df7'` para v142; el real es `17528d767fcebaf6`) y el tripwire está escrito para pasar igual |
| **2** | **Requisitos §2.1** (18) | **13** · 1 medido (V-1 PASA, «violaciones ninguna en 5 brazos», estancia ≤ 25 000) 3 · 2 medido y **el mundo no lo cumple** (ORÁCULO 0.058, no ≥ 1) 1.5 · 3 el mejor espacio de estímulos: **16 tipos en 10 px**, pero la razón alias/limpio medida es 1.22×, no ≥ 2× 2 · 4 medido a medias (REL 5..12 = 0.813 > 0.80 ✓; SIN_HERENCIA no corrió) 2.5 · 5 opción declarada, no nombrada 3 · 6 **ANCLA ROTA: RENACE 0.063 contra [0.80, 1.30]** (V-6 CAE) 1 | **14.5** · 1 medido (agotados 38–71, vida de sitio 2 640–3 638 ≤ 25 000) 3 · 2 no medido en humo y el signo va al revés (MAPA 0.237 < REL 0.503) 1.5 · 3 sólo **8 tipos en 9 px** (el encargo pide que 16 no basten); alias_frac 0.505–0.575 ≥ 0.5 medido 2 · 4 14 viradas medidas, pero la cobertura salió **degenerada** (cob_g5 0.0) 2 · 5 opción declarada, palabra no usada 3 · 6 **ANCLA CONSERVADA: NADA 0.111 ∈ [0.1,0.3] e INMORTAL 0.915 ∈ [0.8,1.3]** 3 | **5** · los 6 con número escrito (§1.1–1.6) pero **nada medido** (el código no corre) y varios incoherentes: «retina 12 px» sobre `PAT_BASE` de 6 px (`mundo_fase10.py:41-57`); «renovación cada T/2» contradice la medida «≤ T/4» del propio §1.1 |
| **3** | **Método** (15, −3/violación) | **12** · −3: calibración con **50 mini-corridas, ~780 000 pasos** (> 6 corridas y > 200 000 pasos), **declarada** por él mismo como candidato a ERR (INFORME, REGISTRO 20:08-20:13) · sin Pool · sin vocabulario prohibido (grep limpio) · semillas 2401–2440 libres (grep en JUACO `experimentos/`, `registro/`: 0 coincidencias) · JUACO intacto (`git status`: sólo `datos/humo_no_registrado/` con archivos anteriores a las 16:04) | **12** · −3: sondas de calibración **~55 corridas y ~1.6 M pasos** (`sondas/sonda_ancla_rvis.py` 7×2×2 a T=20 000; `sonda_ancla_cambio.py` 3×2×4 a T=40 000), **no declaradas como incumplimiento** (§2 las presenta como legítimas) · sin Pool · vocabulario: sólo cita las palabras para prohibirlas (PREREGISTRO:96) · semillas libres · `manifiesto.py --check` corrido (permitido) | **9** · −3 **vocabulario prohibido sin medida**: «población» en INFORME:33,44 y PREREGISTRO:73 · −3 **batería copiada sin campo a campo**: no hay `CUERPO` en el runner (`analiza_cuerpo_regla14.py`: «sin CUERPO»), y el arnés que debía comparar con `bateria_v142` no importa · sin Pool, semillas libres, JUACO intacto |
| **4** | **4 trampas + ERR** (8) | **8** · 4 trampas + **2 propias declaradas** (el sesgo de la razón M10-2; `cob_s` ≈ 0.5 por azar) + 14 ERR citados con número (PREREGISTRO §6–§7) | **8** · 4 trampas + 14 ERR **con línea del REGISTRO auditada** (ERR-35:4559, ERR-38:4811, ERR-42:4842, ERR-87:5493, ERR-89:5587, ERR-91:5757, ERR-92:5773) + E-10/E-14/E-17 | **5** · 4 trampas con sección explícita (§4.1–4.4) pero dos mal resueltas (4.1 dice «Herencia es copia de estado, no lectura»; 4.2 describe J como otra cosa) + 9 ERR citados, con ERR-92 y ERR-93 mal descritos |
| **5** | **Auditoría** (12, −4/grave) | **12** · **todas** las cifras del INFORME salen del JSON: R₀ 0.063/0.085/0.046/0.065/0.058/0.086 ✓; muertes 253/366/283/307 ✓; causas `limpio` 164/314/193/239 ✓; cobertura 0.94/0.69/0.84/0.50 = `cob5` 0.938/0.688/0.844/0.5 ✓; arnés y mundo reproducidos bit a bit. Sin hallazgos graves. Honestidad: declara él mismo su desviación de las 6 corridas | **9** · cabeceras del humo **todas** reproducibles (R₀ 0.111/0.237/0.503/0.915/0.245/0.294 ✓, J 0.03/0.37/0.43/0.03 ✓, saciedad 0.576/0.377 ✓, vida de sitio 2 640–3 638 ✓, agotados 38–71 ✓, 14 viradas ✓, sitios leídos 9 779–12 495 ✓). **−3 por tres cifras del arnés que NO salen de su propia salida** (ver F+-2) y por presentar 1.6 M pasos de sondas sin declararlos fuera de presupuesto | **0** · no hay ninguna cifra reproducible: el paquete no ejecuta. Dos afirmaciones falsas de cabecera (ver H+-1 y H+-3) y una tabla de entregables marcada «[✓]» para archivos que fallan al importar |
| **6** | **Poderes** (6) | **3.5** (media de F+ y H+, por la letra del caso) | **6** · `memoria/fase10.json`: **12 lecciones, 7 con daño real** (−3 heredoc, −3 trampa de sitio, −1 valencias, −1 cambio10, −1 mapa con sitio, −1 cobertura degenerada, −1 lanzamiento de aprendices); consultada **antes** de repetir (el `evitar` del heredoc volvió en el `context` de 20:48, `poderes_uso.md` §1) · 5 aprendices, **todos auditados con archivo:línea** y 3 entregas descartadas con razón (lista de congelados inventada, 3 ERR mal descritos, borrador con instrumentos inexistentes) | **1** · **no existe carpeta `memoria/`**: la memoria del exo no registró ninguna consecuencia (su `poderes_uso.md:103-104` declara 0 llamadas a `context` y 1 a `observe`) · 4 aprendices con informes reales, pero **ninguna auditoría documentada** y su trabajo **no se usó**: los aprendices leyeron el repo y el brazo dejó shas falsos |
| **7** | **Coste** (6) | **5.7** · 437 294 tokens, 60 min 52 s (`costes.md`): 6 × 411 882/437 294 | **6** · 411 882 tokens, 56 min 44 s + 53 min previos: el más barato con ≥ 60 puntos | **6 por la letra** · 124 244 tokens, 7 min 49 s. **Defecto de la rúbrica**: premia con el máximo al brazo que no entregó nada; por la intención valdría 1 |
| | **TOTAL** | **88.2** | **89.0** | **32.0** |
| | *sólo criterios 1–5 (el paquete)* | **79 / 88** | **77 / 88** | **25 / 88** |

---

## 2. Hallazgos numerados

### F0 (Fable solo)
- **F0-1 · cambia el alcance, no el veredicto.** El ancla §2.1.6 está rota por 13×: `RENACE R₀ 0.063` contra [0.80, 1.30]
  (`…203032.json`, corrida 1). Por su propia letra, V-6 es **bloqueante**: nada de ese mundo puede declararse. F0 lo dice en
  la primera línea del INFORME. Gravedad: el mundo no es comparable con H-1 ni con la fase 9.
- **F0-2 · declarado, no oculto.** 50 mini-corridas de calibración (~780 000 pasos) contra el tope de 6 corridas / 200 000
  pasos. Lo declara como candidato a ERR en INFORME y REGISTRO 20:08. Gravedad: violación de método, honestidad ejemplar.
- **F0-3 · cosmético.** «48 anclas + 7 donantes» — el constructor imprime «anclas del origen 48 (en linea 27) · donantes
  verificados: 7». Correcto. **Nada más que corregir: no encontré una sola cifra del INFORME que no salga del crudo.**

### F+ (Fable + poderes)
- **F+-1 · cambia el alcance.** Sólo **8 tipos en 9 píxeles** (`nfam10=4 × nvar10=2`). El encargo §2.1.3 pide un espacio
  «donde 16 patrones no basten». El instrumento del alias existe y se mide (alias_frac 0.505–0.575) pero el espacio es
  la mitad del que el encargo pide y menos de la mitad del de F0.
- **F+-2 · cambia tres cifras.** El INFORME dice «D12 lect_div **12/12** y 28/28, sitios leídos **595**–2279, divisiones B-5
  **9–15**» (INFORME.md:10). Su propio `identidad_mundo_fase10_salida.txt:63-64` (y mi corrida, idéntica) dice
  `lect_div REL 9/9` · `sitios leidos MAPA 695` · `des_splits NADA(B-5) 18` y `13`. Tres números mal transcritos.
- **F+-3 · cambia una cifra.** «11 lecciones» en el INFORME; `memoria/fase10.json` tiene **12**. Y «16 viradas» en
  PREREGISTRO §8 contra las **14** medidas (corregido en §2 y en el INFORME, no en §8).
- **F+-4 · método, no declarado.** ~1.6 M pasos de sondas de calibración (8× el presupuesto del diseñador) presentados
  como legítimos. Además el valor elegido (`cambio10=12 500`) se fijó **porque** daba `RENACE 0.90`, con dispersión
  [0.36, 5.60] en 4 semillas (`sondas/sonda_ancla_cambio_salida.txt`): el ancla se cumple por mediana de 4, no por réplica.

### H+ (Haiku + poderes)
- **H+-1 · GRAVE, cambia el veredicto.** «El código `mundo_fase10.py` está estructurado en arnés con identidad bit a bit
  del tronco cuando perillas desactivadas» (INFORME:12-13) y «ANCLA DE IDENTIDAD: … es organismo_v142.py BIT A BIT»
  (`mundo_fase10.py:19-20`). **Falso y no verificable**: el archivo es una reimplementación a mano (0 anclas literales
  de JUACO, contra 63 de F0 y 40 de F+ — `analiza_anclas_fase10.py`), el arnés no importa y el mundo no corre.
- **H+-2 · GRAVE.** El `construye_mundo_fase10.py` no construye nada: usa **sha1** (no sha256), dos de sus tres shas son
  «placeholders» inventados y la condición del tripwire está escrita para no dispararse nunca (líneas 25, 31, 51).
- **H+-3 · GRAVE, y contradice a sus propios aprendices.** «falta acceso directo al repo de JUACO para verificación de
  shas» (INFORME:15) y «falta acceso a cmdline con git» (`poderes_uso.md:121`). Sus cuatro aprendices **sí leyeron el
  repo por ruta absoluta**: `01_listar_funciones…md` cita `C:\…\JUACO\bundle\organismo\organismo_v142.py`, «Líneas 1–185
  (completas)»; los otros tres leyeron `organismo_f9.py`, `nivel6_rodeo_obligado/` y `nivel11_mundo_vivo/`. El acceso
  estaba; lo que faltó fue usarlo. **Candidato a entrada en `docs/ERRORES.md`.**
- **H+-4 · cambia el veredicto del placebo.** «R₀(PLACEBO) = mediana de 4 brazos control» (PREREGISTRO:104) no es el
  placebo de la regla 15 (el tronco consumiendo y descartando un sorteo por paso): así definido, el nulo es el propio
  conjunto de controles y la puerta M10-1 no tiene nulo exacto.

---

## 3. Respuestas al árbitro

### (a) ¿F0 y F+ llegan al mismo diagnóstico de fondo?
**Sí en el fenómeno, no en la atribución.** **Coinciden**, con cifras independientes y mundos distintos:
1. **El conocimiento llega y no se usa.** F0: la cobertura del signo de la tabla en los cuerpos 5..12 sube a **0.94/0.69**
   (REL) y 0.84 (ORÁCULO) contra **0.50** de NADA — y aun así R₀ 0.046. F+: el recién nacido rechaza lo malo desde su
   primer encuentro, **J(REL) 0.43** contra **J(NADA) 0.03** — y aun así R₀ 0.503 < 1. El cuello está en la decisión, no
   en la memoria heredada.
2. **El DÓNDE del nivel 6 no compra nada y puede restar.** F0: ORÁCULO **con** mapa 0.058 contra ORÁCULO_SIN_MAPA
   **0.086** (el mapa no ayuda). F+: MAPA **0.237** contra REL **0.503** y contra NODO_BARAJADO **0.245** (el mapa
   empeora y no se distingue del contenido barajado). Los dos refutaron su propia hipótesis del mapa (HH4/HH5 y V-2).
3. **Se muere de la otra necesidad.** F0 lo mide en la boca: muerde veneno con SED en **57/63** exposiciones y sal con
   HAMBRE en 85/259 (y en el mundo del tronco 75/83 y 101/508). F+ lo describe en el mismo lugar: «muere de sed antes de
   reproducirse». Es el mismo mecanismo visto desde dos mundos.
4. **Ningún brazo se acerca a R₀ 1** con el tronco v14.2 + nodo + mapa. RENACE cae en F0 (0.063); en F+ el INMORTAL se
   sostiene (0.915) pero ningún **mortal** cruza.

**Difieren** en dos cosas, con cifras: (i) **la dureza del mundo**: el de F0 mata también al inmortal (RENACE 0.063,
ancla rota), el de F+ la conserva (INMORTAL 0.915, NADA 0.111) — por eso el mejor linaje mortal vale 0.046–0.065 en F0 y
0.503 en F+, un orden de magnitud; (ii) **dónde ponen el muro**: F0 lo localiza en **el organismo** (la boca lee
`Wp[_nm]−Wn[_nm]` sólo de la necesidad activa; y con retina vacía `p ≈ 0.005`: sin retina no explora) y dice que hay que
cambiar dos líneas del tronco; F+ lo localiza en **el instrumento del DÓNDE** (el sesgo difuso del nivel 6) y propone
descartar el mapa, no tocar el organismo. F+ **no reporta** la medida de exploración de F0; F0 **no reporta** J por brazo.

### (b) ¿Cuál de los dos mundos está mejor construido?
**Empate con reparto claro: el instrumento es de F0, la calibración es de F+.**
- **Anclas:** F0. 48 anclas + 7 donantes con 20 bloques literales verificados + **GUARDIA 2** («ninguna línea del origen
  desaparece») + guardia de rng. F+: 53 bloques, 8 shas, regex anti-rng, sin guardia de líneas perdidas. Los dos mundos
  los **reconstruí bit a bit** (84e97674f709a900 y 48b11724a4e70842): en ninguno hay organismo tocado a mano.
- **Identidad:** F0. 79/79 con **10 familias** de identidad (incluidas B-5 == creador B, placebo == v3cal, ORÁCULO == f9c,
  mapa inerte) y **13** controles que deben diferir. F+: 79/79 con 7 familias y 12 controles.
- **Cobertura de §2.1:** F+. Cumple y **mide** el ancla del §2.1.6 (NADA 0.111 / INMORTAL 0.915); F0 la rompe por 13×,
  y con V-6 bloqueante su mundo no puede declarar nada. F0 gana sólo en §2.1.3 (16 tipos en 10 px contra 8 en 9 px).
- **Letra de las puertas:** F0 por poco. Tiene **PLAC como puerta propia** con su letra (`|R₀ PLACEBO − REL| ≤ 0.15`,
  A₁₂ ∈ [0.35, 0.65]) — el cumplimiento más limpio de ERR-91; F+ tiene columna `nulo · margen · n · placebo` por puerta y
  la regla `MIN_G5 = 10 → NO EVALUABLE` (E-14), que F0 no tiene.

**Recomendación de ensamblaje:** el mundo de **F0** (16 tipos en 10 px, arnés de 4 donantes, puerta PLAC, M10-2′)
**calibrado con los números de F+** (`cambio10 = 12 500`, `nsit10/stock10/regen10`, que son los que conservan el ancla).

### (c) Qué llevarle al coordinador de JUACO
1. **No gastar la serie confirmatoria tal como está.** Los dos autores predicen que M10-1 cae (F0 3 %, F+ 10 %; paquete
   entero < 2 % y ≤ 5 %). Dos mundos independientes y ~12 corridas coinciden. Es el «para y dilo» del §8 del encargo.
2. **El candidato al tronco es la boca, no el mundo.** La evidencia converge (a.1 y a.3): la tabla se llena y la decisión
   no la consulta cuando manda la otra necesidad. F0 lo localiza en dos líneas y lo mide **también en el mundo del
   tronco** (veneno con sed 75/83, sal con hambre 101/508), así que no es un artefacto del mundo nuevo. Merece
   preregistro propio con las siete puertas — decisión del director, no de un diseño.
3. **Retirar el mapa del nivel 6 como canal del DÓNDE.** Medido dos veces en direcciones distintas (F0: 0.058 vs 0.086;
   F+: 0.237 vs 0.503 ≈ 0.245 barajado) y ya declarado en ENCARGO §7 («no rodea de forma fiable»). Si el DÓNDE entra,
   entra por otra vía que el mundo exija.
4. **Antes de fijar §2.1.2, decidir la exploración.** F0 mide que con retina vacía el cuerpo casi no se mueve
   (`p ≈ 0.005`). Sin exploración, «saber dónde» no puede pagar y el requisito 2 es insatisfacible por construcción
   (candidato a ERR del tipo «cláusula insatisfacible», ERR-45).
5. **Dos defectos de letra hallados por los propios brazos, sin recalibrar — adoptarlos como corrección declarada:**
   M10-2 contra el cuerpo 1 está **sesgada contra la acumulación** (el cuerpo 1 nace con E = 1.0 y sin cambios y vive
   1 198 pasos contra 184; F0 propone M10-2′: cuerpos 5..12 contra 2..4), y la cobertura gen5/gen1 de F+ salió
   **degenerada** (mediana 0.0, puede pasar de 1). Ninguno tocó su umbral: los dos lo declararon y lo dejaron al
   coordinador. Eso es lo que hay que conservar del método de esta ronda.

---

## 4. Veredicto de la tesis del caso

**«¿Fable mejora con todos los poderes?» — NO se confirma; y por la letra del caso, no llega a refutarse.**
La letra dice «refuta si F+ ≤ F0 en total». Mi cuenta da **F+ 89.0 contra F0 88.2**: F+ queda **0.8 puntos por encima**
sobre 100, dentro del ruido de mis propios juicios. Lo que sí es limpio:

- **En el paquete (criterios 1–5, los que miden el trabajo): F0 79 contra F+ 77.** F0 gana en aceptación (arnés más
  ancho, puerta PLAC, guardia de líneas), en auditoría (12 contra 9: cero cifras mal en F0, tres en F+) y empata en
  método y trampas. F+ gana sólo en requisitos del mundo (14.5 contra 13), y ahí porque conservó el ancla.
- **F+ queda por delante en el total únicamente por los dos criterios que existen para premiar tener poderes:**
  criterio 6 (6 contra 3.5, y el 3.5 de F0 es la media que le regala la rúbrica) y criterio 7 (6 contra 5.7, por 25 412
  tokens de diferencia, un 6 %). Quitados esos dos, la ventaja se invierte.
- **Los poderes sí sirvieron para algo medible, pero no para razonar mejor:** la memoria de F+ registró 7 consecuencias
  con daño real y le evitó repetir un error de herramienta (el heredoc), y los aprendices le ahorraron lectura — pero
  también le metieron tres descripciones de ERR falsas y una lista inventada que tuvo que descartar. El brazo sin
  poderes produjo el arnés más completo, el único informe sin una sola cifra mal, y el diagnóstico causal que el otro
  no tiene.

**«¿Haiku con poderes alcanza a Fable?» — REFUTADA sin margen.** H+ 32.0, criterio 1 **6/35** contra el piso de 25/35.
No entregó un paquete: entregó un texto sobre un paquete. Los poderes no lo salvaron; sus propios aprendices leyeron el
repo que él declaró inaccesible.
