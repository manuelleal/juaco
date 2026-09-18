# Auditoría — Bloque 2 (curiosidad), Bloque 3 (XOR lectura) y N3d mudo — 17 sep 2026

Leídos `registro/EQUIPO.md` y el bloque "Estado (día 5)" de `CLAUDE.md` antes de auditar. No edité ni corrí nada.
Al momento de leer, Bloque 2 y Bloque 3 ya tenían corrida y veredicto (`datos/curiosidad_s41-60_20260917_211739.*`,
`datos/xor_lectura_s1-20_20260917_213124.*`, registrados en `REGISTRO_etapas_1_2.md:3251-3293`): los dos fueron
REFUTADOS tal como estaban escritos. Ningún hallazgo de esta auditoría es bloqueante.

## Hallazgos

1. **[IMPORTANTE] Bloque 3 — la puerta de familiaridad enmascara la vía lenta en X1/X4**
   (`organismo_v13q.py:77-79`, sin tocar; criterios en `corre_xor.py:117,120`). Con `puerta=3`, `valor(P)` lee la vía
   RÁPIDA si ≥3 celdas del código del patrón (nunca visto) están consolidadas por solapamiento incidental con
   patrones entrenados — pasa igual en los tres brazos, independiente de `lectura`. Ya confirmado con datos
   (`REGISTRO_etapas_1_2.md:3286-3293`): `W_lenta(P0·P1) = −2.65` (signo y magnitud correctos, la vía lenta sí
   representa XOR) pero `acc` de CUADRÁTICA salió idéntica a LINEAL (0.438 ambas) — firma exacta de enmascaramiento,
   no de fallo representacional. Bien manejado: en vez de recalibrar, preregistraron `PREREGISTRO_xor_lectura_3b.md`
   (Y1–Y3, lectura pura de `W_lenta_apriori` + brazo `puerta=None`). Sugerencia para 3b: ya que Y2 mide la fracción de
   test "familiares", repórtenla por semilla junto al resto de la tabla, no sólo agregada.

2. **[IMPORTANTE] N3d mudo — el chequeo secundario del preregistro no es medible con lo que guarda el instrumento**
   (`PREREGISTRO_N3d_mudo.md:11`: "`n_sesgo_soc` en Q4 debe ser ≈0"; `mundo_social_n3.py` `Organismo.resultado()`
   ~L278). `n_sesgo_soc` se acumula sobre los 200 000 pasos completos; a diferencia de `dq`/`mord`/`vis`, no tiene
   índice de cuarto (`self.dq[self.q(t)]+=1` vs `self.n_sesgo_soc+=1`). El log sólo da el total (CONV_MUDO 14494 vs
   CONV 19670); el ~74% es consistente con la predicción por aritmética, no una verificación directa de Q4. No
   afecta el veredicto — M1/M2 sí usan `vis[k][3]`/`mord[k][3]`, correctamente indexados (`corre_N3d_mudo.py:54-58`)
   — pero el chequeo tal como está escrito no se puede auditar desde el JSON. Cambio propuesto: `n_sesgo_soc_q` de 4
   posiciones, igual que `dq`.

3. **[MENOR] Bloque 2 — el control "prioridad barajada" no garantiza "misma magnitud"**
   (`PREREGISTRO_curiosidad.md:25-27` vs `construye_curiosidad.py:32-35`, generado en `mundo_largo_c.py:48-51`).
   `_perm_c` permuta sobre las 90 celdas de `NKMAX`, incluidas las que aún no existen por división (`err_l-err`
   idénticamente 0 ahí); al empezar la corrida sólo 30/90 celdas están activas, así que parte del "progreso
   barajado" de un patrón puede venir de una celda muerta en vez de una celda activa con otro progreso. Esto diluye
   al control (lo debilita, no lo infla), y de hecho P3 dio NO (6/20 CUR>BAR) — no cambió el veredicto (ya negativo
   por P1), pero conviene arreglarlo (permutar sólo sobre `np.where(activa)[0]`) antes de reusarlo en "novedad de
   sitio", el siguiente candidato ya anunciado (`REGISTRO_etapas_1_2.md:3269`).

