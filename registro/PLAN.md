# PLAN — Traspaso a Claude Code y etapas siguientes

> **ORDEN VIGENTE AL 16 SEP 2026 (día 4, tarde). Manda sobre todo lo de abajo.**
> Los "Pasos" numerados de la sección "PLAN PARA LA PRÓXIMA SESIÓN" son **históricos**.
> 1. ✅ Prueba de coste del arreglo con el techo mordiendo: **PASA** (14/14).
> 2. + 3. ✅ Fundidos por dirección. Examen de congelación, criterio v3: **PASA 20/20. v8 es el tronco**
>    (tag `v8-tronco`).
> 4. ✅ **3T confirmatorio sobre v8: SÍ, y REPLICADO en semillas 21–40.** ERR-13 cerrado.
>
> **Siguiente, en la escalera del brief:** cerrar la **Etapa 3 (versión dura)** sobre v8. Primero se revisa su
> preregistro, escrito para v6, contra lo que v8 cambia, y **sólo después** se corre. Luego 2P y Etapa 4.
>
> Cola, sin fecha: 2P (política bajo hambre); A5 corregida (recuperación espontánea estructural); versión dura
> de Etapa 3; 3F (fusión).
>
> **Circula una copia externa del repo que afirma "v7 congelado": es falsa y no se fusiona**
> (`registro/AUDITORIA_copia_antigravity_20260916.md`).

> **ESTADO AL CIERRE DEL DÍA 3 (15 sep 2026).** Fase 0 y Fase 1: **HECHAS**. Etapa 3: primera mitad hecha.
> Ramas 3T, 3K y 2K-bis: cerradas, las tres con veredicto negativo y las tres útiles.
> v7 **NO congelado**. Detalle y criterios vivos en `REGISTRO_etapas_1_2.md`, sección "Día 3".
> Para retomar sin esta conversación: `registro/HANDOFF.md`, sección 9.

---

# PLAN PARA LA PRÓXIMA SESIÓN (escrito al cierre del día 3)

**Todo el proyecto converge hoy en un solo punto: BUG-01.** Tres ramas independientes que no se hablaban entre
sí (3T composición temporal, 2K-bis capacidad, y el propio arreglo) lo señalan como el cuello de botella real.
No es un detalle de implementación: es lo que impide la composición temporal, lo que baja la capacidad de v7
por debajo de la de v6, y lo que congela el 82% de los valores de v7 en 0.000 exacto.

## Paso 1 (el que importa) — BUG-01 experimento 2: decaer sólo la PARTE COMÚN
El experimento 1 (decaimiento uniforme) está **refutado con demostración**: la ventana de λ es vacía
(hace falta λ>0.015 para no saturar y λ<0.010 para no estropear W_B). El diagnóstico es que el decaimiento
uniforme ataca la **magnitud** y la patología es de **redundancia**.

Cambio a probar, UNO solo:

    m = np.minimum(Wp[ix], Wn[ix]);  Wp[ix] -= lam_c*m;  Wn[ix] -= lam_c*m

**Propiedad clave, que es la razón de elegirlo**: resta lo mismo a los dos canales, así que **`Wp − Wn` queda
exactamente intacto** y el valor neto sigue obedeciendo Rescorla-Wagner puro. Desaparece el sesgo del 1.1%
que hundió P2 en el experimento 1, y con él la tensión entre no saturar y conservar el valor.

Predicción a derivar y escribir ANTES de correr (base: la derivación validada del exp. 1, que acertó a 3
decimales): la redundancia `m` tiene equilibrio `m* ≈ 0.045/λ_c`; para `m* < 1` hace falta **λ_c > 0.045**.
Elegir λ_c a priori por ese argumento, no por barrido. Predecir explícitamente si el canal mayor (`Wn`, que
crece 3× más rápido por la aversión) puede seguir topando y bajo qué condición, porque eso decide si hace
falta el experimento 3.

**Experimento 3, si el 2 no basta**: normalización opuesta completa — `m = min(Wp,Wn); Wp -= m; Wn -= m`,
que impide por construcción que se acumule redundancia. Un cambio por experimento; no mezclar con el 2.

