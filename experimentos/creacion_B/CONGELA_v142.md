# CONGELACIÓN v14.2 — textos preparados (NO aplicados)

**v14.2 = v14.1 + B-5 (DESAMBIGUAR CÓDIGOS).** Decisión del director, 18 sep 2026 ~20:40: *"corre las
recomendaciones"* — B-5 entra al tronco como v14.2. Este archivo es el material listo para que **el coordinador**
lo aplique: el bloque de `manifiesto.py`, la línea nueva de la regla 1, la entrada de `REGISTRO_etapas_1_2.md` y
el comando de tag. **Nada de esto está aplicado.** El compilador no edita `manifiesto.py`, no toca `CLAUDE.md`,
no corre la regla 1 (Pool) y no commitea.

---

## 0. Qué se construyó (archivos nuevos, por anclas, sin tocar nada congelado)

| archivo nuevo | sha256_16 | origen (sólo leído) | qué cambia |
|---|---|---|---|
| `organismo/organismo_v142.py` | `17528d767fcebaf6` | `experimentos/creacion_B/organismo_v14_codigo.py` (`a4eeca90fb605c78`) | **sólo** el defecto `desambiguar=0` → `1`, + cabecera |
| `organismo/organismo_v142g.py` | `9e5f566cd6a7a4d2` | `experimentos/creacion_B/organismo_v14g_codigo.py` (`ae9231070a95c801`) | ídem (mundo de regla) |
| `organismo/bateria_v142.py` | `6375d90e531b06e6` | `organismo/bateria_v14.py` (`72216f5415de0c86`, CONGELADA) | módulo examinado + nombres de salida |
| `organismo/bateria_generaliza_v142.py` | `e5929942647756a5` | `organismo/bateria_generaliza.py` (`9cf72581ebae7dea`) | **una** entrada en `INSTRUMENTOS` + `_dir` |

Constructor: `experimentos/creacion_B/construye_v142.py` (tripwire de sha en los cinco orígenes, incluido
`organismo/organismo_v14.py` `feefc88b1fd8d434`; si alguno cambia, no escribe nada).
Arnés: `organismo/identidad_v142.py`. Humo: `experimentos/creacion_B/humo_v142.py`.

**Regla 14 (ERR-38):** la entrada nueva de `bateria_generaliza_v142.py` es **campo a campo** la de
`organismo_v14`, verificado por el constructor contra una cadena esperada antes de escribir:
`('organismo_v142g', dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1))`
— `eta_s`/`clip_s` **explícitos** porque `organismo_v142g`, como `organismo_v14g`, los trae apagados por defecto
(`eta_s=0.0`, `clip_s=3.0`).
**ERR-42:** las dos baterías viven en `organismo/`, así que `AQUI == organismo/` y los sha de `organismo_v11.py`,
`organismo_v10.py`, del organismo y del instrumento se leen de su sitio real; el humo comprueba además que el
JSON **se escribe**.

**Humo (regla 14 ampliada / ERR-42), 2 semillas, UN proceso — las dos baterías LLEGAN A ESCRIBIR SU JSON:**

```
=== HUMO bateria_v142.py 2 --log (un proceso) ===
[20:48:01] === Batería v13 — CRITERIO v3, 2 semillas (1..2) ===
[20:48:01] sha organismo_v13 17528d767fcebaf6  bateria_v13 6375d90e531b06e6  preregistro b46b59b0251ed417
[21:06:28] VEREDICTO bateria_v13: 5_identidad=True 1_cientificos=True 2_celdas=True 3_control=True
           4a_identidad=True 4b_sin_conflicto_no_divide=True 4c_misma_valencia=True 4d_causa=True
[21:06:28] datos -> examen_v142_20260918_204801.json  sha256_16 = a9b54c2ea59e7928
  JSON ESCRITO: ['examen_v142_20260918_204801.json']

=== HUMO bateria_generaliza_v142.py organismo_v142 2 --desde 101 --log (un proceso) ===
[21:06:28] instrumento organismo_v142g 9e5f566cd6a7a4d2  organismo 17528d767fcebaf6  esta bateria e5929942647756a5
[21:07:25]   OK    K  cobertura del primer encuentro: 2/2
[21:07:25]   PASA  G1 valor en patrones nunca vistos: px0 0.950 (>=0.65), azar 0.650, px0>azar 2/2
[21:07:25]   PASA  G2 conducta al primer encuentro: px0 0.921 (>=0.55), azar 0.539, px0>azar 2/2
[21:07:25] *** organismo_v142 CONSERVA la generalización de la Etapa 3
[21:07:25] datos -> regresion_generaliza_organismo_v142_20260918_210628.json  sha256_16 = 7f9eb012535e7602
  JSON ESCRITO: ['regresion_generaliza_organismo_v142_20260918_210628.json']

HUMO v14.2: bateria_v142 JSON OK | bateria_generaliza_v142 JSON OK   (1164s)
```

El humo **no es el examen**: 2 semillas no congelan nada (la propia batería lo dice: *"Congelar sólo con S>=20"*).
Sirve para lo que exige la regla 14: que los instrumentos copiados corran de punta a punta, apunten al módulo y al
instrumento correctos (sha en la cabecera del log) y **escriban su JSON**.

