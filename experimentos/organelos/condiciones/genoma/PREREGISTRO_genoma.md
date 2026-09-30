# PREREGISTRO — EXPLORATORIO DIAGNÓSTICO — CONDICIONES / GENOMA: ¿el muro de "no inventa combinaciones" es falta de capacidad? (30-sep-2026, creador)

Misión: llegar a la AGI por este camino. **EXPLORATORIO DIAGNÓSTICO** (5 índices). No decide tronco: decide el siguiente paso.
Escrito con el arnés PASADO (`identidad_gen_salida.txt`) y **antes** del humo y de cualquier número de estos brazos.
Carpeta: `experimentos/organelos/condiciones/genoma/` (sólo archivos nuevos). Se IMPORTAN sin tocar, con sha fijado:
- `sentidos_muro/corre_sentidos_muro.py` (`4776b80e18733079`);
- `bloques_pista/corre_bp.py` (`6b9c11a6639d3948`);
- los carros `V143_BQ2` (`183fb81cf6ad520c`) y `V143_BQ2AZA` (`aa88b32e4b4de152`);
- por `sentidos_muro.verifica`: pista, juez, TERMO, O1 y V143.

ERR-158 está usado. ERR-159 va a mutación. El siguiente libre de esta sesión se fija al cierre (la sesión JUACO 5 numera desde ERR-160). Auditoría H-G1.

## 1. Hipótesis (junta Fable, ingeniero genético)
Con las tasas de fábrica de V143_BQ2 (inicial 2, dup 0.02, del 0.07, ins 0.05), el cambio de largo esperado por parto es **0**.
El genoma queda en ~2 reglas (`PREREGISTRO_bloques_pista.md` §9: "se queda en el largo inicial (2.0)"). La regla PRUEBA de O1, escrita
en reglas, necesita dos (`corre_bp.PRUEBA_O1`: "desconocida → boca −" y "reserva → boca +"). Si el genoma tiene **capacidad** (inicial 6,
p_dup 0.06 → Δlargo **+0.04** por parto), la selección tendría lugar para juntar dos reglas y "no inventa combinaciones" podría ser un artefacto.

**Dato previo (no es de esta prueba; es la cadena fab en otras semillas):** en `sentidos_muro` bq2_pas (10 × 25k, prueba 59201–59205),
el largo de la siembra sube despacio de ~2.0 a 2.0–3.4 en p9 (las listas vacías no entran al banco: sesgo hacia arriba). El largo_med
del banco final de la prueba da **2.3 / 3.0 / 2.4 / 4.1 / 3.0**. La doble regla aparece en **0/45** linajes, y cruzan **11/45**.

## 2. Diseño (memoria nueva: cero; mecanismo nuevo: ninguno; las tasas son configuración del runner)
La cadena es la de `bq2_pas` de sentidos_muro:
- `corre_bp.prepara` / `corre_bp.siembra_de`;
- **10 pasajes de T 25 000**; el pasaje 0 va sin siembra;
- la siembra siguiente = la unión de los bancos finales (sólo entra quien parió);
- después, una **prueba a T 100 000** con la siembra final.

Se elige la cadena de 10 pasajes de sentidos_muro y no la de 4 de bloques_pista (28-sep) porque es la cadena sobre la que se concluyó "no inventa".

| brazo | carro | tasas | papel |
|---|---|---|---|
| **fab** | V143_BQ2 | fábrica | CONTROL (es bq2_pas en semillas nuevas; arnés F bit a bit) |
| **cap** | V143_BQ2 | **CAP** = inicial **6**, p_dup **0.06**, el resto de fábrica | CANDIDATO |
| **aza_largo** | V143_BQ2AZA | CAP | CONTROL que puede fallar (mismas tasas, **sin herencia**: cada cuerpo sale de una entrada al azar del banco) |

**Semillas NUEVAS** (grep 30-sep: `635xxx` sólo aparece como cifras de floats en un log de `reunion/`): el pasaje p del índice i (1..5) usa
**635000 + 10 i + p** (635010–635059), las mismas en los tres brazos (pareado); la prueba usa **635100 + i** (635101–635105). Humo: pasaje
635090 y prueba 635190. Arnés: 635192. No hay pareado con referencias viejas: fab es el control pareado.

