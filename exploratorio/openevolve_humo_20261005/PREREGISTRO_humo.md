# PREREGISTRO del humo JUACO × OpenEvolve (5-oct-2026, escrito ANTES de correr el humo principal)

Misión: llegar a la AGI por este camino. Esto es un HUMO EXPLORATORIO de una tarde: **nada se declara**. Sirve para saber
si la herramienta funciona en este PC, cuánto cuesta y si vale la pena una serie con protocolo.

## 1. Pregunta
Partiendo de O1 con la limpieza quitada (`CTRL_O1_SINLIMPIA`, que colapsa), ¿un bucle de OpenEvolve (un modelo de lenguaje
propone cambios de código, un juez fijo los puntúa) reencuentra en ≤ 30 iteraciones algo que haga persistir a los linajes?
Lo que se pone a prueba es **evolución de programas guiada por un modelo de lenguaje sobre un juez fijo**. No es selección
natural del organismo, y el modelo puede "saber" trucos por cultura general.

## 2. Instrumento (fijado antes de correr)
- Pista y juez de JUACO **sin tocar** (sólo se leen): `pista.py` sha 9f47c65e438e0ff4, `juez.py` sha 6a68f640a7832f12,
  `revisa_carro.py` sha 1c8a789f7427ab96. Llamada = la de `corre_v143.tarea` (9 carros iguales, pizarra 1, escala 1) con
  **fundador NO limpio** (`fundador_limpio=0`, por ERR-191).
- Punto de partida: `raiz/programa_inicial.py` = `CTRL_O1_SINLIMPIA` (sha be029b0a1b8d6634) sin comentarios ni código muerto
  que delaten el mecanismo (se quitaron la bandera apagada, la función de "golpe costeable" y la constante PISO).
  Identidad comprobada: misma física que `CTRL_O1_SINLIMPIA` a T 5 000 y T 25 000 (semilla 270001), campo a campo.
- Modelo: Claude Sonnet por el CLI de Claude Code (sesión del director, sin clave), **sin herramientas**, en modo seguro
  (sin memoria, CLAUDE.md, agentes ni MCP) y en una carpeta vacía: no puede leer el repo JUACO.
- Prompt neutro (`config_humo.yaml`): describe el mundo, la interfaz, lo prohibido y el objetivo. No nombra O1, ni la
  limpieza, ni qué letra es buena o mala. Sí dice la física (un objeto sólo se va si alguien lo muerde o por retiro al azar).
- OpenEvolve 0.4.0: 1 isla, cambios en formato diff, temperatura por defecto del CLI, `random_seed` 42, **1 evaluación a la vez**.

## 3. Puntaje (por corrida de 9 linajes)
`base = [0.5 × (persisten/9) + 0.4 × (cruzan con R0 real/9) + 0.1 × min(mediana R0 real, 1)] × (1 − fracción de muertes voluntarias)`
- "persiste", "cruza_real", "R0_real" y "muertes voluntarias" son los de `juez.resumen_linaje` (física de la pista).
- El R0 solo pesa 0.1 (desempate): por ERR-99/102 nunca decide.
- Programa rechazado por `revisa_carro`, por la **regla de tabla** (nombrar letras del mundo en el código = oráculo) o que
  revienta: **puntaje 0** y el motivo vuelve como artefacto.

## 4. Cascada
| Etapa | T | Semilla | Puntaje | Pasa si |
|---|---|---|---|---|
| 1 | 5 000 | 271001 | 0.05 si corre, 0 si no | corre y pasa el filtro |
| 2 | 25 000 | 271002 | base2 = [0.7 × (linajes sin extinción tras t = 10 000)/9 + 0.3 × min(mediana R0 real, 1)] × (1 − muertes voluntarias); 0.05 + 0.10·base2, o 0.20 + 0.10·base2 si pasa | ≥ 5/9 linajes sin extinción tras t = 10 000 |
| 3 | 100 000 | 271003 | 0.30 + 0.70·base | — |

**Enmienda hecha por la cordura, antes de correr el humo:** la primera versión de la puerta de la etapa 2 era "persisten
≥ 3/9". La cordura mostró que estaba mal: a T 25 000 el "persiste" del juez exige ≥ 5 nacimientos reales y O1 de fábrica
sólo lo cumple en 2/9 (aunque no se extingue ninguno), así que O1 no habría llegado a la etapa 3. Se cambió por "sin
extinción tras t = 10 000" (el mismo dato físico del juez, sin el mínimo de nacimientos). La etapa 3 no cambia.

La etapa 3 usa UNA semilla (no dos) para que el humo quepa en una tarde con un solo proceso; el sobreajuste a esa semilla
se mide en el examen.