Reusar `experimentos/bug01/corre_bug01.py`: ya evalúa P1–P4 con los mismos criterios y produce datos con
cabecera de procedencia. Los controles de inercia (`lam=0` bit-idéntico) y de reproducción del bug son
obligatorios otra vez.

## Paso 2 — con BUG-01 arreglado, repetir 3T como CONFIRMATORIO
3T ya mostró post-hoc que, levantando sólo el bloqueo, la regla de división **descubre sola la dimensión
temporal**: `sep` 3.97, `lift` 0.34, 20/20, alcanzando el techo de la versión cableada a mano. Eso no cuenta
hasta repetirlo con criterio escrito antes y con el arreglo principista en lugar del techo subido a mano.
**Si sale, es el nivel 7 de la escala del punto 6 con criterio preregistrado.** Es lo más valioso pendiente.

## Paso 3 — v7, con la ley de disparo definitiva
La ley correcta es **`err_max > 0.6`** (concordancia 320/320, con derivación: `err_max = 0.147509·|R|`, que
exige `|R|` efectivo > 4.068, imposible sin recompensas de signo opuesto sobre la misma celda). Las dos leyes
que registré antes —"umbral en 2 celdas" y "valencia opuesta"— están **refutadas** como enunciados generales.
Reescribir el criterio de disparo de `bateria_v7b.py` en términos de `err` y volver a correr 20 semillas.
Ojo: v7 sólo debería congelarse **después** de arreglar BUG-01, porque 2K-bis mostró que v7 tiene menos
capacidad que v6 precisamente por ese bloqueo.

## Paso 4 — 2P, política bajo hambre
Sigue siendo el único problema abierto de conducta y ahora cuesta minutos con la Fase 1 hecha.
Antes de correr: escribir la función objetivo (propuesta: minimizar muertes sujeto a tasa de mordida de comida
≥95% por visita) y reportar **la superficie completa** de α × hambre_boca × sesgo, no el mejor punto.

## Cola de preregistros pendientes (ninguno corrido)
- **Etapa 3 versión dura**: la fórmula `W_X = 0.333·nA − 1.0·nB` sólo se probó donde no podía fallar. Correrla
  con códigos solapados, con el clip activo y con más de dos estímulos, donde sí puede romperse.
- **3F fusión**: la operación inversa de 2L. El organismo sabe dividir y no sabe juntar. Sin lanzar.
- **`hebb_mordida` rompe E2K** (18/20), única condición de 3K que lo hace.
- **Dirección de división 2L v2 en la tarea de 3K**: dio 0.763 contra 0.683 del azar, el mejor de ese estudio,
  aunque por debajo del margen.
- **Techo de v6 en capacidad**: no se estableció; el diseño de 20.000 pasos por estímulo mide muestreo, no
  capacidad. Hace falta un cuarto punto de tiempo o igualar mordidas por estímulo en vez de pasos.

## Lo que NO hay que tocar
- `.gitattributes` con `* -text`. Sin él, git convierte LF→CRLF y **rompe los 55 hashes** en cualquier clon.
- Los cuatro archivos congelados. `python manifiesto.py` los verifica y sale con código 1 si alguno cambió.
- Rama 2M (pulpo): refutada el día 2, no entra al tronco salvo decisión explícita.

---

## Fase 0 — Validar el traspaso (primera sesión, ~20 min)
1. `git init`, commit inicial con este bundle. Etiquetar `v6-baseline`.
2. `cd organismo && python3 bateria.py 6` → todo PASA. Luego `python3 bateria.py 20`.
3. Reproducir `datos/baseline_v6.csv`: 20 semillas, A_sin y B_aprende. Comparar medianas con el registro
   (comida 1400/338, veneno Q4 370/13, muertes 218/142, W_A +1.00, W_B −3.00). Si coincide, el traspaso está validado.
4. Añadir al registro una línea: "Traspaso validado en Claude Code, fecha, hash".

## Fase 1 — Infraestructura mínima (una sesión)
- `experimentos/run_etapa.py --etapa <nombre> --semillas N` que llama a `organismo_v6.run` con el escenario, escribe
  `datos/<etapa>_<fecha>.csv` y `.json` (por semilla: mord, vis, W, comp, deaths, log), y añade una línea al registro con hash.