**Medidas.** Todas salen de la prueba, salvo que se diga otra cosa.
- **largo_med:** la mediana, sobre los linajes con banco, del largo medio de las últimas 10 listas del banco final (= `corre_bp.resumen`).
- **doble** (la definición del encargo): en la **misma** lista hay ≥ 1 regla (sentido 7 u 8, acción boca, w < 0) y ≥ 1 regla (sentido 7 u 8, boca, w > 0).
  - `doble_lin` cuenta los linajes con una lista doble entre las últimas 10 del banco (de 45).
  - `doble_siembra` es la fracción de listas dobles en la siembra de cada pasaje.
- **Forma O1 (`es_o1`):** "7 `<` → boca −" y "8 `>` → boca +". Es estricta y se agrega como **lectura descriptiva** (`o1_lin`, `o1_siembra`); no entra en la letra (H-G3).
- **cruzan:** la suma de `cruza_real` de 45. También se registran R0 mediano, fundadores, largo de la siembra por pasaje y partos.
- **Piso de azar de doble (calculado y comprobado por Monte Carlo en el arnés M):** una regla al azar es "tipo prueba" con q = 2/9 · 1/3 = 2/27.
  Entonces P(doble | n reglas al azar) = 1 − 2(1 − q/2)ⁿ + (1 − q)ⁿ, que da **0.0354 con n = 6** y **0.0027 con n = 2**.

## 3. Instrumento y anclas (arnés `identidad_gen.py`, salida pegada en `identidad_gen_salida.txt`: **ARNES: PASA**, 108 s)
- (K) shas.
- (C) CAP difiere de fábrica sólo en inicial 6 y p_dup 0.06. Δlargo esperado: +0.04 en cap y 0 en fab.
- (F) **A tasas de fábrica este runner es el instrumento original bit a bit:**
  - fab = `sentidos_muro.tarea('bq2_pas')`, con siembra y sin ella;
  - aza_largo = `corre_bp.tarea('bloq2aza')`;
  - cap = fab;
  - `trabajo` fab = `sentidos_muro.trabajo('pas', 'bq2_pas')`, JSON por JSON;
  - reproduce el pasaje guardado `bq2_pas i1 p0` (s 614010, T 25 000) en linajes, pista, R0_pista, tel, tel_termo y bq.
- (A) **Las tasas nuevas actúan:**
  - la cfg del carro es CAP;
  - los fundadores sin banco tienen un largo mediano de 6 (fab: 2);
  - el operador `_bq_muta` del carro da Δlargo +0.0403 en cap y −0.0019 en fab.
- (M) La medida: `es_doble` y `es_o1` en 7 casos, y `PRUEBA_O1` es doble. El piso de azar coincide con el Monte Carlo (0.0354 contra 0.0351).
- (E) Regla 14: la entrada se compara campo a campo contra `corre_bp.tarea(carro, CAP)`. La siembra actúa (36/36 fundadores del banco).
- (D) determinismo.
- (W) reintento de abortos y reanudación de una cadena.
- (X) el runner niega pool > 2.
- (L) la letra en 14 casos.

## 4. Predicciones (firmadas antes del humo; `lee()` las imprime contra lo medido)
| # | predicción | p |
|---|---|---|
| I1 | (ingeniero) largo_med de cap ≥ 4.0 en ≥ 4/5 | 0.85 |
| I2 | (ingeniero) doble en ≥ 1/45 linajes de cap | 0.30 |
| I3 | (ingeniero) R0 sube: R0 mediano cap > fab, pareado, en ≥ 4/5 | 0.15 |
| K1 | (creador) = I1 | 0.85 |
| K2 | (creador) = I2 | **0.70** |
| K3 | (creador) veredicto CAPACIDAD SIN USO | 0.60 |
| K4 | (creador) veredicto CAPACIDAD PAGA | 0.07 |
| K5 | (creador) doble (co-presencia) (descriptivo, sec. 6; `compone` en el código) | 0.10 |
| K6 | (creador) suma de cruzan de cap ≤ la de fab | 0.55 |

