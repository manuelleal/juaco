# PREREGISTRO — DISECCIÓN de HUMO (nube, 6-oct-2026; escrito ANTES de correr)

Misión: llegar a la AGI por este camino. Es el paso 1 del plan aprobado por el director ("ya arranca"): saber qué pieza de HUMO cruza el
muro, para dársela después a la selección desde cero (paso 2). HUMO cruza con mayoría en 19/20 y 20/20 (`PREREGISTRO_examen_grande.md`).

## 0. Corrección previa (declarada)
El LEEME del humo y el `INFORME.md` de la serie describen HUMO como "limpieza con piso + llenar al tope + no perseguir lejos". Al leer el
código completo aparece **una cuarta pieza que nadie había nombrado: una CULTURA COMPARTIDA por la pizarra pública.**
- Cada cuerpo publica, por turno, el valor medio de hasta 2 letras que conoce. La letra va como un código numérico (`ord`).
- Cada cuerpo lee la pizarra y adopta los valores de letras que no ha mordido.
- Un fundador sin memoria arranca así sabiendo lo que el resto del monocultivo ya aprendió.
- O1 no escribe ni lee la pizarra (O1.py, l. 21).
- La interfaz lo permite: no es una trampa del filtro ni del simulador. Pero es un canal entre linajes, y en un monocultivo los 9 son
  copias, así que funciona como cooperación.

## 1. Pregunta
¿Cuál de las cuatro piezas de HUMO es necesaria para cruzar el muro, cuál sólo suma y cuál sobra?

## 2. Brazos (`diseccion/programas/`; cada ablación cambia 1–2 líneas, diff en el repo)
| brazo | cambio | sha12 |
|---|---|---|
| HUMO | ninguno (referencia) | 69fcfcb2473f |
| KO_RECICLA | `_reciclable` devuelve siempre False: nunca muerde lo malo conocido para renovar el mundo | 46d85155fe5d |
| KO_BANCO | `banco = False`: sin el modo "en zona de reproducción no explores, no limpies, no vayas lejos" | 1ea29d0db707 |
| KO_CAP | `CAP = 1.25` en lugar de 1.5: llena hasta el umbral de la raíz y no hasta el tope real | c8cb69d88184 |
| KO_PIZARRA | `_escucha` y `_difunde` vacíos: ni publica ni lee | 965aaec1e366 |

Los cinco pasan el filtro de reglas. El script se niega a correr si un sha no coincide.

## 3. Instrumento y semillas
- `corre_diseccion.py` con `corre_carro.py` (pista y juez sin tocar; fundador NO limpio; T 100 000). Pool 3.
- Serie **277001–277010**; réplica **277011–277020**. Las dos se corren, porque cuestan 0 USD de modelo (~1.2 h cada una). Grep del
  6-oct: 2770xx no aparece como semilla.

## 4. LA LETRA (por tanda de 10 semillas; mayoría = cruzan_real ≥ 5/9)
**Validez:**
- V1: 50/50 corridas.
- V2: HUMO con mayoría en ≥ 8/10. Dio 39/40 en el examen grande.

**Clase de cada pieza** (se mira su ablación):
- **NECESARIA:** el KO tiene mayoría en **≤ 5/10**.
- **CONTRIBUYE:** no es necesaria, y el KO cruza **menos** linajes que HUMO en **≥ 7/10** semillas (pareado; los empates no cuentan).
- **SOBRA:** todo lo demás.

**Bloque:** una pieza se declara con su clase si serie y réplica coinciden; si no, vale la clase menor (NECESARIA > CONTRIBUYE > SOBRA).

## 5. Predicciones (antes de correr)
| pieza | NECESARIA / CONTRIBUYE / SOBRA |
|---|---|
| RECICLA | 0.65 / 0.25 / 0.10 |
| PIZARRA | 0.25 / 0.45 / 0.30 |
| BANCO | 0.10 / 0.35 / 0.55 |
| CAP | 0.10 / 0.30 / 0.60 |

**Razón:** quitar la limpieza a O1 lo hace colapsar (CTRL_O1_SINLIMPIA 0/9), así que espero lo mismo en HUMO. La pizarra es mi apuesta
para la ventaja sobre O1, porque el muro es el establecimiento del fundador. Ninguna predicción decide el veredicto.

## 6. Qué sigue según el resultado (paso 2, con preregistro aparte)
- Las piezas NECESARIAS y CONTRIBUYE se convierten en genes heredables que arrancan apagados, en el montaje de selección que ya funcionó
  (BLOQUES o perillas).
- Si la PIZARRA resulta NECESARIA o CONTRIBUYE, la pregunta del paso 2 cambia: ¿la selección puede sostener un canal cooperativo entre
  linajes? Es la hipótesis del bien público que tiene abierta `ESTADO.md`.

Costo: 0 USD de modelo. Siguiente ERR libre: ERR-196.

Firmado: Claude (sesión nube), 6-oct-2026, antes de correr.
