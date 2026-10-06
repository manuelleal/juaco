# PREREGISTRO — reflejo de clic y cuarentena del clic irreversible

Escrito el 5-oct-2026 ANTES de correr ninguna semilla de evaluación y antes de ver ningún acierto (al escribirlo sólo se
había comprobado que el módulo importa y que arma pantallas de 9–24 elementos en la semilla de desarrollo 99).
Exploratorio, un proceso, sólo numpy. Código: `reflejo_clic.py`. Análisis: `analiza.py`.

## Hipótesis
1. Una colonia de células con clave LOCAL (rasgos del elemento respecto a la instrucción, nunca posición absoluta) aprende
   de 5 demostraciones por familia a completar tareas de formulario y aguanta reordenar, distractores y renombrar donde las
   macros se rompen.
2. La regla de cuarentena (hipótesis → validada con k=2 confirmaciones independientes, más una segunda célula que predice
   el efecto del clic) baja los clics irreversibles errados a ≤1 % con un costo acotado en tareas completas.

## Mecanismo mínimo y memoria nueva
- Célula de clic: clave (143 números), radio, energía, confianza, efecto demostrado. Tope 200.
- Parte 2 añade por célula: validada, confirmaciones, última demostración que confirmó, paso de nacimiento; y una segunda
  colonia de células de efecto (clave rol + etiqueta propia, valor = efecto), tope 200. Esa es la memoria nueva.
- Sin retropropagación en la colonia. La logística (techo) sí usa gradiente.

## Simulador (congelado aquí)
- 48 conceptos con 3 etiquetas cada uno (canónica, variante que comparte letras, otra palabra). 6 roles.
- 6 familias (registro 5 pasos, contacto 4, pago 5, baja 3, filtro 4, pedido 6). Irreversibles marcados a mano: enviar,
  borrar, pagar. Todas las pantallas tienen al menos un irreversible que NO es el blanco.
- Por semilla: disposición canónica de cada familia (0–4 rellenos, orden de grupos y dentro del grupo al azar).
  Cada pantalla concreta añade 0–3 enlaces en un grupo `pie` al final. 9–24 elementos.
- Enseñanza: 5 demostraciones por familia, familias intercaladas. Prueba: 20 tareas por familia y régimen (120 por régimen
  y semilla). Nadie aprende durante la prueba.
- Regímenes: `sin_cambio`; `reordenar` (baraja grupos y dentro de cada grupo); `renombrar` (TODOS los blancos del guion
  pasan a un sinónimo al azar, el resto con p=0.5); `distractores` (4–8 elementos nuevos en sitios al azar, 30 % son dobles
  con la etiqueta de un elemento real y otro rol); `cambia_y_vuelve` (versión B: en cada familia un paso cambia de blanco a
  otro elemento de la misma pantalla; 5 demostraciones por familia en B; luego UNA demostración por familia de vuelta en A
  y se prueba en A. Se registran también 0 y 2 demostraciones de vuelta, como curva, no como predicción).
- Tarea completa = todos los pasos bien, sin pedir ayuda. Un clic malo corta la tarea.
- Mentiroso inconsistente: en cada paso de cada demostración, con p=0.4 pisa otro elemento al azar. Mentiroso
  consistente: en cada familia, en el paso irreversible (o el último), pisa SIEMPRE el mismo irreversible equivocado.
  Los dos se prueban sin cambio contra la verdad del guion.

## Rasgos (iguales para colonia, 1-NN y cuarentena; la logística recibe los mismos crudos)
Distancia cuadrada por bloques: instrucción 1 · rol 1 · coincidencia de etiqueta con la palabra de la instrucción
(0.5·exacta + 0.5·coseno de pares de letras) 1 · etiqueta vecina 0.5 · orden en su grupo 0.5. Los pesos se fijan a priori:
lo propio del elemento pesa 1, lo del contexto pesa 0.5. No hay posición absoluta en la clave.