4. **[MENOR] Bloque 3 — la cláusula de refutación no listaba la causa real**
   (`PREREGISTRO_xor_lectura.md:32-34`). Preveía sólo "no encuentra el peso" o "el tiempo no alcanza"; la causa real
   (peso correcto pero tapado por la puerta) es una tercera opción no anticipada. No hizo daño porque registraron la
   sorpresa y escribieron 3b en vez de forzarla en una de las dos cajas — pero vale añadir "la puerta puede estar
   enmascarando la vía lenta" como causa candidata en preregistros futuros que toquen `puerta`.

5. **[MENOR] Patrón fragil repetido en los tres runners**
   (`corre_curiosidad.py:107`, `corre_xor.py:114`, `corre_N3d_mudo.py:122`, y `med()` en los tres). Sustituyen `None`
   por `0.0`/`0.5` cuando una métrica no se pudo calcular, y `med()` hace `min([])`/`max([])` sin guardia si TODAS las
   semillas de un brazo dan `None`. No se disparó en ninguna de las tres corridas auditadas, y ya causó un `KeyError`
   real en Bloque 2 (`vf[k]` con C/D), corregido antes de la corrida final (commit `d4367e0`). Sigue frágil para el
   próximo brazo que se agregue; vale una función compartida con guardia en vez de repetir el patrón.

## Verificado correcto (preguntas puntuales del encargo, Bloque 3)

`phi(P)` con `lectura='cuadratica'` (`organismo_v13q.py:73-76`): índice 6 = `P[0]*P[1]` porque `_IJ[0]=(0,1)` —
coincide con el supuesto de `corre_xor.py:63`. El drenaje `np.minimum(Wps,Wns)*(phi(P)>0)` (`organismo_v13q.py:136`)
tiene sentido con 21 entradas: la máscara marca, entre las 6 lecturas lineales y los 15 productos, cuáles están
activos para el patrón mordido — mismo rol que `P>0` con 6. `random15` (`organismo_v13q.py:69-72`) es un control
válido de "dimensión sin estructura": código de 15 bits fijo por patrón pero independiente de la regla y de los
demás patrones, no puede generalizar a los nunca vistos; el resultado real lo confirma (`acc=0.500` exacto, X2 OK).

## Cuatro trampas — sin hallazgos nuevos

**Canal social simétrico:** evitado en N3d/N3d_mudo por diseño experto/novato explícito (receptor `gamma_soc` activo,
emisor `escucha=False`, `corre_N3d_mudo.py:18-20`); no aplica a bloques 2/3. **Acierto sin balancear:** balanceado en
los tres (`corre_N3d_mudo.py:54-58`; `corre_xor.py:36-44`; `pool_de` 25/25 en `corre_mundo_largo.py:41-50`, heredado
por bloque 2). **Mundo que se come la comida:** comida y veneno se retiran/regeneran por el mismo camino de código
en los tres mundos (`mundo_largo_c.py:139-143`; `mundo_social_n3.py:44-50`). **Sitios fijos que se memorizan:** no
aplica a bloques 2/3; en N3d_mudo es estructuralmente imposible, no sólo vacía en los datos — el patrón enmascarado
del receptor es idéntico para el par comida/veneno de una misma "vista" (`corre_N3d_mudo.py:42-51` + máscara `MR` en
L15), y la posición nunca entra en `code()`/`Wp`/`Wn` (`mundo_social_n3.py:101-105`).

**Identidad (fugas):** las tres construcciones por anclas (`construye_curiosidad.py`, `construye_xor.py`,
`construye_n3.py`) reducen exactamente al original con la perilla apagada — verificado leyendo el código (los
`if gamma_C:` / `lectura=='lineal'` / `mudo_desde is None` son no-ops correctos) y en las corridas de identidad ya
hechas (3/3, 6/6, 6/6 en los tres logs). **Vocabulario:** disciplinado en los tres preregistros y en las entradas de
hoy del registro — usan líneas "Vocabulario:" que restringen, no inflan (p. ej. "transfiere por conducta; no
comunica, no entiende"; en bloque 3, "aprendió la estructura" se apoya en un peso medido, no en la conducta).
