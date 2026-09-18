# REFUTACIÓN — sala 2, lente MEDIBILIDAD Y EVIDENCIA, del diseño «dos_escalas» (`DISENO_dos_escalas.md` 0242fdf0718dbb8b)

**Refutador de la sala 2, 18 sep 2026, ~10:15.** Misión primero: llegar a la AGI por este camino — un organismo mínimo con reglas
locales, sin retropropagación en el runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada.
Primero la frontera; segundo, que viva.

**Reglas cumplidas.** No edité ningún archivo del repo. Creé tres archivos nuevos en `sala2/`: este documento,
`refuta_dos_escalas_estructural.py` (ba459eceb6225171) y su salida `refuta_dos_escalas_estructural.json` (e6329dd3163406a2). No corrí
el organismo ni ningún `Pool` (hay uno vivo: v15e/v15f del coordinador). Los dos cálculos que hice son de sólo lectura sobre
`organismo_v14g.split_regla` (reparto tren/test y ajuste de mínimos cuadrados sobre los 8 de tren): no simulan un paso del organismo.
Todo lo demás es lectura de datos que ya existen en `datos/` y del código congelado (`organismo_v14.py` feefc88b1fd8d434,
`organismo_v14g.py` 1f1318480cd34cde).

## Veredicto en una línea

**REFUTADO como está escrito:** su puerta P1 ya está caída por datos que existían tres minutos antes de guardarse (v15f serie 09:53–10:00:
E1 "veneno Q4 < Q1" 17/20 y E2I `W_C ≤ −2.5` 17/20, que v16 hereda bit a bit en conducta), sus umbrales nuevos no deciden (zonas
muertas entre "pasa" y "refuta", `n*` sin regla de censura) y uno de ellos (P4 "≥ 0.75 en ≥ 16/20") está **por encima del techo de
información** de sus propios rasgos en las semillas que eligió (LSQ exacto: 15/20); además juzga con el criterio v1 que el director
retiró a las 09:55 y omite tres de las siete puertas del criterio v2.

## 1. Motivos, con evidencia

### M1 — La puerta que mata (P1) ya está caída por datos anteriores al diseño; v16 la hereda en conducta, no la puede pasar

- El diseño se basa en el **humo** de v15f (`v15f_humo_20260918_094706`, 2 semillas) y predice para P1: *"E1 'venenoQ4<Q1' y E2I
  'W_C≤−2.5': 19–20/20 … ≤ 18/20 → el canje es real"* y en la cláusula: *"Si P1 o P2 caen (≤ 18/20 en cualquier subcriterio …), v16
  no entra al tronco"*.
- La **serie** de v15f terminó a las 10:00:43 (`datos/v15f_s161-180_20260918_095309.json` b0c5e28e04c6f3e5; examen
  `examen_v15f_20260918_095443.json` c72c6ab10186fc7e): **E1 17/20 (venenoQ4<Q1), E2I 17/20 (W_C ≤ −2.5)**, V1 = NO. El diseño no la cita
  (su lista de fuentes termina en el humo 09:47–09:50).
- v16 no puede cambiar esos dos números. Derivado del propio pseudocódigo del diseño: (a) en E1/E2 la consolidación **no actúa**
  (`n_consolida = 0`, P7 del diseño: 14 pares empatan exactamente; lo verifiqué par a par con A = 110100 y B = 101010: sólo (0,5) comparte
  casilla) → `_regla ≡ lineal`; (b) el replay sólo mueve `Wps/Wns`, y **la boca nunca lee la lineal para A ni B después de la primera
  mordida** (casilla vista → lee la tabla; familiar → lee la rápida). Luego la conducta de E1 en v16 ON es la de v15f ON: Q1 con 2–11
  mordidas de B porque la tabla dice −3 desde la primera → 17/20 otra vez. En E2I la palabra (2,3) consolidada es **silenciosa** (P2·P3 = 0
  en A, B y C, como dice el diseño) y `W_C` lo lee la rápida cuando C se hace familiar → 17/20 otra vez.
