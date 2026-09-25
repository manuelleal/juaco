# INFORME — CÓDIGO GENÉTICO v0.1 (Opus, equipo organelos, 24-sep-2026, 22:10). Misión: llegar a la AGI por este camino.

**Veredicto del trabajo: FUNCIONA como instrumento. La serie NO está corrida.** El paquete está listo para el PC del director:
- la calibración de PERILLAS_ROBUSTA está hecha y aceptada (λ = 0.292);
- el arnés da 11/11;
- el humo a la TL de la serie escribe los 10 JSON.

**Mi predicción para la serie: NO (0.45), MODESTO (0.32), FUNCIONA (0.18).**

## La pregunta
v0 igualó ERRORES por copia (~1.1), no FENOTIPOS cambiados por copia. Con la cinta el ~72 % de los hijos nace con el fenotipo idéntico al
del donante; con PERILLAS, el ~31–34 %. **¿La cinta sigue viviendo sola mejor cuando PERILLAS muta el fenotipo con la misma frecuencia?**
- **P1 decide:** CODIGO_SIN_SOS > PERILLAS_ROBUSTA en nacimientos solos tras el corte, ≥ 15/20, en quieto y en onda8k por separado.
- FUNCIONA si pasa en los dos mundos con las guardias MUT0 y AZAR; MODESTO si pasa en uno (o en los dos sin una guardia); NO si no pasa.

## Qué construí (`experimentos/organelos/codigo/v01/`; no toqué nada fuera, ni `prometeo/`, ni los archivos del Fable)
- **`construye_v01.py` → `motor_v01.py`**: 4 anclas sobre `motor_fable.py`, cuyo sha se verifica. `fable_mundos.py` se IMPORTA de
  `exploracion_fable/`. Las anclas agregan sólo telemetría:
  - el fenotipo cambiado por parto en PERILLAS;
  - **el banco de CINTAS en el corte**;
  - su salida.
- **`corre_v01.py`**: `--calibra`, `--calibra_rob`, `--humo`, `--serie` (Pool, sólo el coordinador) y `--lee`, que además de la letra da
  un descriptivo del banco en el corte: cintas desarrolladas frente a perillas, en log(g/G0).
- **`identidad_v01.py` 11/11**:
  - **I2 (la pedida):** ROBUSTA con la mutación en 0 == PERILLAS con la mutación en 0, bit a bit.
  - I2b: con λ = 1, ROBUSTA == PERILLAS.
  - I1: `motor_v01` == `motor_fable` en 4 brazos/mundos.
  - I3: la telemetría de fenotipo.
  - I4: el banco de cintas.
  - I5: quieto == sin cambio.
  - I6: AZAR sin SOS.
- **`PREREGISTRO_v01.md`**: la letra, las predicciones y el costo. §0–§8 quedaron con sha 9705085a16ca026f a las 21:54, antes de leer el
  humo.

## Calibración de PERILLAS_ROBUSTA (rápida y declarada)
Un solo factor λ sobre TODAS las tasas de PERILLAS (numérica y gramática). Se corrió con TL_CAL (T 36 000, el TL corto del Fable) y 3 + 3
semillas, en un proceso, ~20 min.
1. CODIGO_SIN_SOS (29901–29903, quieto y onda8k): fracción idéntica **0.715** (n 3868).
2. λ analítica = 0.292.
3. PERILLAS_ROBUSTA (29904–29906) midió **0.721**, dentro de la tolerancia de ±0.03 fijada antes. **Se acepta LAMBDA_ROB = 0.292.**

- Declarado: ROBUSTA iguala la FRECUENCIA del cambio de fenotipo, no su TAMAÑO.
- Tolerancia para la serie: si las medianas de SIN_SOS y ROBUSTA en quieto difieren en más de 0.05, P1 lleva la nota «carga no
  igualada» y un ERR.

## Diseño recortado al límite del director (≤ 45 min de pared, Pool 6, 20 semillas)
- **TL de la serie: T 24 000, onda desde t = 0, corte en 16 000, margen 2 000.** La onda llega al corte en su fase de fábrica, como en el
  Fable. Nac solo se cuenta en [16 000, 22 000).
