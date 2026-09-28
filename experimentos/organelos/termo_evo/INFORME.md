# INFORME — TERMO_EVO: ¿la selección encuentra el termostato sola? (nube, 28-sep-2026)

**VEREDICTO: NO por la letra (serie 41001–41020; réplica no se corre).** La selección sí mueve el gen: `g` sube con la herencia y no sube
sin ella. Pero lo hace despacio: en 100 000 pasos la media de los padres va de 0.066 a 0.092 (P3 en 7/20 semillas) y el linaje no cruza
(P1 2/20), porque cada refundación lo devuelve a la zona letal.

Misión: llegar a la AGI por este camino. Encargo `ENCARGO_NUBE.md`; preregistro `PREREGISTRO_termo_evo.md` (commit `e471de9`, antes
del humo y de la serie). Arnés `identidad_evo.py` → **ARNES PASA** (388 s). Humo OK. Auditor (solo lectura): el NO se sostiene por la letra.

## 1. La serie (41001–41020, T 100 000, 9 carros iguales, fundador limpio; 120 corridas, 0 abortos, contabilidad 180/180 en cada brazo)
Resumen: `datos/evo_s41001-41020_T100000_20260928_144525/resumen.json` (sha `9c621d7136731dce`); log `serie_pool3.log`; 7 194 s con Pool 3.

| brazo | qué es | R0 real (mediana) | semillas con mayoría que cruza | linajes que cruzan | fundadores (mediana) | vida (mediana) |
|---|---|---|---|---|---|---|
| v143 | base | 0.611 | 1/20 | 54/180 | 16.0 | 600 |
| **evo** | g heredable, fundador U[−0.10, 0.10], σ 0.03 | **0.309** | **2/20** | 37/180 | 25.0 | 184 |
| sinher | CONTROL: el hijo re-sortea g | 0.184 | 0/20 | 12/180 | 37.5 | 85 |
| ancho | g heredable, fundador U[−0.10, 0.60] | 0.753 | 4/20 | 70/180 | 7.0 | 759 |
| m40 | g = 0.40 fijo (techo diseñado, == HIBB m40) | 0.895 | 11/20 | 89/180 | 2.5 | 1 146 |
| o1 | techo LLM, ancla | 0.941 | 20/20 | 136/180 | 0.0 | 3 118 |

**Pareados** (mediana del R0 real por semilla): evo–sinher **gana 18/20, +0.141** · evo–v143 5/20, −0.297 · sinher–v143 0/20 ·
ancho–sinher 20/20, +0.539 · ancho–v143 13/20, +0.085 · m40–v143 19/20, +0.208 · evo–m40 0/20, −0.547 · o1–v143 20/20, +0.333.

**La letra:** validez V1–V4 **todas True** (O1 gana 20/20; V143 0.611 dentro de [0.40, 0.80]; la pieza actúa en evo y sinher).
Puertas: **P1 False (2/20) · P2 True (18/20) · P3 False (7/20)**. MODESTO exige P3 → **NO**.

## 2. La curva de g (serie, brazo `evo`; 9 linajes × 20 semillas juntos; ventana = 10 000 pasos)
| ventana | g padres: media [q10 q50 q90] (n) | g vivos: media | muertos: hijos por cuerpo | SINHER: g padres media |
|---|---|---|---|---|
| [0, 10k) | 0.066 [0.024 0.065 0.098] (386) | 0.005 | 0.18 | 0.063 |
| [10k, 20k) | 0.071 [0.024 0.067 0.113] (372) | 0.012 | 0.29 | 0.058 |
| [20k, 30k) | 0.077 [0.024 0.079 0.131] (404) | 0.020 | 0.37 | 0.055 |
| [30k, 40k) | 0.074 [0.021 0.072 0.125] (470) | 0.027 | 0.31 | 0.054 |
| [40k, 50k) | 0.076 [0.027 0.075 0.125] (518) | 0.035 | 0.38 | 0.057 |
| [50k, 60k) | 0.080 [0.028 0.075 0.127] (555) | 0.046 | 0.47 | 0.058 |
| [60k, 70k) | 0.080 [0.027 0.075 0.131] (557) | 0.050 | 0.48 | 0.059 |
| [70k, 80k) | 0.083 [0.031 0.078 0.138] (523) | 0.049 | 0.41 | 0.060 |
| [80k, 90k) | 0.093 [0.039 0.093 0.144] (562) | 0.055 | 0.45 | 0.058 |
| [90k, 100k) | **0.092** [0.041 0.089 0.152] (547) | 0.059 | 0.49 | 0.055 |

**Paisaje** (evo, todos los cuerpos muertos; bin de g: cuerpos / hijos por cuerpo / edad media):
−0.10: 2 434 / 0.0 / 764 · −0.05: 2 548 / 0.0 / 1 165 · 0.00: 3 133 / 0.375 / 1 600 · 0.05: 3 347 / 0.647 / 1 510 · **0.10: 454 / 2.27 / 4 120 ·
0.15: 82 / 2.67 / 4 308 · 0.20: 13 / 3.23 / 5 295**. El gradiente es empinado: g < 0 no deja hijos nunca, y g ≥ 0.10 deja 3–5 veces más
hijos que [0, 0.10). Pero casi todos los cuerpos están abajo, porque la mayoría son fundadores recién sorteados en la zona letal.

