# v13E — ¿"la sorpresa del mundo en la boca" (dE-TEST) puede ser un órgano del TRONCO? Prueba de NO REGRESIÓN (retención y generalización)

**Escrito ANTES de correr, 18 sep 2026.** Es el paso que falta tras `PREREGISTRO_probar_si_mismo.md` (Enmienda 1
y Enmienda 2, `registro/REGISTRO_etapas_1_2.md` "Bloque C-P1"; `registro/PROPUESTA_v14.md`, segundo candidato):
dE-TEST —el error de predicción de ΔE (bloque 6, copiado) entrando en la BOCA con ganancia `k_testE`— ya midió,
en el mundo largo (`corre_probar_si_mismo.py`, T=200 000, `invertir_en`=T/2), **tres series** (41–60, 61–80,
81–100): recuperación **0.143× / 0.144× / 0.141×** de V13 (pareado **20/20 × 3**), se apaga sola (P4' **20/20 ×
3**, ERR-27) y no envenena (P7' OK × 3). La serie 3 (81–100, `probar_si_mismo_s81-100_20260918_012715`) ya corrió
además sus **baterías**: retención M5 (las SEIS etapas de `bateria_v13`, su `CRIT` importado) **20, 19, 20, 20,
20, 20** de 20, y generalización M6 **G1 px0 0.90 / G2 0.85** — con eso quedó registrado como *"candidato a
órgano con tres series"* (`registro/REGISTRO_etapas_1_2.md`, entrada "Bloque C-P1, serie 3"). Pero M5/M6 son
**más laxas** que el examen del tronco: M5 sólo evalúa el `CRIT` por etapa (`corre_probar_si_mismo.py`, tarea tipo
`'B'`, que llama a `organismo_v13p` con los kwargs del brazo) y **nunca corre la identidad 5, el control 3'/3''
ni 4a'–4d**, porque nunca ejecuta `bateria_v13.py` como programa: sólo importa su diccionario `CRIT`. **Ninguna
corrida hasta hoy pasó dE-TEST por el examen v3' COMPLETO de `organismo/bateria_v13.py`** (los OCHO veredictos)
fijado ON en una copia del tronco, como si fuera a congelarse — exactamente lo que `PROPUESTA_v14.md` marca como
pendiente ("Falta para v14: el examen v3' completo... sobre una copia del tronco con la perilla fija, como
v13D"). Eso es lo que prueba este bloque, con el mismo patrón por anclas que
`nivel7_hija_dispersa/PREREGISTRO_v13D.md`.

## 1. Qué se prueba, y qué NO

Esto es una prueba de **NO REGRESIÓN**, no una demostración: dE-TEST ya se validó como candidato en su propio
diseño experimental (bloque C-P1, semillas 41–80, con sus propios controles CONST-a/b y MOMENTO). Aquí se
pregunta si, fijado ON por defecto y examinado con el instrumento **congelado** del tronco
(`organismo/bateria_v13.py`, `organismo/bateria_generaliza.py`), **rompe algo que v13 ya tiene cerrado**.

**A diferencia de la hija dispersa** (`nivel7_hija_dispersa/PREREGISTRO_v13D.md`, cuya máscara se predijo y se
midió *inerte* en el mundo del tronco), **aquí NO se espera inercia**: `Vb += k_testE·s̄_E` es la razón de ser
del bloque, y se predijo y se midió **ACTIVO** en este mismo mundo (AB, 6 píxeles, un objeto) en las tres series
41–60, 61–80 y 81–100 —si no cambiara nada, no habría recuperación 0.14× que declarar—. Esto tiene una
consecuencia directa sobre el **criterio 5** (identidad de instrumentos) de `bateria_v13E`: en su forma
**original** (`eta_s=0, puerta=None` nada más) no reduce el candidato a `organismo_v11`/`organismo_v10`, porque
`k_testE·s̄_E` no pasa por ninguna de esas dos perillas — se comprobó a mano, antes de escribir este preregistro,
que `organismo_v13E` por defecto **sí difiere** de `organismo_v13p` apagado (claves `W`, `mord`, `comp`, `sobre`,
`llegadas`, `sin_objetivo`, `err_max`, `vis` ya difieren a T = 3 000, semilla 1), y el primer `--humo` de este
paquete lo confirmó en la instrumentación real: criterio 5 original, **0/84**. Por eso el criterio 5 está
**ADAPTADO** (§3, ERR-30): con las CUATRO perillas apagadas (`eta_s`, `puerta`, `k_testE`, `eta_pred`) el
candidato **sí** debe reducirse a v11/v10 bit a bit —ya verificado (parte E, §2)—, y es esa identidad, no la
original, la que da derecho a interpretar el resto del examen v3' (las seis etapas, 3'/3'', 4a'–4d) como una
prueba **genuina** de si el candidato, con la perilla puesta, rompe algo que v13 ya tiene cerrado. Ese resto del
examen sigue siendo capaz de fallar: es exactamente el tipo de riesgo que una prueba de no regresión debe poder
mostrar.

## 2. Instrumentos (por anclas; ningún original tocado)

| archivo | origen (sólo lectura) | sha origen | sha generado |
|---|---|---|---|
| `organismo_v13E.py` | `organismo_v13p.py` (generado por `construye_probar.py`; ya pasó su propio arnés J1–J6) | `2dbed7ccac4dd736` | `ab8e3b0579edfc29` |
| `organismo_v13gE.py` | `organismo_v13pg.py` (ídem, mundo de regla) | `910f1f5fb64453bb` | `882f32b4ae88b853` |
| `bateria_v13E.py` | `organismo/bateria_v13.py` **(CONGELADA)** | `1a027bcb37eb536e` | `bed81b870faf5da5`¹ |
| `bateria_generaliza_E.py` | `organismo/bateria_generaliza.py` **(CONGELADA)** | `46772f5a582872c8` | `9b213f803933a9e9` |

¹ Sha tras el parche ERR-30 (§3): el sha anterior, sin el parche, fue `bded47a8f1211df7` — quedó 3 semillas × 84
comparaciones en 0/84 en el criterio 5 (ver §3) y no llegó a correr el examen; se reemplazó, no se conserva.

Constructor único: `construye_v13E.py`. Las dos baterías son **copias por anclas**: cambian sólo el módulo que
importan (y las rutas, por vivir fuera de `organismo/`); **las seis etapas, los `CRIT` importados, los umbrales
del criterio v3' y los criterios G1/G2/K quedan INTACTOS salvo el criterio 5, adaptado por ERR-30 (§3)**, y los
originales no se modificaron.

**Identidad obligatoria** (`identidad_v13E.py`, corrida ya por el diseñador, un proceso, T = 10 000):

- **(A)** `organismo_v13p`, con sus perillas en su propio default (todas apagadas), es `organismo_v13` bit a bit
  en **todas** las claves de v13 — 3 semillas × 3 escenarios (base, inversión en T/2, estímulo nuevo C veneno).
- **(B)** `organismo_v13E` por defecto es `organismo_v13p` llamado con los kwargs exactos de
  `BRAZOS['dE-TEST']` (`eta_pred=0.03, ema_pred=0.05, k_testE=10.0`) bit a bit, **mismas claves exactas** —
  3 semillas × 3 escenarios, mundo AB.
- **(C)** lo mismo para `organismo_v13gE`/`organismo_v13pg`, mundo de regla — 3 semillas × 2 reglas.
- **(D)** `bateria_generaliza_E.py organismo_v13p 3` da lo mismo, **línea a línea**, que
  `organismo/bateria_generaliza.py organismo_v13 3`.
- **(E)** `organismo_v13E(eta_s=0, puerta=None, k_testE=0, eta_pred=0)` es `organismo_v11` bit a bit en **todas**
  las claves de v11 — 3 semillas. Prueba el parche **ERR-30** (§3): el criterio 5 adaptado dentro de
  `bateria_v13E.py`.

**A/B/C/D prueban que el constructor no rompió nada; E prueba el parche ERR-30 del criterio 5. NINGUNA prueba que
la perilla ON (con `k_testE`/`eta_pred` en sus valores del brazo) sea inerte** (no se espera que lo sea; ver §1).
**Resultado: IDENTIDAD 28/28 (123.3 s)** — A 9/9, B 9/9, C 6/6, D 1/1, E 3/3.

> **Trampa de instrumento (la misma de `identidad_v13D.py`):** `experimentos/v13_dos_vias/` contiene **su
> propio** `organismo_v13.py` (`88c3574cf9cf38bf`), distinto del tronco congelado (`cc8b16b492d4d324`).
> `organismo/` va primero en `sys.path`, siempre (ERR-28).

## 3. Criterio 5 adaptado (v3'' para órganos en la boca) — ERR-30

**Escrita ANTES de correr el examen** (después de ver el primer `--humo`, que es exactamente para esto: probar
el montaje con números que no cuentan como evidencia — regla 3 de `EQUIPO.md`). No es una recalibración de un
umbral con datos del examen real; es una corrección de la FORMA del criterio 5, con el mismo procedimiento que
`ERR-21` usó para desdoblar el criterio 3 en 3'/3'': se declara aquí, con ERR numerado, antes de que el examen de
101–120 corra.

**Por qué.** El criterio 5 de `organismo/bateria_v13.py` (`tarea_id`) reduce el candidato a v11 (y, por separado,
a v10) apagando `eta_s` y `puerta` — las dos perillas del esquema de DOS VÍAS. Eso basta para v13 y para la hija
dispersa (`nivel7_hija_dispersa`, cuya perilla vive dentro de la vía RÁPIDA, la misma que v11 ya tiene). **No
basta para dE-TEST**: `k_testE·s̄_E` se suma a `Vb` **después** de `alpha·w`, sin pasar por `eta_s` ni por
`puerta` — apagar esas dos no apaga esto. El primer `--humo` de este paquete (2 semillas, 101–102) lo confirmó:
**criterio 5 dio 0/84** y `bateria_v13E.py` abortó por su propia guarda, exactamente como debía (`sys.exit(1)`
antes de correr las seis etapas) — la instrumentación no estaba rota; el criterio, tal cual, no podía medir a
este candidato.

**Qué compara exactamente ahora.** El parche (por anclas, en `construye_v13E.py`, aplicado sobre la copia de
`bateria_v13.py` que ya construye `bateria_v13E.py`) añade `k_testE=0.0, eta_pred=0.0` a las DOS llamadas de
`tarea_id` — la que reduce a v11 y la que reduce a v10 (`div_signo=False`) — dejando `eta_s=0.0, puerta=None`
como ya estaban. Las siete claves de `ESC_ID` y el resto del examen (criterios 1, 2, 3'/3'', 4a'–4d) **no se
tocan**. Verificado a mano antes de escribir esta sección: `organismo_v13E.run(seed, eta_s=0.0, puerta=None,
k_testE=0.0, eta_pred=0.0)` es bit a bit `organismo_v11.run(seed)` (semilla 1, T=5 000); `identidad_v13E.py` lo
repite formalmente en 3 semillas (parte **E**, §2).

**Cláusula (la misma forma que el criterio 5 original).** Si con las CUATRO perillas apagadas (`eta_s`, `puerta`,
`k_testE`, `eta_pred`) `organismo_v13E` no es `organismo_v11`/`organismo_v10` bit a bit, **el instrumento está
mal y no se interpreta nada más del examen** — igual que si el criterio 5 original fallara en `bateria_v13.py`.
Esto no es negociable ni se relaja: es una identidad, no una medida.

**Precedente y registro.** `ERR-21` (`experimentos/v13_dos_vias/PREREGISTRO_tronco_v13.md`, criterio 3 → 3'/3'')
es la forma: un criterio que no distingue lo que se necesita distinguir se **reescribe**, con su propio ERR, antes
de la serie nueva — nunca se relaja un umbral después de ver datos. `registro/REGISTRO_etapas_1_2.md` ya trae una
entrada "Examen v3' y órganos que actúan en la boca" anotando esta decisión antes de correr el examen; ésta es su
justificación completa.

**Confirmado con el segundo `--humo`** (2 semillas 101–102, tras el parche): `5_identidad = True`, y con la
identidad pasando `bateria_v13E.py` corrió el examen completo por primera vez — los OCHO veredictos en `True`
(`1_cientificos, 2_celdas, 3_control, 4a'–4d`), incluidas las nueve etapas científicas a 2/2. A 2 semillas esto
**no es evidencia** (regla 3), pero confirma que el parche deja pasar la instrumentación de punta a punta, que es
exactamente lo que un humo debe probar.

## 4. El mecanismo (el mismo de C-P1, sin cambiar una constante)

Sobre `organismo_v13p`/`organismo_v13pg` (que a su vez llevan el automodelo importado de `creacion_C`, todo
apagado salvo lo de este bloque):

```
b_dE  = Wpe·P + Wke·kenyon(P)                      (predictor lineal de ΔE, al morder; bloque 6, copiado)
e     = E_VAL[valencia] − b_dE  ;  s_E = |e|
Wpe  <- clip(Wpe + eta_pred·e·P,          ±clip_e)
Wke  <- clip(Wke + eta_pred·e·kenyon(P),  ±clip_e)
s̄_E  <- (1 − ema_pred)·s̄_E + ema_pred·s_E           (CAUSAL: la usa la boca del PRÓXIMO encuentro)
Vb    = alpha·w + hambre_boca·hambre + 0.5 + k_testE·s̄_E
```

`eta_pred = 0.03, ema_pred = 0.05, k_testE = 10.0` — **los mismos tres valores medidos y preregistrados** en
`PREREGISTRO_probar_si_mismo.md` (brazo `dE-TEST`, `K_TEST = 10.0`, tabla de perillas §2); no se barren ni se
ajustan aquí. `k_test` (el término del automodelo/SELF-TEST) se queda en su default `0.0`: este bloque no lo usa,
igual que el resto de perillas nuevas de `organismo_v13p` (todas ya apagadas por defecto).

## 5. Diseño

Semillas del examen de congelación de v13 (**101–120**, las de ERR-21), igual que `nivel7_hija_dispersa`:

1. **IDENTIDAD** (§2, incluida la parte E del criterio 5 adaptado, §3). Si hubiera fallado, no se corre nada más.
2. **E1 RETENCIÓN:** `bateria_v13E.py 20 --desde 101 --log` — el examen **criterio v3' COMPLETO** con el
   **criterio 5 adaptado (§3, ERR-30)** (las seis etapas E1/E2/E2I/E2J/E2K/E2L, celdas ≤ 45, 3'/3'', 4a'–4d,
   identidad 5) — los **ocho** veredictos.
3. **E2 GENERALIZACIÓN:** `bateria_generaliza_E.py organismo_v13E 20 --desde 101 --log` — G1, G2 y K, fórmula sin
   tocar.
4. **E3 INERCIA (diagnóstico, NO gate):** en escenarios **sin inversión** (T = 100 000 por defecto, sin
   `invertir_en`), `organismo_v13p` (apagado) contra `organismo_v13E` (ON) en las mismas semillas —
   divisiones/celdas dentro de **±10 %**, y el sesgo de boca acumulado (`sesgo_boca` por cuarto y `sbarE` final,
   ambos ya devueltos por `run()`) debe ser **pequeño** (ver §6). E3 no aparece en la cláusula de refutación
   (§7): es lectura, exactamente como D3 en `nivel7_hija_dispersa`.
5. **Referencia** con `organismo_v13p` (apagado) en las mismas semillas, para comparar contra el registro de v13
   (`examen_v13_20260917_165859`, `regresion_generaliza_organismo_v13_20260917_170148`, ambos verificados en
   disco).

Las baterías se lanzan como **subprocesos secuenciales** (cada una abre su propio `Pool(14)`): un solo `Pool` a
la vez, regla 11. `corre_baterias_v13E.py` usa una **clave explícita** por etapa (`E1`, `E2`, `E2_ref`) al
guardar cada veredicto — ver la nota de cabecera de ese script sobre una colisión de claves encontrada en
`corre_baterias_v13D.py` (`etiq.split()[1]` hace que la etapa de generalización ON y la de referencia OFF
escriban en la MISMA clave `'GENERALIZACION'`, y la de referencia corre después y la pisa). Para la hija dispersa
—perilla predicha casi inerte— probablemente no cambió el veredicto final; aquí, con una perilla que sí cambia el
comportamiento, sí habría importado. **Corregido: ERR-29** (`registro/REGISTRO_etapas_1_2.md`). El mismo día se
corrigió también `corre_baterias_v13D.py` (no congelado), con claves `D2`/`D2_ref`, **sin volver a correrlo**: el
veredicto ya registrado (`D2_generalizacion = True`) no cambia porque las dos corridas (ON y OFF) pasaban.

## 6. Predicción numérica

- **E1 (retención).** `bateria_v13E` cumple el **criterio v3' completo, con el criterio 5 ADAPTADO (§3,
  ERR-30)**, en 101–120: **los ocho veredictos en `True`** (5_identidad ya con las cuatro perillas apagadas,
  1_cientificos, 2_celdas, 3_control con 3' ≤ 1/20 y 3'' ≥ 19/20, 4a', 4b, 4c, 4d).
  Lo **ya medido** (mundo largo, M5 de `corre_probar_si_mismo.py`, serie 3, semillas 81–100): las seis etapas
  **20, 19, 20, 20, 20, 20** de 20 (una sola semilla por debajo en una etapa; sirve de calibración de qué tan
  "casi perfecto" es realista esperar, no cambia el umbral). **Lo NUEVO aquí** (nunca medido para dE-TEST, en
  ninguna semilla): 3' ≤ 1/20, 3'' ≥ 19/20, celdas ≤ 45, 4a'–4d, **y la identidad 5 adaptada** — ésta es la que
  §1 y §3 marcan como prueba genuina, no formalidad, precisamente porque la perilla no es inerte (con el criterio
  SIN adaptar, ya se vio en el humo que da 0/84: §3).
- **E2 (generalización).** `bateria_generaliza_E organismo_v13E`: **G1 ≥ 0.80** y **G2 ≥ 0.85**. Dos referencias:
  (a) v13 mismo en 101–120 (`regresion_generaliza_organismo_v13_20260917_170148.json`, verificado en disco): G1
  px0 0.800 / azar 0.500 / px0 > azar 18/20; G2 px0 0.892 / azar 0.458 / 20/20; (b) dE-TEST en 81–100
  (`probar_si_mismo_s81-100_20260918_012715`, M6, otras semillas, instrumento hermano `organismo_v13pg` con los
  mismos kwargs en vez de `organismo_v13gE`): **G1 px0 0.90, G2 0.85** — exactamente en el borde del umbral de
  G2 que se fija aquí. Con **K con cobertura ≥ 6 en 20/20 semillas** (más estricto que el ≥ 90 % que exige
  `bateria_generaliza.py` por sí sola).
- **E3 (inercia y sesgo, SIN criterio de aceptación).** Divisiones y celdas de `organismo_v13E` dentro de
  **±10 %** de `organismo_v13p` en las mismas semillas sin inversión. Sesgo de boca **pequeño**: mediana de
  `sesgo_boca[q]` (los cuatro cuartos) **< 0.05** y mediana de `sbarE` final **< 0.05**. El umbral se fija **por
  comparación**, no por una corrida previa en este mundo sin inversión (no existe una): **0.05 está por debajo
  de `CONST-a`** (`test_fijo = 0.173`, `PREREGISTRO_probar_si_mismo.md` §5), el sesgo constante más chico que
  este mismo proyecto ya trató como "no despreciable". Si `sbarE`/`sesgo_boca` resultan del orden de `CONST-a` o
  mayores incluso **sin nada que predecir** (sin inversión el predictor de ΔE debería converger y su error caer
  cerca de cero), sería la señal de que el predictor no consolida en este mundo más simple que el de C-P1 —se
  registra como hallazgo, **no tumba el candidato por sí solo** (E3 no está en la cláusula de refutación, §7).

## 7. Cláusula de refutación (escrita antes)

**Si cae la generalización (G1 < 0.80 o G2 < 0.85, o K < 20/20) o la retención (cualquiera de los OCHO
veredictos del criterio v3' en `False` — incluida la identidad 5 ADAPTADA de §3, ERR-30), "la sorpresa del mundo
en la boca" se queda
como ÓRGANO DE EXPERIMENTO** —validada en su propio diseño (C-P1, tres series 41–60/61–80/81–100: recuperación
0.143×/0.144×/0.141×, se apaga sola, no envenena, M5/M6 de la serie 3 ya OK)— **y NO entra al tronco.** No se
recalibra `eta_pred`, `ema_pred` ni `k_testE`: se registra el fallo, y si hay un mecanismo nuevo se preregistra
aparte con semillas nuevas (precedente ERR-21). E3 (inercia y sesgo sin inversión) es lectura, no gate: aunque
muestre que el sesgo es grande incluso sin inversión, eso **no** tumba el candidato por sí solo — sólo E1
(retención) y E2 (generalización) lo hacen.

Si E1 y E2 pasan, lo declarable es: *"la sorpresa del mundo en la boca no daña la retención ni la generalización
del tronco"* — y entonces, y sólo entonces, tiene sentido preguntar si v14 = v13 + dE-TEST (o v13 + dE-TEST +
hija dispersa, dado que `PROPUESTA_v14.md` marca los dos candidatos como componibles), con su propio preregistro
de congelación: gemelo compilado con arnés de identidad (regla 9) y `manifiesto.py` — la réplica de retención y
generalización de la serie 3 (81–100) ya está corrida (§ arriba), así que lo que sigue tras este bloque es la
congelación, no una réplica nueva.
