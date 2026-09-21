# Auditoría de ERR-29 → **ERR-87** — `corre_baterias_v13D.py` y `corre_baterias_v13E.py` (18 sep 2026, tarde; auditor externo; numerado y commiteado por el coordinador el 21 sep)

## 1. Veredicto registrado: NO cambia (verificado contra los JSON, no asumido)

Corrida registrada `datos/baterias_v13D_20260918_012145.json` (semillas 101–120, no humo):

| archivo del mismo arranque | módulo | fecha | veredictos |
|---|---|---|---|
| `regresion_generaliza_organismo_v13D_on_20260918_012533.json` | organismo_v13D_on (ON) | 01:26:17 | K=True, G1=True, G2=True |
| `regresion_generaliza_organismo_v13D_20260918_012617.json` | organismo_v13D (OFF, referencia) | 01:27:00 | K=True, G1=True, G2=True |
| `baterias_v13D_..._012145.json` → `V['GENERALIZACION']` | (el que quedó) | 01:27:00 | K=True, G1=True, G2=True |

Números del log (`baterias_v13D_20260918_012145.log`): ON → K 20/20, G1 px0 0.800 (19/20), G2 0.834 (19/20);
OFF → K 20/20, G1 px0 0.800 (18/20), G2 0.892 (20/20). Los dos lados pasan los tres subcriterios, así que
`D2_generalizacion = True` es correcto sea cual sea el JSON que se leyó. Lo que entró a PROPUESTA_v14.md (fila
"generalización (v13D, perilla ON)": 0.800/19-20, 0.834/19-20) son los números ON del log, correctos.
No hay ERR nuevo por cambio de veredicto (regla 11 no se dispara).

## 2. Segundo defecto en la misma línea (no cubierto por la corrección de ERR-29 ya commiteada, 1e2d7a6)

`lee_json(pref)` usaba `startswith(pref)` y se quedaba con el ÚLTIMO por orden de nombre. Como
`regresion_generaliza_organismo_v13D_` es prefijo literal de `regresion_generaliza_organismo_v13D_on_` y `'o' > dígito`,
la etapa 3b (OFF) devolvía el JSON de la ON. Consecuencias:

- En la corrida registrada, la etapa 3b releyó el JSON ON (012533); el JSON OFF (012617) nunca entró a `V`.
  Por ese segundo accidente, lo guardado bajo `V['GENERALIZACION']` es literalmente el veredicto ON.
- Con la corrección commiteada (claves `D2`/`D2_ref`), `D2_ref` habría seguido leyendo el archivo ON: la referencia
  OFF nunca quedaría registrada en el JSON de baterías.

Corrección aplicada en `corre_baterias_v13D.py` (sin commit, pendiente de revisión del coordinador):
- `lee_json` exige `prefijo + AAAAMMDD_HHMMSS.json` exacto (regex) y devuelve `(json, nombre)`.
- Cada etapa guarda `archivo` y `modulo` leídos en `V[clave]` (trazabilidad).
- Aviso en el log si el JSON leído es anterior al arranque de la etapa (la batería no escribió el suyo).

Verificación mecánica (sin lanzar Pool: el coordinador tenía `corre_familias_b5.py` con Pool(14) vivo, pid 24300, y
bajo `--humo` las dos baterías siguen abriendo Pool(14) cada una): `py_compile` limpio; `lee_json` sobre `datos/` real
devuelve ahora 012533 para el prefijo ON y 012617 para el OFF; simulación del bucle de etapas con `subprocess.run`
sustituido → `D2` y `D2_ref` leen archivos distintos y `D2_generalizacion` = True. Falta un `--humo` real cuando no
haya otro Pool corriendo.

## 3. Mismo riesgo en `nivel9_probar_si_mismo/corre_baterias_v13E.py` (no tocado)

Su `lee_json` es el mismo `startswith`. El prefijo `regresion_generaliza_organismo_v13E_` también casa
`regresion_generaliza_organismo_v13E_k3_*` y `..._k5_*` (existen desde 03:09/03:24), y `'k' > dígito`: si se vuelve a
correr el runner E, `E2` leería el JSON k5 en vez del de `organismo_v13E`. Las corridas E ya hechas (02:04–02:36) son
anteriores a los archivos k3/k5, así que no las afecta. Sugerencia: copiar la misma `lee_json` con regex.