- Brazos: CODIGO_SIN_SOS, PERILLAS, PERILLAS_ROBUSTA, MUT0 (los mínimos) y AZAR.
- **Quedan fuera por costo:** CODIGO con SOS (`--con_sos`, +~9 min) y golpe (`--con_golpe`, +~16 min). Sin CODIGO con SOS, P3 no se mide.
- **Orden:** los 4 mínimos primero (160 corridas) y AZAR al final (40). Si el tiempo se acaba, sólo cae AZAR. En ese caso la guardia de
  selección queda «no medida» y FUNCIONA baja a MODESTO.
- **Costo** (humo en este PC, 73 s por corrida de media: quieto ~85 s, onda ~59 s): **200 corridas ≈ 41 min con Pool 6** (los 4 mínimos
  ≈ 33 min). No medí cuánto se frena cada corrida con 6 a la vez en el PC del director.
- Recorte frente al Fable: el vivero dura 16 000 en vez de 24 000. Hay menos generaciones de selección, y el efecto puede salir más chico.

## Humo (29001, TL de la serie, 10 corridas en un proceso, 732 s; una semilla, SIN valor)
| mundo | SIN_SOS | PERILLAS | ROBUSTA | MUT0 | AZAR |
|---|---|---|---|---|---|
| quieto: nac solo | 114 | 56 | 56 | 60 | 47 |
| quieto: fenotipo idéntico | 0.80 | 0.29 | 0.72 | 1.0 | 0.84 |
| onda8k: nac solo | 31 | 28 | 22 | 25 | 37 |
| onda8k: fenotipo idéntico | 0.67 | 0.32 | 0.71 | 1.0 | 0.81 |

- **Banco en el corte**, en quieto y con SIN_SOS: el **74.5 % de las cintas lleva un `EJE 2` con d < 0**. Una sola mutación baja dote,
  rep_umbral, rep_X y tau_e a la vez; aquí quedaron en −0.335 en log. En PERILLAS y ROBUSTA esos rasgos no se movieron (±0.01).
  - Es el mecanismo que apuesto en el preregistro, escrito antes de leer el humo: la pleiotropía da «vida rápida» en un paso, y la
    selección por fertilidad del vivero la barre.
  - Pero es UNA semilla, y en onda8k no apareció.

## Comandos (el coordinador, en el PC del director)
```
python experimentos/organelos/codigo/v01/construye_v01.py      # debe dar sha 8a67a259baa5454b
python experimentos/organelos/codigo/v01/identidad_v01.py      # 11/11
python experimentos/organelos/codigo/v01/corre_v01.py --serie --ventana serie --pool 6
python experimentos/organelos/codigo/v01/corre_v01.py --lee experimentos/organelos/codigo/v01/datos/v01_serie_s29011-29030
# manana: --serie --ventana replica --pool 6   (29031-29050)
```
- Si se corta, se sigue con `--reanuda`: salta los JSON ya escritos.
- La serie escribe `RESUMEN.json` y `progreso.log` en su carpeta, unos 70 KB por corrida.

## Mis predicciones refutadas y lo que no verifiqué
- **Refutadas hasta ahora:** ninguna medible; no hay serie.
  - En la calibración esperaba que la fracción idéntica del código se pareciera a la del Fable (~0.65). Salió 0.715 (0.67–0.78 por
    corrida) porque la cinta también cambia su propia tasa: los errores por copia van de 0.57 a 1.19 según la semilla.
  - Mi supuesto de que la carga de la cinta es fija por diseño queda refutado: las zonas TASA derivan.
- **No verifiqué:**
  - la serie ni Pool 6 en el PC del director (el costo es una estimación con un proceso);
  - que la fracción idéntica se mantenga igualada a la TL de la serie más allá de una semilla (el humo da +0.08 en quieto a favor de
    SIN_SOS);
  - que 16 000 pasos de vivero basten para que la «vida rápida» se seleccione en la mayoría de las semillas;
  - la SOS y golpe, fuera por costo.
- **Lo que leería primero de la serie:** el descriptivo del banco (`--lee`).
  - Si CODIGO gana a ROBUSTA y su banco muestra el `EJE 2` negativo, la estructura ayuda porque ofrece un cambio COORDINADO: la
    pleiotropía que la selección puede tomar de un paso.
  - Si ROBUSTA empata, la ventaja era carga.