---

## 1. Bloque para `manifiesto.py` (pegar al final de `CONGELADOS`, antes de la llave de cierre)

```python
    # v14.2 = TRONCO desde el 18 sep 2026 (noche; decision del director ~20:40: "corre las recomendaciones").
    # v14.2 = v14.1 + B-5 DESAMBIGUAR CODIGOS (nivel 4, declarado en dos series el 18-sep 09:07 y 09:12): la division
    # por conflicto de signo de v11 se dispara TAMBIEN cuando una celda consolidada (|Wb[c]|>0.2), bajo una retina
    # distinta (kj@P > KW[c]@P), recibe R == 0; la hija nace SIN valor y la madre conserva el suyo. Memoria nueva CERO,
    # constantes nuevas CERO, rng intacto. Lo UNICO que cambia respecto de v14.1 es el defecto de la perilla.
    # En los mundos del tronco R in {+1,-3}: INERTE POR CONSTRUCCION (identidad_v142.py 62/62 exigidas, I5 inercia
    # 30/30; en B-5: examen v3' 8/8 con splits identicos y generalizacion 40/40 identicas a v14.1, coste 0 % exacto).
    # Donde SI actua: el mundo vivo, donde repara el alias de codigo (18/18 semillas ALIAS en dos series:
    # |W[sal]| 0.0, veneno -3.0, evitacion x7 -> x1, muertes 41 contra 75).
    './organismo/organismo_v142.py':          '17528d767fcebaf6',
    './organismo/organismo_v142g.py':         '9e5f566cd6a7a4d2',
    './organismo/bateria_v142.py':            '6375d90e531b06e6',
    './organismo/bateria_generaliza_v142.py': 'e5929942647756a5',
```

Tras pegarlo, `manifiesto.py --check` debe decir **20 archivos congelados** intactos (16 + 4).

---

## 2. Línea nueva de la regla 1 (`CLAUDE.md`, regla de trabajo 1 y bloque de estado)

```
cd organismo && python bateria_v142.py 6 && python bateria_generaliza_v142.py organismo_v142 20 --desde 101
```

Sustituye a la de v14.1 (`python bateria_v14.py 6 && python bateria_generaliza.py organismo_v14 20 --desde 101`),
que pasa a **regresión histórica** junto con v13, v11 y v9.
Añádase `--log` cuando se quiera el JSON en `datos/` (la batería de generalización sólo escribe JSON con `--log`).

---

## 3. Entrada para `registro/REGISTRO_etapas_1_2.md` (al final)

