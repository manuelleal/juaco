## 14. Dónde está cada cosa en el repositorio

**Idea principal.** El trabajo vigente vive en la carpeta `C:\Users\User\Documents\PROYECTOS\JUACO\organelos` (rama `organelos`, sin unir todavía a la rama principal: lo decide el director). Hay tres zonas que no se mezclan: `registro/` (lo que se declara y su historia), `experimentos/` (cada experimento con su preregistro, su código y sus datos) y `exploratorio/` (lo que está fuera de protocolo). Para orientarse, el orden de lectura es siempre el mismo: primero `registro/ESTADO.md`, luego la entrada del registro, luego el preregistro del experimento.

### 14.1 La raíz

| Ruta | Qué hay |
|---|---|
| `registro/` | Estado, historia, reglas. Ver 14.2. |
| `experimentos/` | Todos los experimentos. Ver 14.3 a 14.6. |
| `exploratorio/` | Lo que no tiene protocolo. Ver 14.7. |
| `organismo/` | El organismo del tronco (versiones congeladas) y sus baterías de examen. |
| `RESULTADOS_VERIFICADOS.md` | Lista corta, en inglés, de resultados cerrados y replicados, cada uno con una frase de lo que **no** muestra. Al 29 de septiembre: no incluye todavía la Escalera. |
| `README.md`, `CITATION.cff`, `LICENSE`, `LICENSE-DATA` | Presentación pública, cómo citar, licencias. |
| `MANIFEST.txt`, `manifiesto.py` | Lista de huellas de los archivos congelados y el programa que la comprueba. |
| `BRIEF_ORIGINAL_y_estado.md` | El plan de pruebas original del proyecto. |
| `CLAUDE.md` | Instrucciones y resumen histórico para los agentes (hay otra copia, más antigua y con las fases 1 a 9, en `PROYECTOS\JUACO\bundle\CLAUDE.md`). |

### 14.2 `registro/`

| Archivo | Para qué sirve |
|---|---|
| `ESTADO.md` | **Empezar siempre aquí.** Una página que se reescribe en cada cierre: lo declarado, el muro, la tabla de la Escalera, el plan, los ERR del día, las decisiones pendientes. |
| `REGISTRO_etapas_1_2.md` | La historia completa, más de 7 600 líneas: cada experimento con su veredicto, sus números, sus reservas y su vocabulario. La jornada del 30 de septiembre empieza cerca de la línea 7360 y la del 1 de octubre cerca de la 7459. Los ERR están definidos dentro de las entradas. |
| `EQUIPO.md` | La misión, las reglas numeradas 1 a 15 y los roles de los agentes. |
| `HANDOFF.md` | Narrativa de traspaso entre sesiones: qué se hizo y por qué, día por día. |
| `RUTA.md` | La ruta de publicación: tesis aprobada, casillas, siguiente paso. |
| `PLAN.md`, `LABORATORIO.md`, `REFLEXION_agi.md`, `HORIZONTE_frontera.md` | Planes y reflexiones. |
| `CRITERIO_TRONCO_v2.md` a `v4.md` | Las versiones del examen que un organismo debe pasar para ser tronco. |

### 14.3 La pista, el juez y O1: `experimentos/carrera_escuderias/`

| Ruta | Qué hay |
|---|---|
| `pista.py` | El mundo: anillo, letras, costos, parto, muerte, fundador, pizarra. |
| `juez.py` | Las medidas: R0 real, cruzar, establecidos, causas de muerte. |
| `REGLAMENTO.md` | Las reglas de la carrera y sus seis enmiendas, con los ERR 95 a 102. |
| `carros/O1.py` | **El organismo que cruza.** 163 líneas. |
| `carros/CTRL_O1_SINLIMPIA.py`, `CTRL_O1_FUNDBORRA.py` | Los dos controles de O1: sin limpieza, y con la memoria del fundador borrada. |
| `carros/FABRICA.py` | El organismo de referencia de la carrera. |
| `revisa_carro.py`, `test_tramposo.py` | El revisor automático de trampas y la prueba del carro tramposo (ERR-96). |
| `identidad_pista.py` | El arnés que ata la pista al mundo original de la fase 9. |

El tronco en la pista está en `experimentos/tronco_v14_3/` (preregistro, informe, constructor y `corre_v143.py`, que es la función que usan casi todas las corridas posteriores).

### 14.4 La Escalera: `experimentos/organelos/escalera/`

| Ruta | Qué hay |
|---|---|
| `ESCALERA.md` | El plan completo: reglas de la Escalera, todos los peldaños, estado de cada uno. |
| `BITACORA.md` | El diario de las pruebas rápidas. Nada de ahí se declara. |
| `PREREGISTRO_p1.md`, `PREREGISTRO_p7.md`, `PREREGISTRO_p10.md` | Los preregistros de memoria de lugar, señal e ir a lo menos visitado. |
| `mundo_escalera.py` | El mundo con oasis. |
| `mundo_tramo_c.py` | El mundo con oasis más mudanza, costo de emitir, letras nuevas y cerrojo. |
| `construye_p1.py`, `construye_p7.py`, `construye_c.py` | Los programas que arman los organismos por anclas. |
| `carros/` | Los organismos armados: `O1_LUGAR.py` (memoria de lugar), `O1_LUGAR_SENAL.py` (señal), `O1_LUGAR_PREG.py` (ir a lo menos visitado), y sus controles terminados en `_BAR` (antípoda) y en `0` (apagado, para el arnés). |
| `corre_p1.py`, `corre_p7.py`, `corre_p10.py` | Los corredores, con la regla de decisión escrita como código. |
| `identidad_p*.py` y sus `_salida.txt` | Los arneses y su resultado. |
| `juntos/` | "Los tres juntos": preregistro, constructor y datos. |
| `mixto/` | PISA: `PREREGISTRO_pisa.md`, `construye_pisa.py`, la sonda `sonda_nl.py`, el nulo `nulo_pisa.py`. |
| `p8/` | Celda retenida: `PREREGISTRO_p8.md`, `carros/O1_LUGAR_COMP2.py`. |
| `sondas/` | Las sondas de P8 y de P9 ("¿hay espacio?"): `PREREGISTRO_sondas.md`. |
| `perillas/` | **Perillas:** `PREREGISTRO_perillas.md`, `construye_perillas.py`, `corre_perillas.py`, `nulo_perillas.py`, `identidad_perillas.py`. |
| `regimen/` | La sonda de por qué la selección deja el mundo pelado. Exploratoria. |