## 3. La larga (DESCRIPTIVA, sin letra: 41041–41050, T 300 000, evo y sinher; 20 corridas, 0 abortos)
Resumen `datos/evo_s41041-41050_T300000_20260928_164544/resumen.json` (sha `e504b7f891d33b31`); log `larga_pool3.log`; 3 212 s.

| ventana (30 000 pasos) | 0–30k | 30–60k | 60–90k | 90–120k | 120–150k | 150–180k | 180–210k | 210–240k | 240–270k | 270–300k |
|---|---|---|---|---|---|---|---|---|---|---|
| evo: g padres media | 0.075 | 0.085 | 0.096 | 0.103 | 0.100 | 0.105 | 0.110 | 0.110 | 0.122 | **0.121** |
| sinher: g padres media | 0.062 | 0.058 | 0.060 | 0.057 | 0.055 | 0.058 | 0.050 | 0.059 | 0.057 | 0.059 |

- evo: R0 real 0.667 (sinher 0.222); pareado **10/10, +0.407**. Media de g de los padres en la última ventana dentro de [0.10, 0.60] en
  **9/10 semillas** (0.099–0.161). Semillas con mayoría de linajes que cruzan **0/10** (30/90 linajes; ninguna semilla llega a 5 de 9).
- Lectura: la subida no se detiene; sigue a ~0.015 cada 100 000 pasos. Con 3× más generaciones, la condición de P3 se cumpliría
  (fuera de la letra). La de P1 no: `cruza_real` exige 0 fundadores después de t = 10 000, y el refundador vuelve a la zona letal (D2).

## 4. Lectura post-hoc (NO preregistrada; `lee_posthoc.py`; auditoría H-6; sesgo de supervivencia declarado)
"Establecido" = 0 fundadores después de t = 10 000.

| | serie evo | serie sinher | serie ancho | larga evo | larga sinher |
|---|---|---|---|---|---|
| linajes establecidos | 66/180 | 33/180 | 109/180 | 33/90 | 9/90 |
| R0 real (establecidos) | 0.922 | 0.824 | 0.947 | 0.983 | 0.903 |
| g padres, última ventana (establecidos / no establecidos) | 0.086 / 0.076 | 0.045 / 0.057 | 0.392 / 0.447 | 0.109 / 0.095 | 0.065 / 0.055 |

Esto matiza la pregunta del encargo:
- **Una vez que arranca, casi cualquier g > 0 vive.** Hasta SINHER tiene linajes establecidos con R0 0.82 y g ≈ 0.05.
- La "banda" (≥ 0.10) salió del exploratorio con margen 0 contra 0.10 (m0 contra m10), y no hace falta para sostener un linaje ya
  establecido.
- Lo que la herencia gana sobre el control es **establecer más linajes**, no un g mucho mayor dentro de ellos: 66 contra 33, y
  fundadores 25 contra 37.5.
- **El muro de P1 es el refundador, no el termostato.**

## 5. Predicciones (§8 del preregistro) contra el resultado
| # | predicción | resultado | ¿se cumple? |
|---|---|---|---|
| E1 | V143 en [0.35, 0.70] | 0.611 | sí |
| E2 | O1 17–20/20 | 20/20 | sí |
| E3 | M40 [0.85, 0.97] / 10–17 | 0.895 / 11 | sí |
| E4 | EVO [0.55, 0.92] | 0.309 | **no** |
| E5 | EVO–SINHER ≥ 15/20 y dif [+0.15, +0.50] | 18/20, +0.141 | **no** (por 0.009 en la diferencia) |
| E6 | P3 ≥ 15/20 | 7/20 | **no** |
| E7 | g padres pooled, última ventana [0.12, 0.35] | 0.092 | **no** |
| E8 | SINHER ≤ 0.45 | 0.184 | sí |
| E9 | EVO 3–12/20 con mayoría | 2/20 | **no** |
| E10 | paisaje: g < 0 ≤ 0.05 hijos; [0.10, 0.15) > [0, 0.05) | 0.0; 2.27 > 0.375 | sí |
| E11 | M40 gana a EVO ≥ 15/20 | 20/20 | sí |
| E12 | ANCHO en banda y R0 > EVO | 0.414; 0.753 > 0.309 | sí |
| V | serie FUNCIONA / MODESTO / NO / NO SE LEE = 0.15 / 0.45 / 0.25 / 0.15 | NO | – |

Error de fondo en mis predicciones: sobreestimé la velocidad. Supuse que en 100 000 pasos la selección subiría la media de g por
encima de 0.12; subió a 0.09. No tuve en cuenta que la mayoría de los partos vienen de linajes que se acaban de refundar.

