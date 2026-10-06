# INFORME — reflejo de clic y cuarentena del clic irreversible (5-oct-2026)

**VEREDICTO: HAY ALGO MODESTO — el reflejo de clic NO (el 1-NN lo iguala o lo supera); la cuarentena del clic irreversible sí aguanta: 0 irreversibles errados en 2 071 propuestas.** La línea NO se cierra por el criterio preregistrado (el 1-NN gana 1 de 3, no 3 de 3), pero lo único que queda en pie es la parte 2.

Simulador numpy propio, 6 familias, 5 demostraciones por familia, semillas 11–15, 120 tareas por régimen y semilla, pantallas de 8–24 elementos. Preregistro escrito antes de correr (`PREREGISTRO.md`).

## Parte 1 — tareas completas (media de 5 semillas; entre paréntesis, semillas en que la colonia queda por delante de ese rival)

| régimen | macro posición | macro etiqueta | 1-NN | 1-NN reciente | logística | **colonia** | barajada (control) | colonia_v2 (explor.) |
|---|---|---|---|---|---|---|---|---|
| sin cambio | 1.000 (0) | 1.000 (0) | 1.000 (0) | 1.000 (0) | 1.000 (0) | **1.000** | 0.967 (1) | 1.000 |
| reordenar | 0.003 (5) | 1.000 (0) | 0.375 (5) | 0.375 (5) | 1.000 (0) | **0.632** | 0.860 (0) | 0.423 |
| renombrar | 1.000 (0) | 0.000 (5) | 0.902 (0) | 0.902 (0) | 0.113 (5) | **0.255** | 0.102 (5) | 0.887 |
| distractores | 0.013 (5) | 0.710 (4) | 0.872 (0) | 0.873 (0) | 0.872 (0) | **0.758** | 0.838 (1) | 0.880 |
| cambia-y-vuelve | 1.000 (0) | 1.000 (0) | 0.433 (5) | 1.000 (0) | 1.000 (0) | **1.000** | 0.800 (3) | 1.000 |

## Parte 2 — irreversibles, conjunto primario (5 regímenes honestos + mentiroso inconsistente; suma de 5 semillas)

| brazo | irreversibles errados | semillas con 0 | se abstiene (de las propuestas irreversibles) | completas sin ayuda | completas o con ayuda |
|---|---|---|---|---|---|
| colonia sin cuarentena | 14.88 % (270/1814) | 0/5 | 0 % | 0.630 | 0.630 |
| **cuarentena** | **0.00 % (0/2071)** | 5/5 | 35.0 % | 0.602 | 0.792 |
| cuarentena sin célula de efecto | 1.93 % (40/2071) | 0/5 | 25.8 % | 0.644 | 0.781 |
| cuarentena sin k=2 | 7.10 % (140/1971) | 1/5 | 13.4 % | 0.663 | 0.759 |
| 1-NN con abstención (mejor de los dos preregistrados) | 10.82 % (184/1700) | 0/5 | 33.6 % | 0.451 | 0.610 |
| 1-NN reciente con abstención (añadido después, D1) | 7.26 % (141/1941) | 0/5 | 31.6 % | 0.557 | 0.728 |
| mentiroso consistente → cuarentena | 83.3 % (500/600) | 0/5 | 16.7 % | 0.000 | 0.167 |

Microsegundos por clic (decisión): macros 1 · colonia 56 · colonia_v2 60 · cuarentena 74 · 1-NN 86 · logística 339 (incluye su reajuste). El cálculo de rasgos, común a todos, suma ~84 (medido aparte en la semilla 99). Memoria tras la fase A: colonia 13 células, cuarentena 27 + 21 de efecto, 1-NN 135 ejemplares.