Por qué discrepo en I2 (0.30 frente a 0.70): con 6 reglas al azar, 3.5 % de las listas ya son dobles por azar, y cada linaje muestra 10 listas.
**I2 casi se cumple sin selección.** No mide composición; la lectura es la doble (co-presencia), contra el piso y contra aza_largo. I1 también es casi trivial:
cap arranca en 6 y la deriva es hacia arriba. Sólo falla si la selección **recorta** el genoma (bloqaza < termo en bloques_pista: las reglas
al azar estorban). Veredicto que espero: **SIN USO 0.60 · PURGADA 0.20 · INDETERMINADO 0.10 · PAGA 0.07 · NO SE LEE 0.03.**

## 5. Control que puede fallar
- **aza_largo:** las mismas tasas y la misma capacidad, sin herencia. Si cap le gana a fab pero aza_largo también, lo que ayuda es el largo o el azar, no la selección de combinaciones.
- **fab:** es la cadena de fábrica, pareada por semilla.
- **Confusión declarada:** cap cambia **dos** perillas a la vez (inicial y p_dup), como lo propuso el ingeniero. Un efecto no se puede atribuir a una sola.

## 6. LA LETRA (por código: `corre_gen.letra`; el arnés la prueba en 14 casos). El orden manda.
- **Validez** (si una falla: NO SE LEE):
  - 0 abortos y 15 cadenas con su prueba;
  - linajes coherentes;
  - **tasas_actúan:** el largo medio de la siembra p0 de cap ≥ el de fab + 1.0, en 5/5;
  - el arnés PASA con los shas actuales.
- **CAPACIDAD PAGA:** cruzan de cap > fab (estricto, pareado) en **≥ 4/5**, **y** cruzan de cap > aza_largo en **≥ 4/5**.
- **CAPACIDAD PURGADA:** largo_med de cap < 4.0 en **≥ 3/5**. La selección recorta el genoma: la capacidad cuesta.
- **CAPACIDAD SIN USO:** largo_med de cap ≥ 4.0 en **≥ 4/5**, sin PAGA. El genoma tiene lugar y la selección no lo usa para cruzar.
- **INDETERMINADO:** cualquier otra cosa válida.
- **Doble (co-presencia)** (descriptivo preregistrado; no cambia el veredicto; en el código se llama `compone`): se cumplen las dos:
  - `doble_siembra` de cap en p9 ≥ 2 × 0.0354 = **0.0708** en ≥ 3/5;
  - `doble_siembra` de cap en p9 > la de aza_largo en ≥ 4/5.
  Mide **co-presencia** de las dos reglas en una lista, no que funcionen juntas; la forma O1 (`es_o1`) se lee aparte, como descriptivo.
- **Potencia y falso positivo (H-G2):** con 5 índices y cruces de 0 a 3 por prueba (fab 11/45 en sentidos_muro), la potencia para un efecto moderado es **baja**.
  Con empates frecuentes, el falso positivo aproximado de PAGA bajo la nula (ganar ≥ 4/5 a fab **y** ≥ 4/5 a aza_largo) es **~1–2 %**.

## 7. Qué decide y qué lo refuta
- **PAGA** → la capacidad era un cuello. La frase "no inventa combinaciones" queda **en suspenso**. Siguiente:
  - réplica confirmatoria cap contra fab;
  - separar las dos perillas (inicial 6 solo; p_dup 0.06 solo).
- **SIN USO** → con lugar para 6 o más reglas, la selección tampoco arma lo que cruza. **No se ve efecto grande en cruzan.** Si además `mutacion` da
  OTRA MONEDA, las dos explicaciones de la junta caen y queda la moneda del pasaje: siembra ponderada por hijos a 100k.
- **PURGADA** → las reglas al azar cuestan y la selección las saca antes de poder combinarlas. Siguiente: capacidad **sin basura**
  (inicial 6 con w = 0, reglas mudas que la mutación puede encender).
- Con SIN USO o PURGADA, y sin doble (co-presencia), en una corrida válida: **no se ve efecto grande en cruzan** (con esta potencia no se descarta un efecto chico).