- Paralelizar semillas con `multiprocessing` (una semilla por proceso). 100 semillas × 100k pasos debe caber en minutos.
- Script `analiza.py`: medianas, rangos, tasas por visita, y la comparación con el baseline.
- Convención: nunca sobrescribir un CSV; cada corrida tiene fecha.

## Fase 2 — Cerrar lo abierto de la Etapa 2
### 2L → v7 (PRIMERO)
`cd organismo && python3 bateria_v7c.py 20`. Si todo PASA (incluido divisiones=0 en etapas normales), renombrar a organismo_v7.py,
hash, commit `v7`. Luego repetir baseline 20 semillas con v7 y comparar con v6. Si algo falla, 2L vuelve a hipótesis.

### 2K-bis — Capacidad representacional (hipótesis derivada del organismo)
Pregunta: qué ocurre cuando la demanda de representación se aproxima al techo.
Condiciones (un cambio por corrida, 20 semillas): D∩B = 0,1,2,3 con clip=3; y D∩B=1,2 con clip=1.5.
Predicción: degradación graduada creciente con solapamiento (ya medida: W_B −3.00/−2.9/−2.78 en 0/1/2 celdas);
con 3 celdas (códigos idénticos) W_D y W_B convergen al mismo valor intermedio (fallo completo); con clip reducido
el fallo aparece a menor solapamiento. Refutación: si con 3 celdas los valores se separan, hay un mecanismo no identificado.
Métricas: W_D, W_B por cuarto; Wp/Wn de ambos; celdas al tope; tasas por visita; muertes.

### 2P — Política bajo hambre (NO recalibrar α a ciegas)
Antes de correr: decidir el criterio (adoptado: tasa por visita condicionada al hambre) y escribir la función objetivo
de la política (p.ej. minimizar muertes sujeto a no dejar de comer). Luego barrer α, β=hambre_boca y b=+0.5 como
hipótesis explícitas, 20 semillas, y reportar la superficie completa, no el mejor punto.

### Semilla congelada de v4
Con v6 no reaparece en 20 semillas. Correr 100 semillas de E1 y contar fallos (comida<100). Si 0/100, cerrar.

## Fase 3 — Etapa 3: Generalización (plan original, punto 10)
Hipótesis: el organismo aprendió "estos píxeles = comida" y no una característica abstracta.
Pruebas: patrones con 1 píxel cambiado (ruido), patrones desplazados, combinaciones. Medir W del patrón nuevo ANTES de
la primera mordida (valor a priori) y cuántas mordidas tarda en converger. Predicción con Kenyon: generalización
proporcional al solapamiento de códigos, no a la similitud visual — eso es una predicción falsable y distintiva.

## Fase 4 — Etapa 4: Memoria (punto 11)
Comparar memoria cero / parcial / heredada tras muerte. Ya sabemos: olvido 5% por muerte × 400 muertes = amnesia total.
Barrer olvido_muerte ∈ {0, .01, .05} y medir recuperación.

## Fase 5 — Población (puntos 12–14), solo cuando el individuo esté cerrado
Retomar `poblacion2.py` con v6. Cambios ya identificados (uno por vez): renacer heredando Wp/Wn del mejor (no en blanco);
score que pese el veneno; compartir solo el canal aversivo vs solo el apetitivo. Pregunta: ¿acumula la población algo que un
individuo no alcanza en una vida? Criterio de emergencia (punto 14): propiedad ausente en el individuo, presente en el grupo,
no programada, reproducible, y que desaparece al romper la estructura.

## Fase 6 — Publicación
- Repo público con README que reproduzca el baseline en un comando.
- Texto de ~3 páginas: la cadena 2A→2G como "un organismo que pide la teoría a golpes", con la limitación metodológica.
- Figura 1: valores W_A, W_B por cuarto en E1/E2 (12 semillas). Figura 2: interferencia vs solapamiento (0/1/2 celdas).
- Venue candidato: ALIFE / Artificial Life journal / arXiv q-bio.NC. No prometer más de lo que la batería demuestra.

## Reglas de sesión en Claude Code
Empezar cada sesión con la batería. Terminar cada sesión con una línea en el registro. Nunca dos cambios a la vez.
Traer el registro al chat de diseño cuando haya que decidir qué hipótesis sigue.
