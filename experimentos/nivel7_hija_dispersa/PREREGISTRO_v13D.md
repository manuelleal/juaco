# v13D — ¿la HIJA DISPERSA puede ser un órgano del TRONCO? Prueba de NO REGRESIÓN (retención y generalización)

**Escrito ANTES de correr, 18 sep 2026.** Es el paso §6 de `PREREGISTRO_hija_dispersa.md`: la hija dispersa por
relevancia ya **compone mejor con menos celdas** en el mundo de historia (serie 61–80 con enmienda 1 y réplica
81–100: `celdas` ≤ 0.75×V13 en 19/20 a k = 5 y 18/20 a k = 4, `lift_q4` 0.352 > V13 en 19/20, `sep` 3.62 con
C3 − C3C ≥ 1 en 20/20, REL > AZAR 16/20, SLOT 4/20, inercia a k = 1 20/20). Eso la valida **como órgano de
experimento en su mundo**. Para que pueda entrar al tronco falta lo que exige ERR-20: que **no rompa** lo que v13 ya
tiene cerrado.

## 1. Qué se prueba, y qué NO

Esto es una prueba de **NO REGRESIÓN**, no una demostración. En el mundo del tronco la retina tiene **6 píxeles y un
solo objeto**: no hay distractores, no hay nada irrelevante que ignorar. **Se espera que la máscara sea inerte o casi
inerte**, exactamente como lo fue a k = 1 en 3T-k (donde salió idéntica bit a bit, 20/20). Si la hija dispersa
cambiara mucho aquí, sería mala señal, no buena.

## 2. Instrumentos (por anclas; ningún original tocado)

| archivo | origen (solo lectura) | sha origen | sha generado |
|---|---|---|---|
| `organismo_v13D.py` | `organismo/organismo_v13.py` **(CONGELADO)** | `cc8b16b492d4d324` | `dd380dada0b72bac` |
| `organismo_v13Don.py` (perilla fija ON) | `organismo_v13D.py` | — | `1dd131dc0298307d` |
| `organismo_v13gD.py` | `experimentos/v13_dos_vias/organismo_v13g.py` | `2a80e125f8593bf2` | `0789c4010b8160b0` |
| `bateria_v13D.py` | `organismo/bateria_v13.py` **(CONGELADA)** | `1a027bcb37eb536e` | `c4467ed7838d027c` |
| `bateria_generaliza_D.py` | `organismo/bateria_generaliza.py` | `46772f5a582872c8` | `ebc6010ce8a16b50` |

Constructor único: `construye_v13D.py` (`e85a494d96e00ba5`). Las dos baterías son **copias por anclas**: cambian el módulo
que importan y las rutas (viven fuera de `organismo/`); **las seis etapas, los `CRIT` importados, los umbrales del
criterio v3' y los criterios G1/G2/K quedan INTACTOS**, y los originales no se modificaron.

**Identidad obligatoria** (`identidad_v13D.py`): con `mask_rel = 0`, `organismo_v13D` es `organismo_v13` **bit a bit**
(3 escenarios × 3 semillas), `organismo_v13gD` es `organismo_v13g` bit a bit (2 reglas × 3 semillas) y
`bateria_generaliza_D.py organismo_v13D 3` da lo mismo, línea a línea, que la batería original sobre `organismo_v13`.
**Si no da 16/16, el bloque no corre.**

> **Trampa de instrumento hallada en el humo de B-2 y anotada aquí:** `experimentos/v13_dos_vias/` contiene **su
> propio** `organismo_v13.py` (`88c3574cf9cf38bf`), **distinto** del tronco congelado (`cc8b16b492d4d324`). Cualquier
> runner que ponga esa carpeta antes que `organismo/` en `sys.path` importa el organismo equivocado y su identidad
> falla sin motivo. En este paquete `organismo/` va primero, siempre.

## 3. El mecanismo (el mismo de B-1, sin cambiar una constante)

`kj = clip(KW[c]·0.95 + paso·dist, 0, 5) · rel` con
`rel[i] ⟺ P[i]>0 ∧ ( |m̂p[i]−m̂n[i]| > δ_s ∨ min(m̂p[i],m̂n[i]) > 1−δ_c )`, con `m̂p = mup[c]/zp[c]`, `m̂n = mun[c]/zn[c]`
medias de `P` condicionadas al **signo de R** (EMA con normalizador, `ema_c = 0.05`). `δ_s = δ_c = 0.25`, **los
mismos de B-1**; no se barren ni se ajustan aquí. Memoria: dos vectores de 6 y dos escalares por celda.

## 4. Diseño

Un solo runner, `corre_baterias_v13D.py`, con la perilla **ENCENDIDA**, sobre las semillas del examen de congelación
de v13 (**101–120**, las de ERR-21):

1. **IDENTIDAD** (perilla apagada ≡ v13, 3 semillas). Si falla, aborta.
2. **RETENCIÓN:** `bateria_v13D.py 20 --desde 101 --log` — el examen **criterio v3'** completo (las seis etapas,
   E1/E2/E2I/E2J/E2K/E2L, celdas ≤ 45, 3'/3'', 4a'–4d).
3. **GENERALIZACIÓN:** `bateria_generaliza_D.py organismo_v13D_on 20 --desde 101 --log` — G1, G2 y K sin tocar.
4. Referencia con la perilla **apagada** en las mismas semillas, para comparar contra el registro de v13
   (`examen_v13_20260917_165859`, `regresion_generaliza_organismo_v13_20260917_170148`).

Las baterías se lanzan como **subprocesos secuenciales** (cada una abre su propio `Pool(14)`): un solo `Pool` a la
vez, regla 11.

## 5. Predicción numérica

- **D1 (retención).** `bateria_v13D` cumple el **criterio v3' completo** en 101–120: los ocho veredictos en `True`
  (5_identidad, 1_cientificos, 2_celdas, 3_control con 3' ≤ 1/20 y 3'' ≥ 19/20, 4a', 4b, 4c, 4d).
- **D2 (generalización).** `bateria_generaliza_D` con la perilla encendida: **G1 ≥ 0.80** y **G2 ≥ 0.85** (los valores
  registrados de v13 en 101–120: G1 px0 0.800 / azar 0.500 / px0 > azar 18/20; G2 px0 0.892 / azar 0.458 / 20/20), y
  **K** con cobertura ≥ 6 en ≥ 90 % de las semillas.
- **D3 (inercia esperada).** Divisiones y celdas con la perilla encendida dentro de **±10 %** de las de la perilla
  apagada en las mismas semillas: en un mundo sin distractores la máscara no debería tener casi nada que quitar.

## 6. Cláusula de refutación (escrita antes)

**Si cae la generalización (G1 < 0.80 o G2 < 0.85) o la retención (cualquier veredicto del criterio v3' en `False`),
la hija dispersa se queda como ÓRGANO DE EXPERIMENTO —validada en el mundo de historia, donde compone mejor con menos
celdas— y NO entra al tronco.** No se recalibra `δ_s`, `δ_c` ni `ema_c`: se registra el fallo, y si hay un mecanismo
nuevo se preregistra aparte con semillas nuevas (precedente ERR-21).

Si D1 y D2 pasan **y** D3 muestra que la máscara casi no actúa aquí, lo declarable es: *"la hija dispersa no daña la
retención ni la generalización del tronco; su efecto está donde hay algo irrelevante que ignorar"* — y entonces, y
sólo entonces, tiene sentido preguntar si v14 = v13 + hija dispersa, con su propio preregistro de congelación.