### 14.5 El muro y la selección: `experimentos/organelos/`

| Ruta | Qué hay |
|---|---|
| `muro_perillas/` | **El mapa del muro:** `PREREGISTRO_muro_perillas.md`, `mapa.log` a `mapa4.log`, el organismo `O1_MURO_GEN`, y el corredor del experimento siguiente (construido, sin correr). |
| `o1_evo/` | O1 con cuatro perillas heredables. Subcarpeta `grande/`: el primer mundo con oasis, donde nadie lo usaba. |
| `condiciones/entre_linajes/`, `mutacion/`, `genoma/` | Los tres diagnósticos de la junta del 30 de septiembre. |
| `condiciones/moneda_muro/` y `moneda_muro_rep/` | La moneda del muro: la exploración y la réplica que no replicó (ERR-177). |
| `moneda/` | El primer experimento de la moneda (indeterminado). |
| `termo/` | TERMO, el termostato diseñado. |
| `reunion/` | "La selección encuentra el termostato en la pista". |
| `termo_evo/`, `termo_banco/`, `termo_organo/` | Trabajo relacionado con el termostato. |
| `patas_muro/`, `veto_muro/`, `sentidos_muro/`, `dinamita/`, `pista_pob/`, `muro/` | Los intentos contra el muro (sección 8). |
| `enriquecido/`, `baldwin/`, `baldwin_exp/` | Mundo enriquecido y los dos de plasticidad. |
| `bloques/` | **BLOQUES**, el órgano de rechazo. El preregistro está en `bloques/opusM/`. |
| `eco_sel/`, `eco_sel_ing/`, `eco_sel_largo/` | La selección en ECO. |
| `frio/`, `frio_carrera/` | El arranque en frío y su intento (fallido) de traslado a la pista. |
| `eco_a_carrera/`, `eco_ing_a_carrera/` | Los trasplantes de ECO a la pista (negativos). |
| `boca_buena/` | El desarme exploratorio que dio origen al termostato. |
| `reactor/` | La sonda del motor para poblaciones grandes. |
| `darwin/`, `cruce/`, `gramatica/`, `ohno/`, `anfitrion/`, `codigo/`, `prometeo/` | Líneas del 24 y 25 de septiembre, casi todas cerradas. |

El mundo ECO está en `experimentos/juaco_eco/`. El índice general de experimentos, en `experimentos/INDICE.md`.

### 14.6 Las fases anteriores

En `experimentos/` hay además decenas de carpetas de las fases 1 a 10 (`nivel…`, `subida_n…`, `etapa…`). Las que más se citan: `nivel09_cuerpo_nuevo_b2/` (el organismo de la fase 9, de donde sale la pista), `nivel11_mundo_vivo/` (donde nacen las dos necesidades y las cuatro letras), `etapa5_comunicacion/` (la transmisión entre experto y novato, y los intentos de que el significado surgiera solo).

### 14.7 `exploratorio/`

| Ruta | Qué hay |
|---|---|
| `LEEME.md` | La advertencia: nada de aquí es resultado declarado. |
| `investigacion_20261001/F0_relojes.md`, `AUDITORIA_F0.md` | El reloj. |
| `investigacion_20261001/FABLE_gen_perdido.md` | La hipótesis del bien público. |
| `investigacion_20261001/FABLE_bloques_autoentrenables.md` | Reflexión sobre bloques que aprenden solos. |
| `investigacion_20261001/alejo/ALEJO.md` | El documento de arranque de Alejo. |
| `investigacion_20261001/red_celulas/INFORME.md`, `INFORME_2.md`, `INFORME_3.md` | La red de células y el bloque junto a un modelo congelado. |
| `investigacion_20261001/red_celulas/hamburguesa/INFORME_HAMBURGUESA.md` | La hamburguesa. |
| `investigacion_20261001/red_celulas/dim40/INFORME_DIM.md` | Las cuarenta dimensiones. |
| `investigacion_20261001/ENTREGA_1_reactor.md` y borradores `PREREGISTRO_F1_reactor_BORRADOR*.md` | El Reactor. |
| `investigacion_20261001/REVISION_organelos_soloLectura.md` | La revisión independiente de la rama. |

### 14.8 Cómo encontrar la prueba de una cifra

1. Buscar el resultado en `registro/ESTADO.md`.
2. Ir a su entrada en `registro/REGISTRO_etapas_1_2.md`: allí están el preregistro, el identificador del commit y la huella de los archivos de resumen.
3. En la carpeta del experimento, los crudos están en `datos/` y el veredicto que imprimió el programa en los archivos `.log` y `resumen.json`.
4. Si la cifra es de una prueba rápida, estará en `BITACORA.md` o marcada como "exploratorio": no es un resultado.