```markdown
### CONGELACIÓN v14.2 (18 sep 2026, noche; decisión del director ~20:40: "corre las recomendaciones"): **B-5 entra al tronco. v14.2 = v14.1 + DESAMBIGUAR CÓDIGOS, con coste 0 % en el tronco por identidad, no por medida**

**Qué es.** La división por conflicto de signo de v11 se dispara **también** cuando una celda consolidada
(`|Wb[c]| > 0.2`), bajo una retina distinta (`kj@P > KW[c]@P`), recibe `R = 0` — ausencia de consecuencia. La hija
nace **sin valor** (no hay signo nuevo que llevarse) y la madre conserva el suyo. Memoria nueva: **cero**.
Constantes nuevas: **cero**. El rng no se toca. Declarado en dos series el 18-sep (B-5 09:07 y réplica 09:12,
semillas ALIAS/LIMPIAS elegidas estructuralmente antes de correr): *"cuando una celda con valor recibe nada bajo
una retina distinta, divide: el código deja de prestar valor"*.

**Qué cambia del tronco: nada más que un defecto.** `organismo_v142.py` es `organismo_v14_codigo.py`
(`a4eeca90fb605c78`, el módulo que ya pasó B-5 y su réplica) con `desambiguar=0` → `desambiguar=1` por defecto.
Ningún número del tronco se movió. En los mundos del tronco `R ∈ {+1, −3}` y la condición `R == 0` **no puede
darse**: la regla es inerte **por construcción**, no por suerte.

**Instrumentos (por anclas; los orígenes sólo se leyeron, con tripwire de sha):**
`construye_v142.py` genera `organismo/organismo_v142.py` (`17528d767fcebaf6`), `organismo/organismo_v142g.py`
(`9e5f566cd6a7a4d2`), `organismo/bateria_v142.py` (`6375d90e531b06e6`, copia de `bateria_v14.py`
`72216f5415de0c86` con las seis etapas, los CRIT y los umbrales del criterio v3′ **intactos**) y
`organismo/bateria_generaliza_v142.py` (`e5929942647756a5`, con **una** entrada nueva en `INSTRUMENTOS`, campo a
campo igual a la de `organismo_v14`: regla 14 / ERR-38, con `eta_s=0.15` y `clip_s=10.0` explícitos). Las dos
baterías viven en `organismo/`, así que todos los sha se leen de su sitio real (**ERR-42**), y el humo
(`humo_v142.py`, dos semillas, un solo proceso con el Pool sustituido por uno en serie) comprueba que **el JSON se
escribe** antes de cualquier serie.

**Identidad (arnés `organismo/identidad_v142.py`, un proceso, T = 30 000 / 120 000): 62/62 exigidas, bloques 3/3.**

| bloque | qué exige | resultado |
|---|---|---|
| I1 | `organismo_v142(desambiguar=0)` ≡ `organismo_v14` (v14.1) en todas las claves, 12 escenarios × 2 semillas | **24/24 idénticos** |
| I2 | el rng NO se consume con la perilla apagada (T = 120 000, 2 semillas) | **2/2 idénticos** |
| I3 | `organismo_v142()` (perilla ON por defecto) ≡ `organismo_v14_codigo_on` (`2f7794d92e68cc89`), 12 × 2 | **24/24 idénticos** |
| I4 | `organismo_v142g(0)` ≡ `organismo_v14g` y `organismo_v142g()` ≡ `organismo_v14g_codigo_on`, 3 reglas × 2 | **12/12 idénticos** |
| I5 (predicción, no exigencia) | con la perilla ON, inercia en los mundos del tronco: `v142()` ≡ `v14` y `v142g()` ≡ `v14g` | **30/30 inerte** |

I3 es lo que hace que **no haya que volver a correr la evidencia de B-5**: el archivo nuevo es, bit a bit, el
archivo examinado en B-5 con otro nombre y el defecto movido. Lo medido allí vale tal cual para v14.2: examen v3′
**8/8** con `splits` por etapa idénticos a v14.1, generalización **40/40 filas idénticas** (G1 1.000, G2 0.967,
K 20/20), **coste 0 % exacto**; y en el mundo vivo, alias reparado en **18/18** semillas ALIAS de dos series
(|W[sal]| 0.0 contra 1.45, veneno −3.0 contra −1.45, exposiciones a la sal 517 contra 3 835 — evitación ×7 → ×1 —,
muertes 41 contra 75, celdas mediana 35 ≤ 45).

**Regla 1 pasa a:** `cd organismo && python bateria_v142.py 6 && python bateria_generaliza_v142.py organismo_v142 20 --desde 101`
(histórica: v14.1, v13, v11, v9). `manifiesto.py --check`: **20** congelados.

**Lo que v14.2 NO es.** No es un candidato bajo el criterio v2 (`CRITERIO_TRONCO_v2.md`): no compite en el mundo
vivo por supervivencia contra v14.1, porque no se propone mejorar el tronco sino **quitarle un defecto que sólo
aparece fuera de él**. Su justificación es exactamente la inversa de la de un órgano: *no cambia nada donde el
tronco vive, y repara el alias donde el tronco iba a vivir*. Los candidatos v15c/v15d/v15e/v15f siguen fuera y no
se rejuzgan (regla 3).

**Pendiente del coordinador:** aplicar el bloque a `manifiesto.py`, actualizar `CLAUDE.md` (tronco y regla 1),
correr la regla 1 completa con Pool (`bateria_v142.py 6` + `bateria_generaliza_v142.py organismo_v142 20 --desde
101 --log`) y `manifiesto.py --check`, commitear y etiquetar. **Mientras la regla 1 no salga toda PASA, v14.1
sigue siendo el tronco.**
```

---

## 4. Comando de tag (tras el commit de congelación)

```bash
git tag -a v14.2-tronco -m "v14.2 = v14.1 + B-5 DESAMBIGUAR CODIGOS: la division por conflicto de signo se dispara tambien cuando una celda consolidada recibe R == 0 bajo una retina distinta; la hija nace sin valor. Memoria y constantes nuevas: CERO. Lo unico que cambia respecto de v14.1 es el defecto de la perilla (desambiguar=1). Inerte por construccion en los mundos del tronco: identidad_v142.py 62/62 (I1 24/24 == v14.1, I2 rng 2/2, I3 24/24 == organismo_v14_codigo_on, I4 12/12) e inercia I5 30/30; examen v3' 8/8 con splits identicos y generalizacion 40/40 identicas (coste 0 % exacto). Repara el alias de codigo en el mundo vivo: 18/18 semillas ALIAS en dos series (|W[sal]| 0.0, veneno -3.0, evitacion x7 -> x1, muertes 41 contra 75). Decision del director 18 sep 2026 ~20:40."
git push origin v14.2-tronco
```

---

## 5. Orden de aplicación sugerido (coordinador)

1. `python manifiesto.py --check` (16 intactos, antes de tocar nada).
2. Pegar el bloque de §1 en `manifiesto.py`; `python manifiesto.py --check` → 20 intactos.
3. Regla 1 con Pool: `cd organismo && python bateria_v142.py 6 --log && python bateria_generaliza_v142.py organismo_v142 20 --desde 101 --log`.
   Regresión histórica: `python bateria_v14.py 6`, `bateria_v13.py 6`, `bateria_v11.py 6`, `bateria_v9.py 6`.
4. Si todo PASA: `CLAUDE.md` (tronco v14.2 + regla 1 nueva), entrada de §3 al registro, commit, tag de §4, push.
5. Si algo falla: **no se congela**, se registra el fallo con ERR nuevo y v14.1 sigue siendo el tronco.