## 8. Cuatro trampas
1. **Canal simétrico:**
   - cap y aza_largo tienen las mismas tasas, el mismo inicial y las mismas semillas;
   - fab difiere en dos perillas (declarado, sec. 5);
   - los tres brazos pasan por la misma `corre_bp.tarea`.
2. **Acierto sin balancear:** la doble tiene un piso de azar alto (0.035 por lista con n = 6). Por eso nada se lee en absoluto: la doble (co-presencia) exige
   el doble del piso **y** superar a aza_largo. I2 queda firmada como la dio el ingeniero, con la advertencia.
3. **Mundo que se come la comida:** los 9 linajes comparten el anillo. Más reglas pueden cambiar cuánto se muerde y con eso el mundo. Se registra
   `fund_media` y los cruces; no hay medida de anillo nueva.
4. **Sitios fijos:** las letras tienen significado fijo (retina fija, `bloques_pista` §0). Todas las semillas son nuevas. La prueba va en
   semillas distintas de los pasajes.

## 9. Costo y comando
- Humo, un proceso: 6 corridas y 150 000 pasos.
- Explora: 15 × (10 × 25k + 100k) = **5.25 M pasos**. A ~1 ms por paso con pool 2 son **≈ 45–55 min** (cap lleva más reglas por paso).
- Comando (lo lanza el coordinador):
  `python experimentos/organelos/condiciones/genoma/corre_gen.py --explora --pool 2`
- Si se corta: el mismo comando con `--reanuda`.
- Lectura: `--lee datos/explora_<fecha>`.

## 10. Mini-prueba (humo; un proceso; pasaje 635090 y prueba 635190; corrida DESPUÉS de firmar las secciones 1–9; no cuenta)
Hubo 6 corridas y 150 000 pasos en 160 s (≈ 1.07 ms por paso). Carpeta `datos/humo_20260930_171834`. Arnés PASA con los shas actuales. Validez OK.

| brazo | largo siembra p0 | partos p0 | prueba 25k: cruzan · R0 med · fund. media | largo_med | doble linajes | doble siembra p0 |
|---|---|---|---|---|---|---|
| fab | 2.31 | 131 | 2/9 · 0.80 · 36.9 | 2.0 | 0/9 | 0.0 |
| cap | 5.52 | 104 | 0/9 · 0.19 · 31.0 | 5.1 | 0/9 | 0.0 |
| aza_largo | 6.37 | 104 | 1/9 · 0.11 · 43.6 | 6.6 | 3/9 | 0.059 |

Con n 1 no dice nada. Declaro lo que se ve, sin cambiar letra ni predicciones:
- cap **acorta** en un solo pasaje (6 → 5.5, contra +0.04 por parto) y pare menos que fab (104 contra 131). Es una señal hacia PURGADA.
- Las dobles que aparecen están en aza_largo (sin herencia, azar puro: 3/9 linajes, 0.059 por lista ≈ el piso) y no en cap.
  Así se ve en la práctica el piso de azar de I2.
- Costo proyectado del explora: 5.25 M × 1.07 ms / 2 ≈ **47 min**.

## 11. Cambios por auditoría antes de datos (30-sep; auditor: LISTO CON CAMBIOS; ningún dato del explora existía)
Sólo cambia el texto. `corre_gen.py` e `identidad_gen.py` **no se tocaron**: sus shas siguen siendo los que cita `identidad_gen_salida.txt`.
- **H-G1:** ERR-158 usado; ERR-159 va a mutación; el siguiente libre de esta sesión se fija al cierre (JUACO 5 numera desde ERR-160). Está en la cabecera.
- **H-G2:** se declaran la potencia baja y el falso positivo aproximado de PAGA (~1–2 %) en la sec. 6. En la sec. 7, "la capacidad no es el muro" y "la hipótesis del ingeniero cae" pasan a "no se ve efecto grande en cruzan".
- **H-G3:** en el texto, COMPONE pasa a "doble (co-presencia)". La clave del código sigue siendo `compone` y su regla no cambia. `es_o1` se agrega como lectura descriptiva (sec. 2 y sec. 6).
- Las predicciones I1–I3 y K1–K6 (K5 renombrada) y la letra por código **no cambian**. El humo (sec. 10) no se repitió.
