# VEREDICTO — Medición del protocolo con errores sembrados (13-oct-2026)

**HAY ALGO MODESTO.** El auditor de sólo lectura atrapa casi todo lo que está en el código y poco de lo que está en la letra del criterio, y da más falsas alarmas de las predichas.

Preregistro: `PREREGISTRO.md` (commit 2d1eb41e, antes de sembrar). Clave sellada: `siembra/CLAVE.sha256` = 237bbfa1…; abierta sólo después de los seis lotes y coincide (`auditoria/PUNTAJE.md`).

## Números (60 copias: 40 con defecto, 20 limpias)

| Medida | Resultado | Wilson 95 % | Predicción | ¿Se cumplió? |
|---|---|---|---|---|
| Sensibilidad total | 28/40 = 0,70 | 0,55–0,82 | P1: 0,40–0,70 | En el borde superior |
| Criterio | 7/18 = 0,39 | 0,20–0,61 | P2: instrumento > criterio | Sí |
| Instrumento | 15/16 = 0,94 | 0,72–0,99 | | |
| Lectura / otro | 6/6 = 1,00 | 0,61–1,00 | | |
| Falsas alarmas (limpias con alarma alta o media) | 6/20 = 0,30 | 0,15–0,52 | P3: ≤ 3/20 | **NO** |

## Decisiones, según los criterios escritos antes

- Instrumento ≥ 0,50: el auditor **sí cuenta** como control para errores de instrumento.
- Criterio 0,39: no alcanza 0,70; el auditor **no basta** para errores de criterio. Ese es el tipo más frecuente del registro (53 de 126).
- Falsas alarmas 6/20 > 5/20: **el formato de hallazgos cambia**: "dato que confirma" obligatorio antes de contar. Cruza el umbral por UNA copia, así que, por la regla de réplica del preregistro, esta decisión queda **pendiente de réplica** con 20 copias nuevas (semilla 20261014).
- No se cumple "≥ 0,70 en todos los tipos": no es FUNCIONA. Total ≥ 0,30: no es NO.

## Lo que esto cambia en el protocolo

1. Los chequeos de instrumento (kwargs, comparadores, qué JSON lee el runner) ya los atrapa la lectura; pasarlos a código (fase 2) es un refuerzo, no un rescate.
2. Los errores de criterio necesitan otro control: cotejo automático preregistro ↔ runner (umbrales, semillas, controles) antes de correr. Es lo que el auditor no vio en 11 de 18 casos.
3. El formato de hallazgos exige dato que confirma; la pregunta espejo (punto 9 del auditor, añadida el 12-oct) no evitó las falsas alarmas.

## Limitaciones (declaradas antes o encontradas durante)

- **Las copias limpias traen errores reales de los bloques originales.** El sembrador avisó, antes de auditar, de al menos tres (criterio_v4: LI de otro brazo citado en el veredicto; bug01: "3 decimales" con datos a 2; hija_dispersa: sha del preregistro no coincide con el JSON). Varias de las 6 falsas alarmas apuntan a esas copias. Según el preregistro cuentan como falsas alarmas; recontarlas excluyéndolas NO está preregistrado y no se hace aquí.
- **ERR-196 (procedimiento):** el preregistro no previó que seis copias del mismo bloque, lado a lado, delatan el defecto por comparación. Antes de auditar se repartieron en seis lotes de diez, una copia por bloque, fuera del repositorio, y cada lote lo auditó un agente distinto. Cambio de montaje anterior a los datos; se numera igual.
- **ERR-197 (criterio de puntaje):** el acierto se cuenta por archivo. En un defecto de criterio sembrado sólo en el preregistro, un auditor que señale el runner con el umbral viejo cuenta como fallo (ocurrió en c34). Se deja como está; se corrige en el siguiente preregistro.
- Los defectos los sembró un agente Claude y los auditó otro Claude. Sesgo compartido posible; se repetirá con otra familia cuando esté conectada.
- Los sha de logs y JSON se resellaron en la siembra; cuatro auditores notaron que por eso el hash no sirve para distinguir alterado de limpio. Es realista (un error de instrumento no cambia el hash de su propio resultado), pero quita una pista que en el repo real sí existe.
- Un solo proyecto, un solo auditor por lote, sin tiempo medido por copia (las notas lo estiman).

## Qué sigue
Réplica de la decisión sobre falsas alarmas: 20 copias nuevas (semilla 20261014), mismo sembrador, lotes de una copia por bloque, formato de hallazgos sin cambios. Después, fase 2 del plan: cotejo preregistro ↔ runner en código.

Siguiente ERR libre: ERR-198.

---

# RÉPLICA (13-oct-2026, noche) — 20 copias nuevas, semilla 20261014

**La decisión sobre falsas alarmas SE CONFIRMA: 3 de 7 limpias (0,43 [0,16–0,75]) con alarma alta o media; cruza el umbral otra vez y por más de una copia.** El formato de hallazgos cambia: "dato que confirma" obligatorio antes de contar.

Clave de la réplica: sha 370fb5ad… en `replica/siembra/CLAVE.sha256`; abierta tras los dos lotes y coincide (verificado a mano; `puntua.py` compara contra el sello de la primera siembra por ruta fija y por eso imprime "NO COINCIDE": defecto del script, ERR-198, no de la clave).

| Medida (réplica) | Resultado | Wilson 95 % |
|---|---|---|
| Sensibilidad total | 7/13 = 0,54 | 0,29–0,77 |
| Criterio | 2/6 = 0,33 | 0,10–0,70 |
| Instrumento | 3/5 = 0,60 | 0,23–0,88 |
| Lectura | 2/2 | 0,34–1,00 |
| Falsas alarmas | 3/7 = 0,43 | 0,16–0,75 |

La réplica se preregistró sólo para la decisión de falsas alarmas; las sensibilidades de la réplica son descriptivas y más bajas que en la serie (instrumento 0,60 contra 0,94), con intervalos anchos por n pequeño. Juntando serie y réplica, de forma descriptiva y NO preregistrada: total 35/53 = 0,66; instrumento 18/21 = 0,86; criterio 9/24 = 0,38; falsas alarmas 9/27 = 0,33.

Lectura final: el auditor de sólo lectura es un control útil para errores de instrumento y de lectura, insuficiente para errores de criterio, y ruidoso. Los dos sembradores avisaron, antes de cada auditoría, de errores reales en los bloques originales que las copias limpias arrastran; parte de las falsas alarmas son eso, y se cuentan como falsas alarmas porque así se escribió.

Errores reales sin numerar encontrados de paso en bloques cerrados (a registrar después del 15-oct): criterio_v4 (veredicto cita el LI de otro brazo), bug01 ("3 decimales" con datos a 2), hija_dispersa (enmienda fechada antes de los resultados que cita; cita 0.221 cuando la tabla da 0.195; sha del preregistro no coincide con el JSON), v10 (Q2 confirmada en las mismas semillas de la exploración), capacidad_grande (G1 ≥ 20 igual al techo viejo).

Siguiente ERR libre: ERR-199.