- Conclusión: correr el bloque decidiría P1 en NO con certeza, por una letra (**ERR-44**, coordinador 10:05: "veneno Q4 < Q1 no puede
  distinguir 'aprendió en una mordida' de 'no aprendió'") que el diseño reconoce en su §6.7 y aun así deja como puerta de muerte. Es el
  patrón de ERR-06/08/10 (un criterio que no dice lo que se quiere decir), conocido antes de correr.

### M2 — Los umbrales nuevos no deciden: zonas muertas y `n*` sin regla de censura (lente ERR-37)

- **P4:** pasa con *"mediana ≥ 0.75 y ≥ 0.75 en ≥ 16/20"*; se refuta con *"mediana < 0.65 o < 12/20"*. Entre 0.65 y 0.75 de mediana, o
  entre 12 y 15 semillas, el bloque **ni pasa ni se refuta**, y el diseño dice al mismo tiempo "sin modos intermedios". Lo mismo en
  **P5**: pasa con `n*_lineal` ON ≤ 0.5 × SIN_REPLAY; se refuta con ≥ 0.8 ×; entre 0.5 y 0.8 no hay lectura.
- **`n*_lineal` puede no existir y no hay regla.** Se define como *"mordidas de tren hasta la primera sonda ≥ 0.75"* (sonda cada 2 000
  pasos). En el brazo SIN_REPLAY con relevo ON, la boca lee la tabla (−3 exacto) desde la primera mordida de cada veneno de tren y deja de
  morderlo (humo v15f: B pasa de 27 a 2 mordidas en Q1); la lineal recibe un puñado de mordidas de veneno y **puede no cruzar 0.75 antes
  de T/2** (OFF no cruza nunca: "> 600", A-4). C8 ya tuvo corridas *censuradas* y las reportó como tales; el diseño no dice qué vale una
  mediana con censurados: si SIN_REPLAY es ∞ en ≥ 10/20, "ON ≤ 0.5 ×" se cumple trivialmente o no se puede calcular. P5 no es decidible
  como está escrito.
- **P6 px0 "palabra consolidada ≤ 3/20 (empate de 5 celdas (0,j))"** está mal derivado y por eso abortaría el bloque por la razón
  equivocada. El empate exacto de E1 existe porque los 14 pares reciben *la misma aritmética en las mismas mordidas*. En px0 los cinco
  pares (0,j) son consistentes con la regla, pero sus casillas se visitan por primera vez en **mordidas distintas** (la casilla `11` de
  (0,1) la abre un patrón con P1 = 1; la de (0,2), otro): sus EMA de error divergen en la primera visita distinta y **nunca vuelven a
  empatar** (decaen desde valores distintos). Luego hay ganadora única estable → racha de 10 → consolidación de algún (0,j) en casi
  todas las semillas (el v15f de 161–180 en px0 ya reporta ganadora repartida: (0,1) 2/20, no ≈ 4/20 de un empate aleatorio). El propio
  diseño manda entonces "reescribir A5, ERR" **antes de leer P4**: el bloque se anula a sí mismo por un control que no mide lo que dice.
  De paso muestra que "racha de 10 victorias únicas = competencia decidida" es una equivalencia no demostrada: la racha sólo exige un
  argmín único, que existe genéricamente.

### M3 — P4 pide más de lo que la información permite en las semillas elegidas (umbral por encima del techo)

- Cálculo estructural (`refuta_dos_escalas_estructural.py`, sólo `split_regla` y `numpy.linalg.lstsq`; el mismo proxy "gradiente exacto"
  que usó A-5): con **los 7 rasgos del diseño** {P0..P5, P0·P1}, sin sesgo (la lineal del tronco no lo tiene), ajustados a los 8 de
  tren con objetivos +1/−3 y leídos con la puntuación ESTRICTA en los 12 nunca vistos:

| rango | lineal 6 px (v14.1) | **lineal + palabra (0,1)** (el techo de la lectura "sin tabla") | oráculo {P0,P1,P0·P1,1} |
|---|---|---|---|
| **181–200** (el del diseño) | mediana 0.500, ≥ 0.75 en 0/20 | mediana 1.000, **≥ 0.75 en 15/20** | 1.000, 16/20 |
| 201–220 (réplica) | 0.375, 0/20 | 1.000, 18/20 | 1.000, 19/20 |
| 161–180 (v15f) | 0.438, 0/20 | 1.000, 17/20 | 1.000, 19/20 |

- La regla delta no puede superar al ajuste exacto en signo de forma sistemática; en 181–200 el **óptimo** da 15/20 ≥ 0.75 y el diseño
  exige **≥ 16/20**. El resultado más probable cae en la zona muerta de M2 (12–15/20) y, si se leyera por el lado de la refutación,
  diría *"la palabra no sostiene XOR sin la tabla: las dos escalas no se conectan"* — un diagnóstico de mecanismo para un límite de
  información (exactamente el error que ERR-35 cerró: no preguntar al mundo de 8 ejemplos lo que no contiene). El cálculo también
  dice lo bueno: **la información sí está** una vez dado el par (mediana 1.000); por eso el umbral correcto no es un número fijo sino
  "≥ techo LSQ de la semilla − δ" o el pareado contra el techo, escrito antes.
- La **cláusula de muestreo** del diseño está mal contada: dice "40/40 con ≥ 1 patrón `11` y 39/40 con ≥ 1 `00`". Medido: 181–220 →
  40/40 con `11`, **38/40** con `00` (semillas 188 y 213), y 6 semillas con **un solo** `11` en el tren (186, 190, 194, 202, 211, 218):
  ahí la palabra aprende su peso de un único patrón. Además en 3/20 semillas de cada rango hay **un segundo par consistente con el tren**
  (181: (0,2); 193: (3,5); 196: (1,3); 202: (1,5); 205: (3,5); 216: (1,2)) con error propio 0 tras sus primeras visitas: la consolidación
  es **irreversible** (`F_max = 1`, sin regla de des-consolidación) y en esas semillas el par que consolida lo decide el orden de las
  primeras visitas, no la regla. El diseño no lo preregistra ni lo excluye.

### M4 — Juzga con el criterio v1, retirado a las 09:55, y omite tres de las siete puertas del criterio v2

- `registro/CRITERIO_TRONCO_v2.md` (022059d98ee57bc8, 09:58) exige a **todo candidato nuevo** T-A (sobrevive en el mundo vivo: muertes,
  r = descendientes − muertes), T-C (se desdice también en el mundo vivo), T-D (bloque de la sal 9 ALIAS / 9 LIMPIAS), T-E (**conducta**
  ≥ 18/20 por escenario; "los pesos internos se REPORTAN, no son puerta"). El diseño no cita el criterio v2, no tiene mundo vivo, no
  tiene bloque de la sal, y sus puertas P1 ("W_B ≈ −3", "W_C ≤ −2.5") y P4 (`W_apriori_regla`, un peso interno leído en la sonda) son
  exactamente pesos internos como puerta. La capacidad declarada (P4) **no es conducta**; la versión conductual (P4b, `ba` tras la
  lesión) queda con umbral más bajo (0.65) y "no es lo que se declara".
- Está además fuera del orden fijado por el director (REGISTRO 09:55, punto 5): (a) criterio v2 → (b) **mundo que obliga** → (c)
  crecimiento por sorpresa → (d) tokens y variables → (e) población. El diseño corre en el mundo de regla de 6 px y 20 patrones, el que
  la misma decisión declaró agotado ("no se le vuelve a preguntar lo que no puede responder"), y mete la capacidad como **perilla diseñada
  a mano** (`consolida = 10`, `F_max = 1`, `replay = 1`) cuando el punto 3 manda: "ninguna capacidad nueva entra como perilla … si puede
  entrar como crecimiento". Con la lente de la sala: es la quinta reparación de la línea v15c → d → e → f → v16 sobre el mismo mundo, no
  una salida de la frontera.

### M5 — Instrumento y coordinación: colisión de nombre y de semillas, y un runner con dos umbrales

- **`organismo_v16.py` ya existe** en esta carpeta (9906cdbb9b533b13, generado por `construye_v16.py` 2ddfa30538f4e0ce a las 09:54): es el
  instrumento del diseño *radical* (TOKEN/grafo de retinas), no el de dos_escalas. El diseño propone crear `construye_v16.py → organismo_v16.py`
  con otro contenido: dos módulos con el mismo nombre en rutas distintas es la familia de ERR-28/ERR-38 (el `import` carga el que primero
  esté en `sys.path`, y los dos declaran "apagado ≡ v14.1", así que la identidad 24/24 no lo detectaría).
- **Semillas:** el diseño toma 181–200 como "vírgenes" y 201–220 para la réplica; el coordinador acaba de asignar (REGISTRO 10:05)
  **181–200 en el mundo de regla a v15f** para su juicio con el criterio v2 (más 121–140 examen y 301–320 mundo vivo). Si v16 se corre en
  las mismas, no son nuevas para la base que dice heredar.
- **P2 con dos umbrales:** el diseño exige G1 ≥ 0.80 / G2 ≥ 0.85 y a la vez que el runner "copie el booleano de la batería y aborte si su
  relectura difiere"; la batería congelada decide con 0.65 / 0.55. Con G1 ∈ [0.65, 0.80) el booleano de la batería dice PASA y el
  preregistro NO: "difiere" → aborta por instrumento cuando en realidad es un veredicto legítimo. Hay que decir cuál manda (v15f resolvió
  con un AND explícito).
- Menor: en ON+BORRAR la lesión ocurre al principio del paso `fase2_en − 1` y la mordida de ese mismo paso lee `_regla` en vez de la tabla
  → `mord` Q2 puede diferir en 1 de ON en alguna semilla; "idénticos 20/20 bit a bit" puede caer por eso y no por instrumento roto.
  Especificar la lesión **después** de la mordida de ese paso o exigir identidad hasta `fase2_en − 2`.

## 2. Lo que el diseño sí tiene bien (para no tirar lo bueno)

- Las derivaciones de inercia (P7) son correctas donde las verifiqué: 14 pares empatan exactamente en E1/E2; (2,3) queda única en E2I
  desde la primera mordida de C y la palabra es silenciosa en A, B, C; 6 casillas compartidas D/B y 8 restantes empatadas en E2J/E2K.
- Los controles CONS_SHUF / REPLAY_SHUF y `azar` en las tres lecturas son los que separan "la palabra correcta" de "cualquier palabra":
  bien puestos. La sonda antes de `tipos.extend(test)` es la correcta (v14g L113–116).
- El coste está sobreestimado, no subestimado: v15f hizo 120 corridas de T = 200 000 en 134 s con Pool(14); los 300 del diseño son ≈ 6 min,
  no 22. Examen ≈ 3 min, V2a ≈ 46 s (medidos hoy). Realista.
- La información **sí** está para la lectura "sin tabla" (techo LSQ mediana 1.000 con el par dado): la idea de que la regla se quede con
  lo que el episodio identificó no está muerta; está mal medida y en el mundo equivocado.

## 3. Qué lo salvaría (en orden; ninguno es enmienda de umbral tras ver datos porque el bloque no ha corrido)

1. **Reescribirlo contra el criterio v2, no contra v1.** P1 pasa a T-E (conducta por escenario ≥ 18/20; `W_B`, `W_C` reportados), y se
   añaden T-A, T-C y T-D con sus umbrales tal como están en `CRITERIO_TRONCO_v2.md`. Sin eso no es candidato, sea cual sea P4.
2. **Umbrales que partan el espacio.** Para P4 y P5: un solo número por lado ("≥ 0.75 en ≥ k/20 pasa; si no, refutado"), con k fijado
   **por debajo del techo LSQ de las semillas elegidas** (181–200: 15/20; mejor: pareado por semilla contra el techo, `acc ≥ techo − 0.125`
   en ≥ 16/20). Regla de censura escrita: `n*` no alcanzado en T/2 = censurado; P5 se decide sólo si ≤ 4/20 censurados en cada brazo,
   y se reporta la fracción censurada al lado.
3. **P6 px0 corregido:** la consolidación en px0 **ocurrirá**; el control válido es "la palabra consolidada en px0 es uno de los cinco
   (0,j) en ≥ 18/20 y G1 px0 sin tabla ≥ 0.90", no "≤ 3/20 consolidaciones".
4. **Des-consolidación local** (la mitad "desaprender" de la misión): si la celda consolidada deja de ser ganadora única durante
   `consolida` mordidas seguidas, `_FEAT = None` y `Wpf = Wnf = 0`. Preregistrar en E2 del mundo de regla (cambio de regla en T/2) que la
   palabra se retira; y reportar en las 6 semillas con segundo par consistente qué par consolidó.
5. **Mini-prueba antes del Pool** (permitida: ≤ 6 corridas de un proceso): 3 semillas de 181–200 con ON, leyendo `W_apriori_regla`,
   `t_consolida` y `n_replay`; hoy P4/P5 no tienen ni un número medido detrás (el propio diseño lo dice).
6. **Instrumento y semillas:** nombre sin colisión (`organismo_v15g_pal.py` o el que asigne el coordinador; nunca `organismo_v16` mientras
   exista el del diseño radical), semillas que el coordinador reserve (221–240 o siguientes en el mundo de regla), un solo umbral en
   V2a con AND explícito, lesión después de la mordida del paso.
7. **El mundo:** o el mismo mecanismo se preregistra en el mundo que obliga (una vez exista, con v14.1 y v15f como controles) o en el
   mundo vivo (tabla y palabra por necesidad, §7 del propio diseño), o se declara honestamente como **v15g: reparación de la línea de
   pares**, con ese nombre, y espera turno detrás de (b)–(d) del orden del director.

## 4. Fuentes

`sala2/DISENO_dos_escalas.md` (0242fdf0718dbb8b) · `organismo/organismo_v14.py` (feefc88b1fd8d434, L50–64, L100–120, L164) ·
`organismo/organismo_v14g.py` (1f1318480cd34cde, L37–54 `split_regla`, L113–116 sonda) · `experimentos/creacion_A/PREREGISTRO_v15f.md`
(df7348599aa68333) y `construye_v15f.py`, `organismo_v15f.py`, `corre_v15f.py` (V2a: AND explícito) · `datos/v15f_humo_20260918_094706.log`
· `datos/v15f_s161-180_20260918_095309.{log,json}` (b0c5e28e04c6f3e5) · `datos/examen_v15f_20260918_095443.{log,json}` (c72c6ab10186fc7e) ·
`datos/regresion_generaliza_v15f_organismo_v15f_on_20260918_095744.log` · `datos/v15e_s141-160_20260918_092921.log` ·
`registro/CRITERIO_TRONCO_v2.md` (022059d98ee57bc8) · `registro/REGISTRO_etapas_1_2.md` (bloque 3 M3 07:43/07:47; ERR-35; ERR-37; v15e;
decisión 09:55; entrada v15f 10:00 y ERR-44) · `registro/EQUIPO.md` (reglas 3, 4, 10–14) · `ENJAMBRE_xor_20260918.md` (§4.1 desempate,
§5 M3) · `PUENTE_creacion.md` (A-4, A-5, C8) · `sala2/DIAG_dinamica.md` (§1.1, B3, §4), `DIAG_metodo.md` (bloqueo 2, §2.3),
`DIAG_mundo.md` (bloqueo 1) · `sala2/construye_v16.py` (2ddfa30538f4e0ce) y `organismo_v16.py` (9906cdbb9b533b13, diseño radical) ·
`sala2/refuta_dos_escalas_estructural.py` (ba459eceb6225171) → `.json` (e6329dd3163406a2).