## Predicciones
- P1 reordenar (colonia ≥0.80): **REFUTADA**, 0.632. P2 distractores (≥0.80): **REFUTADA**, 0.758. P3 renombrar (≥0.60): **REFUTADA**, 0.255. Las macros sí caen donde se dijo (posición 0.003 y 0.013; etiqueta 0.000).
- P4 macro por etiqueta gana en reordenar: cumplida, 1.000.
- P5 cambia-y-vuelve, colonia − 1-NN ≥0.15: cumplida 5/5 (+0.33 a +0.83).
- P6 cuarentena ≤1 % y sin cuarentena ≥8 %: cumplida (0.00 % y 14.88 %). P7 costo ≤15 puntos: cumplida, 1.3. P8 el mentiroso consistente atraviesa: cumplida, 83.3 %.
- Control barajada: **FALLA**. La colonia sólo queda por delante en 3/5 semillas; barajada le gana en reordenar (0.860 frente a 0.632). El pago no está haciendo el trabajo.
- Mis apuestas: (a) "empata con el 1-NN en renombrar": refutada, pierde por 0.65. (b) "gana al 1-NN pero no al 1-NN reciente en cambia-y-vuelve": acertada. (c) "sin cuarentena queda bajo 8 %": refutada. (d) "el costo pasa de 15": refutada.

## Criterio de cierre
- renombrar: gana el 1-NN (0.902 frente a 0.255; 0/5 semillas para la colonia).
- cambia-y-vuelve: gana la colonia, pero el candado salta: el 1-NN con desempate por recencia hace 1.000, igual que ella. La victoria es contra un rival que no borra lo contradicho.
- irreversibles: gana la cuarentena (0.00 % frente a 10.82 %; contra el rival reforzado de D1, 7.26 %).

## Qué falló
- La colonia preregistrada nace sólo donde falla la política, y el clic de mejor esfuerzo acierta de rebote: se queda con 13 células para 27 contextos y se hunde al renombrar. Corregido eso (colonia_v2, exploratorio), **empata con el 1-NN en todo** (renombrar −0.015, distractores +0.008) salvo cambia-y-vuelve. No hay nada que la colonia haga que un prototipo más cercano no haga.
- Los rasgos, por descuido mío, dejan que el contexto pese tanto como la etiqueta: en reordenar todos los brazos por rasgos quedan en 0.38–0.63. Con contexto a 0.25 (`datos/sensibilidad_ctx025.md`, exploratorio) reordenar sube a 0.97 y renombrar baja a 0.06; el patrón de cierre es idéntico.
- La logística no es techo en renombrar (0.113).
- El costo de 1.3 puntos está confundido: la cuarentena tiene más células que la colonia con la que se compara. Contra colonia_v2 el costo es 12.2 puntos.
- La ventaja de la cuarentena depende de dónde se mire. Con mentiroso inconsistente es clara (0 frente a 64 % del 1-NN reciente) pero cuesta: se abstiene en el 94 % y completa sola el 3 %. Sin mentiroso, contra el rival reforzado, queda en 0/1741 frente a 6/1721 (0.35 %): menos de un punto, empate según mi propia regla. Sólo en desplazamiento, con el umbral calibrado ahí, 0/941 frente a 34/921 (3.7 %).

## Qué no se verificó
- Nada fuera de este simulador: sin pantallas reales, sin estado entre pasos (cada paso es una decisión independiente), y la marca de irreversible se da hecha.
- El efecto de un clic es función determinista del elemento; la célula de efecto tiene el trabajo fácil.
- Por qué la cuarentena se abstiene en el 16.7 % con el mentiroso consistente (hay una célula sin validar por semilla; no lo seguí).
- Un 1-NN con negativos o con regla de dos coincidencias; sería el rival que falta para la parte 2.
- Sensibilidad a k, al radio y al 40 % de mentira: un solo valor de cada uno.

## Desviaciones
D0 (tras el humo, antes de evaluar): se añaden `colonia_v2` y la corrida de contexto 0.25, fuera del veredicto. D1 (después de ver resultados): se añade el rival `1nn_rec_abst_irr` y dos tablas post hoc; la primera salida quedó en `datos/principal_v1_antes_de_D1.json` y la nueva la reproduce idéntica. Ninguna perilla se tocó.

Archivos: `PREREGISTRO.md`, `reflejo_clic.py` (`--humo`), `analiza.py`, `demo.py`, `datos/principal.json` y `.md`, `datos/sensibilidad_ctx025.json` y `.md`, `datos/humo.json`.