## 6. Decisiones difíciles (sesión de nube, 28-sep; hora, opción tomada, alternativa descartada y porqué)
- **~14:05 · D1, unidad heredable = el cuerpo, por el canal `al_parir` → cola → `nace`.** La pista ya lo permite y no se toca.
  *Descartado:* heredar por linaje-carro, que da una sola g por linaje y no hay selección entre cuerpos.
- **~14:05 · D2, el refundador sortea de la distribución inicial.** Lo impone la ENMIENDA 5: nada del objeto viejo pasa.
  *Descartado:* que el refundador herede la g del linaje, porque violaría el fundador limpio y la pista.
  Es la causa principal de que P1 no se cumpla, y quedó declarada antes de correr.
- **~14:10 · rng del gen = `ctx['rng'].spawn(1)[0]`.** No avanza el rng del cuerpo (arnés (d)).
  *Descartado:* sortear del rng del cuerpo, porque cambiaría la física de V143 y rompería la identidad con m40.
- **~14:15 · D4, m40 como carro EVO degenerado.** Así el techo corre por el mismo código que el candidato (arnés (b)).
  **D5, sin SINHER del brazo ancho**, por presupuesto; ancho queda descriptivo.
- **~14:20 · D7, telemetría del gen en un dict de módulo de solo escritura (`_TEL`).** La ENMIENDA 5 cambia la instancia en cada
  refundación, y `d['carro']` sólo ve la última.
- **~16:45 · Serie NO → no hay réplica** (§7). **Sí la larga descriptiva**, porque ya estaba prevista y respondía lo único abierto:
  ¿es lentitud o techo? *Descartado:* correr la réplica "por si acaso", que la regla prohíbe.
- **~17:00 · Auditoría H-6:** la lectura de "linajes establecidos" era post-hoc y no estaba versionada. Se versionó
  (`lee_posthoc.py`, `posthoc_serie.txt`, `posthoc_larga.txt`) y se marca como no preregistrada.
  No se abre un ERR: no se cambió ningún umbral ni se usó como puerta.

## 7. Errores de instrumento declarados
- **Ninguno nuevo. ERR-149 sigue libre.** Hallazgos del auditor, todos menores o de matiz:
  - H-1: la prueba de práctica D6 se vio antes del preregistro, y está declarada.
  - H-2: monkeypatch de `P.run` en el worker; es serial, así que es seguro.
  - H-3: la identidad bit a bit no se probó a T 100 000; se extrapola desde T ≤ 20 000.
  - H-4: la trampa "sin partos = no cumple" no se materializó; todas las semillas tienen n ≥ 14.
  - H-6: arriba, en §4.
- **Declarado:** en `corre_evo.py`, la LARGA pasa por `lee_serie`, pero su veredicto se reemplaza por DESCRIPTIVA. La "letra" que
  imprime su log (V1–V3 False, P3 9/10, modesto True) **no cuenta**.

## 8. Qué propongo (para el coordinador; no se construyó nada)
- La pregunta "¿la selección encuentra el termostato?" tiene respuesta **sí, lentamente**. Lo que la frena en esta pista es el
  **refundador que olvida**, no la falta de gradiente.
- Siguiente peldaño natural, con preregistro nuevo: medir en **JUACO-ECO** (sin refundador de la ENMIENDA 5, con población real), donde
  una g heredada no se pierde con la extinción de un linaje.
- En la pista, la única salida sin tocar la ENMIENDA 5 sería un fundador que parta de una distribución más ancha: eso es ANCHO, que ya da
  0.753 y 4/20. Pero entonces el diseño elige la banda de partida, y deja de ser "la evolución lo encuentra sola".

## 9. Línea para CLAUDE.md
> 28-sep-2026 (nube): **TERMO_EVO = NO** por la letra (41001–41020): el margen del termostato como gen heredable sube con herencia y no sin
> ella (padres 0.066 → 0.092 en 100k; 0.075 → 0.121 en 300k, descriptiva; EVO gana a SINHER 18/20 y 10/10), pero el linaje no cruza
> (P1 2/20, P3 7/20): el refundador de la ENMIENDA 5 vuelve a la zona letal. Sin ERR nuevos (siguiente libre ERR-149). `experimentos/organelos/termo_evo/INFORME.md`.

## 10. Archivos
`ENCARGO_NUBE.md` · `PREREGISTRO_termo_evo.md` · `construye_evo.py` (6cdd7dd10e9a0594) · `carros/V143_EVO_{BAJO,SINHER,ANCHO,M40}.py` ·
`corre_evo.py` · `identidad_evo.py` + `identidad_evo_salida.txt` · `humo_salida.txt` · `serie_pool3.log` · `larga_pool3.log` ·
`lee_posthoc.py` + `posthoc_serie.txt` + `posthoc_larga.txt` · `datos/` (humo, serie, larga).
Reproducir: comandos en §11 del preregistro; `python lee_posthoc.py datos/<carpeta>`.