## 5. Semillas
- Calibración del evaluador (cordura): 270001, 270002.
- Búsqueda: 271001 (etapa 1), 271002 (etapa 2), 271003 (etapa 3).
- **Examen selladas: 272001, 272002, 272003** (T 100 000, fundador no limpio). El bucle y el modelo nunca las ven.
- Comprobación con `rg` en `PROYECTOS\JUACO\organelos`: ninguna aparece como semilla (ni en nombres de archivo `s27x00y`,
  ni en campos `seed`, ni en `--desde`). Las únicas coincidencias del número son decimales de datos (p. ej. `0.270001`)
  e índices de tiempo dentro de 9 JSON de datos viejos.

## 6. Presupuesto y parada
- Ejemplo de comprobación: 6 iteraciones (ya corrido antes de este preregistro; no es parte del humo).
- Humo principal: **30 iteraciones** de OpenEvolve, tope duro de 33 llamadas al modelo (30 + 3 reintentos). Se para ahí.
- Una sola corrida del bucle. Sin réplicas (es humo).

## 7. Controles
- **Cordura del evaluador (obligatoria antes de buscar):** O1 de fábrica a T 100k en 270001–270002 debe cruzar 5–8 de 9;
  `CTRL_O1_SINLIMPIA` debe dar 0 de 9; tres carros tramposos de prueba: dos rechazados (marcos de Python; tabla escrita a
  mano) y uno que miente en `salida()` debe puntuar igual que la raíz.
- **Examen:** el mejor programa (el de mayor puntaje del bucle, congelado) junto a **O1** (techo) y a **la raíz** (suelo =
  "la raíz sola, sin búsqueda") en las mismas 3 semillas selladas.
- Auditoría a mano del mejor programa (que no use trucos fuera de las reglas).
- NO se corren en el humo (se describen en el informe): azar con el mismo presupuesto, modelo débil, réplicas del bucle.

### Resultado de la cordura (corrida antes del humo; archivos en `cordura/`)
| Prueba | Resultado |
|---|---|
| Ancla de identidad: O1, fundador no limpio, semillas ya registradas 883001 y 883002 (paso A del muro, hoy) | **idéntico al registro**: cruzan 5/9 (R0 real 0.9032, causas 71/83/25/30) y 8/9 (0.963, 99/60/32/45) |
| O1, T 100k, calibración 270001 / 270002 | cruzan **5/9** y **2/9** (persisten 7 y 2). La segunda queda FUERA del 5–8 esperado: el rango "5–8" salió de dos semillas; el evaluador es idéntico al canónico, así que es variación de semilla de O1, no fallo del arnés |
| `CTRL_O1_SINLIMPIA`, T 100k, 270001 / 270002 | **0/9 y 0/9** |
| Raíz limpia de pistas == `CTRL_O1_SINLIMPIA` (T 5k y 25k) | idéntica campo a campo |
| O1 por la cascada (semillas de búsqueda) | 0.05 → 0.294 → **0.826** (etapa 3: persisten 7/9, cruzan 6/9) |
| Raíz por la cascada | 0.05 → **0.058** (no pasa a la etapa 3) |
| Tramposo "marcos de Python" / "tabla escrita a mano" | rechazados, puntaje 0 |
| Tramposo "miente en salida()" | pasa el filtro y puntúa **igual que la raíz** (0.058): la mentira no cuenta |

Consecuencia para leer el examen: O1 mismo puede dar 2/9 en una semilla. El techo se lee en la misma semilla, no contra "5–8".

## 8. Cómo se lee (veredicto del HUMO, no declaración)
- **FUNCIONA (como humo):** el mejor programa persiste en ≥ 5/9 linajes en ≥ 2 de las 3 semillas selladas, y la raíz en 0.
- **HAY ALGO MODESTO:** el mejor supera a la raíz en las 3 semillas selladas (más linajes que persisten, o mediana de R0
  real ≥ raíz + 0.10) sin llegar a lo anterior.
- **NO:** lo demás, o el bucle/proveedor no funciona.

## 9. Predicción firmada (antes de correr)
| Predicción | Probabilidad |
|---|---|
| El humo sale FUNCIONA por la letra de la sección 8 | 0.70 |
| El mecanismo del mejor programa es "morder lo que daña cuando no hay nada útil, para que aparezca otra cosa" (limpieza) | 0.75 |
| Aparece en las primeras 5 iteraciones | 0.50 |
| El mejor iguala o supera a O1 en linajes que cruzan (suma de las 3 selladas) | 0.30 |
| Al menos una propuesta del modelo es rechazada por el filtro de reglas | 0.50 |
| Al menos 20 % de las iteraciones se pierden por diffs mal formados | 0.35 |

Motivo de la confianza alta: el prompt dice la física (lo que nadie muerde se queda) y el resumen que vuelve al modelo
muestra el mundo lleno de las dos letras que dañan. Para un modelo de lenguaje eso es casi una adivinanza resuelta; por
eso un FUNCIONA aquí **no** prueba que el bucle "descubra": probaría que la tubería funciona. Lo interesante sería la
sorpresa: que no lo encuentre, o que encuentre algo distinto y mejor que O1.

Firmado: agente del encargo (Claude), 5-oct-2026, antes del humo principal.
