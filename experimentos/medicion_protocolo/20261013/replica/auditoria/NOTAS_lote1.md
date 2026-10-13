# NOTAS lote1 (auditor ciego, 13-oct-2026)

Resultado: 5 copias con defecto (r03, r07, r13, r14, r19), 5 limpias (r04, r05, r06, r09, r12). Ningun defecto de instrumento ni de criterio con umbral cambiado: todos los hallazgos son de lectura/fecha/texto (VEREDICTO o PREREGISTRO contra JSON/log).

## Metodo (por copia)
1. Preregistro contra runner: umbrales, semillas, brazos, kwargs (leidos en el codigo, no inferidos).
2. sha256[:16] de cada archivo contra los shas que el log/JSON registran al arrancar. Coinciden todos (r04, r05, r06, r07, r09, r12, r14, r19, r03 salvo la letra CRITERIO_TRONCO_v4.md, que se edito despues de la serie por el "Estado 23-sep"; r13 preregistro difiere porque se le anadieron la enmienda y el resultado). Esto descarta casi por completo defectos de instrumento/criterio sembrados en codigo o preregistro.
3. Runner contra JSON: recalcule con stdlib las tablas (medianas, conteos pareados, LI de no inferioridad, N*, M_max, retencion, etc.) desde los crudos. Todas cuadran con el log.
4. JSON contra VEREDICTO: linea a linea las cifras. De ahi salen todos los hallazgos.

## Lo dificil
- r13 y r19: el sha del preregistro del segundo run no se pudo reproducir truncando el archivo actual (intente variantes de saltos de linea y de la hora de la enmienda). No se que cambio entre run y archivo actual; no lo tome como defecto.
- r14: el diagnostico exploratorio (error por estimulos tras el agotamiento) depende de una definicion no incluida; mi recalculo solo coincide en el "antes/al agotar" y en el final.
- Distinguir errata de copia (r03 LI -3.478) de defecto sembrado: no tengo como saberlo, reporto la discrepancia contra el JSON.

## No pude verificar sin correr
- Identidades/arneses (42/42, 54/54, 7/7, etc.): la salida del arnes no esta en las carpetas; solo el conteo citado en log/VEREDICTO (punto 2 del auditor; falta la salida en todas).
- Los organismos base (v7, v8, v9, v11, mundo_largo, organismo_v3cal) y los examenes/baterias (Q1, Q2, Q5 de r09; examen_v8 de r07) no estan: no se puede reproducir ningun numero ni la fraccion "diff de N lineas".
- Commits/hashes git y tiempos de pared en VEREDICTO (r03, r05, r06...).
- r03: la funcion no_inferior esta en corre_criterio_v3 (ancla externa); lo recalcule independientemente (media - 1.645*sd/sqrt(80)) y coincide.

## Observaciones sin hallazgo (copias limpias)
- r05: la prediccion secundaria del preregistro (retencion <= 10/20 y acierto >= 0.75 en beta=1; cruce entre 0.30 y 0.75) no se cumple (12/20, 0.70) y el veredicto no la menciona; esta declarada "sin voto", no la conte.
- r06: sin salida del control 1 (42/42) en la carpeta.
- r12/r14: la prediccion numerica (G1 25-40) quedo por debajo de lo medido; veredicto lo trata bien.
- r04: K2 en 60k pasa por 0.5 (11.5 >= 12-1); el veredicto lo declara.

## Hallazgos de baja confianza (se cuentan aparte)
r03 VEREDICTO:23 y :27; r13 VEREDICTO:12 y PREREGISTRO:58; r14 VEREDICTO:33; r19 PREREGISTRO:38.

## Tiempo por copia (aprox., lectura + recalculo)
r03 ~12 min (la mas larga: 2 series, crudos de 1 MB); r04 ~6; r05 ~7; r06 ~6; r07 ~6; r09 ~5; r12 ~5; r13 ~12; r14 ~9; r19 ~7.
Total ~75 min de trabajo. Nunca abri CLAVE.csv ni nada fuera de lote1 (salvo juaco-auditor.md).
