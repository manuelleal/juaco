# HALLAZGO EXTERNO — el mundo de la fase 10 (tres brazos en JUACO-EXO, 21-sep-2026). HIPÓTESIS, NO DATO

**Misión:** llegar a la AGI por este camino; lo externo se cita, no se obedece (regla 8 de EQUIPO).
**Origen:** `C:\Users\User\Documents\PROYECTOS\JUACO-EXO\equipos\fase10\` (rama `autonomo-fase3-4` de alefast). Copias de los archivos de
origen en `experimentos/nivel10_mundo_acumula/externo/` (F0 entero; F1 informe, registro, preregistro, runner, humo, sonda del ancla; la
evaluación). Integración y verificación en el repo: `experimentos/nivel10_mundo_acumula/INFORME_INTEGRACION.md` (22-sep).

## Cifras externas (tal como las declaran; ninguna entra al REGISTRO por sí sola)
| afirmación | cifra externa | archivo de origen | ¿verificada o reproducida en el repo? |
|---|---|---|---|
| arnés de identidad de F0 | 79/79 | `externo/F0_fable_solo/identidad_mundo_fase10_salida.txt` | **SÍ**: 79/79 con la letra de F0 y 79/79 con la ENMIENDA 1 |
| 15 shas de anclas (origen + 7 cadena + 7 donantes) | verificados | `externo/F0_fable_solo/construye_mundo_fase10.py` | **SÍ**: tripwire pasa y aborta si se altera un sha; `mundo_fase10.py` regenerado byte a byte (`84e97674f709a900`) |
| humo F0: RENACE 0.063, NADA 0.085, REL 0.046/0.065, ORÁCULO 0.058, ORÁCULO_SIN_MAPA 0.086 | — | `externo/F0_fable_solo/datos_humo/mundo_fase10_humo_20260921_203032.json` (`41667be59f5a5b79`) | no se rehízo (semillas 1–2; no hacía falta) |
| humo F1: NADA 0.111, INMORTAL 0.915, REL 0.503, MAPA 0.237/0.294, NODO_BARAJADO 0.245 | una semilla | `externo/F1_fable_poderes/mundo_fase10_humo_20260921_201914.json` (`b4cdef09e840a3fe`) | instrumento de F1 no integrado |
| la calibración de F1 conserva el ancla §2.1.6 | RENACE 0.90 [0.36–5.60], NADA 0.30 (4 semillas, T 40 000) | `externo/F1_fable_poderes/sonda_ancla_cambio_salida.txt` | **NO se transfiere** al instrumento de F0: RENACE 0.306 / 0.214 (s5, s6) |
| H-BOCA: la boca lee sólo la fila de la necesidad activa; inmortal muerde veneno con SED 57/63 y sal con HAMBRE 85/259 (F10); 75/83 y 101/508 (tronco) | — | `externo/F0_fable_solo/REGISTRO.md` 20:08 (sin script ni JSON de origen) | **REPRODUCIDO en dirección** (otras cifras, otras semillas/config): tronco 63/84 vs 2/763 con HAMBRE; F10 literal 60/68; sin cambios 71/79 |
| el conocimiento heredado llega (cobertura 0.94/0.69 vs 0.50 NADA; J 0.43 vs 0.03) | — | F0 humo; F1 humo | parcial: `lect_div > 0` (HH2) sí; coberturas del humo del repo 0.625–0.81 vs NADA 0.25–0.5 (n = 1) |
| el mapa de nivel 6 no sirve como canal del DÓNDE | ORÁCULO 0.058 vs 0.086; MAPA 0.237 vs REL 0.503 | F0 y F1 humos | **consistente en dirección**, n = 1 por par: ORÁCULO 0.188 vs 0.265; REL 0.102 vs REL_SIN_MAPA 0.222 |
| con retina vacía el cuerpo casi no se mueve (p ≈ 0.005) | — | `externo/F0_fable_solo/REGISTRO.md` 20:08 | **no verificado** |
| "cambiar la boca" es el candidato (decisión 1 de §6) | — | `externo/_evaluacion/PARA_JUACO_mundo_fase10.md` | sonda del repo: el veto quita el mordisco (63/84 → 2/224) pero **hunde al inmortal del mundo del tronco** (R₀ 1.15 → 0.05): la boca no es el muro por sí sola |

## Qué entra al REGISTRO (propuesta; el coordinador decide)
Sólo lo verificado o reproducido: tripwire y arnés (dos veces 79/79), humo de la ENMIENDA 1 (ancla NO conservada), diagnóstico H-BOCA
(reproducido en dirección) y la sonda boca2 como resultado de un proceso (no declarado, n = 1). Las cifras de las columnas "cifra externa"
quedan aquí como procedencia.