## Perillas (fijadas a priori, sin barrido)
Radio inicial R0 = 0.95 (deja entrar un cambio de contexto, no un cambio de rol, instrucción o etiqueta); c_exist 0.01;
pago 0.5; castigo 0.5; eta 0.2; E0 1.0; tope 200. Cuarentena: k=2, plazo 80 pasos, E_h 0.4, gana 0.3, pierde 0.2.
Célula de efecto: radio 0.6. Logística: 400 iteraciones, lr 0.2, L2 1e-3.

## Brazos
`macro_pos` · `macro_etq` · `1nn` (200 ejemplares FIFO, mismos rasgos; empates exactos → primer elemento de la pantalla) ·
`1nn_reciente` (rival EXTRA que añado: entre empates exactos gana el ejemplar más nuevo) · `logistica` (techo) ·
`colonia` · `colonia_barajada` (control: pago, castigo y ajuste de clave van a una célula al azar) · `cuarentena` ·
ablaciones `cuar_sin_efecto` y `cuar_sin_k` · `1nn_abst` en dos variantes: `irr` (se abstiene sólo cuando propone un
irreversible) y `todo` (en cualquier paso), umbral de distancia elegido por semilla en una rejilla de 83 valores para que
su tasa de abstención sea la más cercana a la de la cuarentena. Calibrar sobre la propia prueba FAVORECE al rival; se deja así.

## Medidas
- Parte 1: fracción de tareas completas por régimen; media de 5 semillas y pareado por semilla (gana/empata/pierde).
- Parte 2: irreversibles errados = clics irreversibles equivocados EJECUTADOS / propuestas de irreversible (ejecutadas o
  abstenidas), sumado sobre el conjunto primario = los 5 regímenes honestos + mentiroso inconsistente. También por 100
  tareas y cuentas crudas. Costo = tareas completas sin ayuda de `colonia` menos las de `cuarentena`, en puntos, sobre los
  5 regímenes honestos. Tasa de abstención: `irr` = abstenciones / propuestas irreversibles; `todo` = (abstenciones +
  reversiones) / pasos.
- Microsegundos por clic (decisión) por brazo, y aparte el cálculo de rasgos.

## Predicciones (las del encargo, tal cual)
P1. reordenar: colonia ≥ 0.80 y macro_pos ≤ 0.30.
P2. distractores: colonia ≥ 0.80 y macro_pos ≤ 0.30.
P3. renombrar: colonia ≥ 0.60 y macro_etq ≤ 0.20.
P4. macro_etq ≥ 0.95 en reordenar (se declara que ahí gana o empata la macro).
P5. cambia_y_vuelve: colonia − 1nn ≥ 0.15 en ≥ 4/5 semillas.
P6. irreversibles errados de la cuarentena ≤ 1 % en el conjunto primario; colonia sin cuarentena ≥ 8 %.
P7. costo ≤ 15 puntos de tareas completas.
P8. el mentiroso consistente atraviesa la cuarentena (fallo conocido): irreversibles errados con `ment_con` ≥ 50 %.
Control que puede fallar: colonia > colonia_barajada en la media de los 5 regímenes en ≥ 4/5 semillas.

Mis propias apuestas, para poder declararlas refutadas: (a) en renombrar la colonia EMPATA con el 1-NN (±0.05), porque
con estos rasgos y sin presión de negativos en la enseñanza la colonia se reduce a prototipo más cercano; (b) en
cambia_y_vuelve la colonia gana al `1nn` pero NO al `1nn_reciente`; (c) la colonia sin cuarentena queda por debajo del
8 % de irreversibles errados (P6 a medias); (d) el costo pasa de 15 puntos por culpa de renombrar (P7 refutada).

## Qué refuta
P1–P3, P5–P7 se leen literal sobre la media de 5 semillas (P5 por semilla). Un número fuera del rango = refutada.

## CRITERIO DE CIERRE
"Gana la colonia" en un régimen = diferencia de medias ≥ 0.05 Y por delante en ≥ 4/5 semillas (en cambia_y_vuelve: P5).
"Gana la cuarentena" en irreversibles = su tasa agregada es menor que la del MEJOR de los dos `1nn_abst` por ≥ 1 punto
porcentual. Si no, el 1-NN empata o gana.
**Si el 1-NN (con abstención en la parte 2) empata o gana en renombrar, en cambia_y_vuelve y en irreversibles, la línea
se CIERRA y el veredicto es NO.**
Veredicto: FUNCIONA = gana en las tres y se cumplen P1–P3 y P6; HAY ALGO MODESTO = gana en una o dos; NO = en ninguna.
Candado adicional: si la única victoria es cambia_y_vuelve y `1nn_reciente` empata ahí con la colonia, se dice que esa
victoria es contra un rival sin desempate y el veredicto no pasa de MODESTO.

