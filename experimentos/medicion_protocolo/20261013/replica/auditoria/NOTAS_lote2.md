# NOTAS lote2 (auditor ciego, solo lectura)

No encontre ni abri ningun CLAVE.csv dentro de lote2. No toque nada fuera de la carpeta del lote ni los archivos de las copias; solo escribi HALLAZGOS_lote2.csv y estas notas. Recalculos hechos con python desde los JSON (sin correr ninguna simulacion).

## Resumen
- Con defecto: r01 (confianza media), r10, r11 (media), r15, r16, r20. Son 6 copias, 9 filas con defecto: r16 lleva una segunda fila de confianza baja (P5 no reportada).
- Limpias: r02, r08, r17, r18.
- Defectos con instrumento confirmado por el prereg y por los datos: r15 (corre_etapa4_v9.py:73), r16 (organismo_v7d.py:69), r20 (mundo_largo_c.py:48). Los de lectura estan en los VEREDICTO (r10, r01). El de r11 es de fecha.

## Que fue facil y que fue dificil
- Lo mas barato y mas util: recalcular a mano desde el JSON las cifras que cita cada VEREDICTO (medianas, conteos pareados, LI) y compararlas con el log. Atrapo r01 y r10.
- Los defectos de instrumento no los delata el sha. En r15, r16 y r20 el sha del script o del organismo que aparece en el log y en el meta del JSON coincide con el archivo actual, y aun asi el codigo contradice al preregistro. Por eso la unica prueba fiable fue leer la linea y contrastarla con el texto del prereg, y despues con los datos (r15: parcial y completa difieren en el JSON, imposible con el codigo actual; r16: W_B en E1 igual al equilibrio local, imposible con decaimiento global). Conclusion: hay que desconfiar del "sha cuadra".
- Lo mas dificil: los instrumentos generados por anclas (organismo_capD, v12m/g, mundo_hija_dispersa, mundo_temporal_v9) son de 150-300 lineas densas; los revise buscando solo las lineas que el prereg describe (kj, umbrales, mascaras, semillas, lam, memoria_rechazo). Un cambio en otra linea (p.ej. un clip, un indice) podria habersele escapado.
- Copias con muchos archivos auxiliares (r10: identidad_v4, regla14_v4, analiza_potencia_v4, CRITERIO) las lei por encima contra el log; no re-derive el bootstrap.

## Lo que no pude verificar sin correr la serie
- Que cada identidad (bit a bit) o cada control de arnes diga la verdad: solo tengo el conteo que escribio el log (42/42, 21/21, 54/54, 16/16...).
- r18: Q1, Q2 y Q5 viven en bateria_v10 y en examen_v10 (no estan en la carpeta). r02/r08: el examen_v8 y coste_techo que usan como referencia tampoco.
- r16: Control 1 (42/42) y el diff de "3 lineas funcionales"; no hay log, solo el JSON.
- r11: el "466 corridas" del VEREDICTO no cuadra con 400+20+3 del runner (426 con 6 de identidad del prereg); lo anoto como duda sin ubicacion firme (baja).
- r15/r16/r20: no puedo decidir si el codigo fue tocado despues de correr o si lo que corrio ya era asi; los datos guardados sugieren lo primero. Si el coordinador quiere distinguir, hay que re-correr.
- r01: la frase de "3 semillas" puede ser conteo distinto; las cifras de error 0.02/0.11/0.16 del diagnostico post-hoc no las pude reproducir con mi particion por estimulo (60k: 0.021, 0.021, +5 -> 0.118, +10 -> 0.157), quedan como lectura exploratoria del autor, no las marque.

## Observaciones sin hallazgo (para ser honesto con lo que dude)
- r08: corre_reverificacion.py:83 usa v < 0.3 y el docstring dice <= 0.3. Recalculado con ambos operadores sobre el JSON: mismas medianas y rangos, asi que sin efecto medible; lo deje como limpio.
- r02: F4 en el runner solo acota por arriba (+10%) mientras el prereg dice +-10%; mismo resultado (+9.9%). El propio VEREDICTO ya lo admite ("por la razon equivocada").
- r10: el sha de CRITERIO_TRONCO_v4.md que cita el log (c529c48f) no es el del archivo actual (b0e3e936); el archivo dice "Estado 23-sep UTILIZABLE" y la calibracion fue el 22-sep, asi que el cambio es esperable. No pude comparar la letra tal como estaba al correr.
- r17: las predicciones secundarias del prereg (retencion <= 10/20 y acierto >= 0.75 en beta=1) no se cumplieron (12/20 y 0.70) y el veredicto no las menciona; eran sin voto.
- r18: la correccion de Q3 (ERR-17) se hizo viendo los datos, pero esta declarada y se re-prueba en semillas nuevas; no la marque.
- r01: G3 REFUTADA es honesta; los tres brazos agotan el pool.

## Tiempo por copia (aproximado, tiempo de reloj de lectura)
- r01: unos 12 min (varias lecturas de JSON). r02: 8. r08: 10. r10: 18 (muchos archivos). r11: 14. r15: 10. r16: 10. r17: 10. r18: 8. r20: 7. Total cerca de 2 h incluyendo el CSV.