## Semillas
Desarrollo (humo, arnés, depuración): 99. Evaluación: 11, 12, 13, 14, 15 (nuevas, no se miran antes de congelar).
Arnés: `python reflejo_clic.py --humo` corre la 99 dos veces y exige JSON idéntico (sin tiempos).

## Regla de desviaciones
No se ajustan perillas después de ver las semillas de evaluación. Todo cambio hecho tras el humo de la 99 se anota abajo
con su motivo ANTES de correr la evaluación; todo cambio posterior se anota como desviación y no salva el veredicto.

## Desviaciones y cambios tras el humo
Anotado tras el humo de la semilla de desarrollo 99 (5 tareas por familia) y ANTES de correr 11–15.
Arnés: identidad de dos corridas de la 99 = OK. Cordura: sin_cambio = 1.000 en todos los brazos.

Lo que mostró la 99 (una semilla, 30 tareas por régimen; no es resultado):
- La `colonia` preregistrada se queda con ~15 células para 27 contextos: como "nace donde la política falla" y la política
  incluye el clic de mejor esfuerzo, cuando acierta de rebote con una célula de OTRA instrucción no nace nada. En
  renombrar eso la hunde (0.23 frente a 0.97 del 1-NN en la 99).
- Con contexto a peso 0.5+0.5 la coincidencia de etiqueta no domina: en reordenar los brazos por rasgos quedan en ~0.5–0.6.
  Fue un descuido mío de diseño (el contexto suma 1.0, lo mismo que la etiqueta), igual para colonia y 1-NN.

Decisión: NO se toca nada de lo preregistrado. `colonia`, rasgos, perillas, predicciones y criterio de cierre quedan
como están y el veredicto se calcula sobre ellos. Se AÑADEN, fuera del veredicto y marcados como exploratorios:
1. brazo `colonia_v2`: igual que `colonia`, pero también nace cuando ninguna célula OÍA el elemento demostrado (acertar
   de rebote no cuenta como saber). Un solo cambio, sin perillas nuevas.
2. una corrida de sensibilidad con el peso de contexto a 0.25 (un único valor, fijado aquí, sin barrido):
   `python reflejo_clic.py --ctx 0.25 --out datos/sensibilidad_ctx025.json`. Mismas semillas 11–15.
Ninguno de los dos puede cambiar el veredicto; sólo dicen si el NO (o el sí) depende de esas dos decisiones.

Aclaración de medida (no cambia nada): los microsegundos de la logística incluyen su reajuste con gradiente.

### D1 — DESVIACIÓN, hecha DESPUÉS de ver las semillas 11–15 (sólo puede perjudicar a la línea)
Al mirar la tabla por condición vi que los irreversibles errados del `1nn_abst` preregistrado salen casi todos de
cambia_y_vuelve (60) y del mentiroso inconsistente (120): ejemplares contradictorios a distancia 0, que ningún umbral de
distancia puede evitar. Es el mismo defecto del rival que el candado de cambia_y_vuelve ya preveía. Añado, sin tocar nada
de lo anterior (la primera salida queda en `datos/principal_v1_antes_de_D1.json`):
- rival `1nn_rec_abst_irr`: el 1-NN con desempate por recencia más abstención por distancia en irreversibles, calibrado
  igual que el otro;
- dos tablas post hoc: sólo desplazamiento (reordenar + renombrar + distractores) y primario sin mentiroso, con el
  umbral del 1-NN calibrado dentro de cada subconjunto;
- el costo de la cuarentena medido también contra `colonia_v2`.
El veredicto mecánico se sigue calculando con lo preregistrado; D1 se informa al lado como candado. Se vuelve a correr
`principal.json` con el código nuevo y se exige que todo lo que ya existía salga idéntico.
