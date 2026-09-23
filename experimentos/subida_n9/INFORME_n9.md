# INFORME — subida del nivel 9: ¿el modelo de sí es causal en el linaje que cruza H-1? (creador, 23-sep-2026)

**Veredicto de la entrega: paquete LISTO PARA SERIE. No hay dato: sólo arnés 22/22 y dos humos de una semilla (sin valor).**
Nada commiteado, sin Pool, sin tocar congelados ni carpetas ajenas. Todo está en `experimentos/subida_n9/`.

## Qué elegí y por qué
La propuesta de subir el nivel 9 de 50 a 65 % se apoya en O3 y O4 (carrera de escuderías, ronda 2). Pero sus políticas las
escribió un LLM, y **nadie midió si lo que las hace cruzar es leerse a sí mismas**. Este bloque mide eso con lesiones sobre O3,
el ganador replicado. Es la pieza "modelo de sí" del nombre del nivel, y es lo que sostiene o tumba el 65 %.
Descarté cuatro caminos:
- **Reescribir F9-4:** sería recalibrar después de ver los datos.
- **"La boca lee las dos filas":** en la fase 10 ya hundió al inmortal.
- **Generaciones:** las está corriendo el coordinador.
- **Un modelo de sí aprendido:** con fundador limpio, el linaje nunca ve su propia extinción. No puede aprender cuándo le
  conviene morir (sesgo de supervivencia). Queda anotado.

## Qué hice
- **Construcción:** `construye_n9.py`, por anclas en bytes sobre `O3.py` (0442c2884fcb0e11). Salen seis carros:
  - `O3`: copia exacta.
  - `O3_LES_OFF`: el instrumento de lesión con las perillas apagadas.
  - `O3_LES_SI`: decide con el (E, Ag) de un paso pasado al azar, tomado de los últimos 2000 pasos del linaje.
  - `O3_TERM_CIEGO`: `COLA_TERM` pasa de 4 a 0; la muerte programada deja de leer la reserva del linaje.
  - `CTRL_O3_SINTERM`: tiene el mismo sha que el control de `generaciones`.
  - `FABRICA`: copia, sólo para la identidad corta del juez.
- **Piezas que se reutilizan sin editarlas:** la pista y el juez de la ronda 2 (`comun_n9.py` sólo cambia `P.CARROS`).
- **Arnés `identidad_n9.py`: 22/22.** `O3_LES_OFF` es igual a `O3` bit a bit en toda la salida de `pista.run`: tres monocultivos
  y una pista mixta, T = 12000, con fundador limpio. TERMINAL se disparó 49 veces. El arnés cubre además:
  - la identidad corta del juez;
  - el chequeo estático;
  - que las lesiones no son inertes;
  - que la marginal de L-SI está igualada.
- **Runner `corre_n9.py`:**
  - Antes de correr revisa shas, construcción, chequeo estático, identidad corta y una mini identidad (s13399).
  - Aplica la letra de las ENMIENDAS 5 y 6 tal cual; encima calcula los pareos por semilla, la regla "pierde" (§5) y las
    predicciones P1–P7.
  - Escribe el crudo antes de resumir.

## Qué falló (declarado)
- **L-COLA:** mi primera lesión de la reserva (la cola del linaje sorteada paso a paso) **falló el chequeo de marginal del arnés**.
  La muerte programada parpadea y cae a 0.33 de la tasa real, así que **la descarté antes de cualquier humo** y la reemplacé por
  `O3_TERM_CIEGO`.
- **Historia desde el nacimiento:** la primera versión de L-SI sorteaba desde el nacimiento del cuerpo y sesgaba hacia la
  juventud (E 0.91 contra 1.01). La cambié a la ventana del linaje.
- **Marginal en el humo (enmienda 1, V-M):** en régimen de colapso, la marginal de L-SI vuelve a separarse (E 0.795 contra
  0.944). V-M es condición de lectura, no puerta. Con tope 0.10, el humo la **incumple**. Primero puse 0.15, que era el valor
  del humo más un pelo: lo retiré por estar ajustado al dato.
- **Frase retirada:** "misma distribución" queda sin garantía cuando el linaje colapsa.
- **Versión del runner:** los dos humos se escribieron con el runner anterior a ese cambio de tope (sólo cambia una etiqueta
  impresa).

## Humo (un proceso, semilla 13391, T = 12000, 6 corridas en total, 72 000 pasos; sin valor)
Archivos:
- `datos/humo/n9_humo_s13391_T12000_20260923_160150{.json,.log,_resumen.json}`: los 4 brazos, 142 s en total.
- `..._160507*`: O3 y O3_LES_SI con el runner final antes del cambio de tope, 69 s.

| brazo | muertes (9 linajes) | persisten | nacimientos reales (mediana) | R0 real eval | sin parir | causas h/s/v/sal |
|---|---|---|---|---|---|---|
| O3 | 28 | 0/9 | 3 | 0.333 | 0.5 | 11/7/6/4 |
| O3_LES_SI | 106 | 0/9 | 0 | 0.0 | 1.0 | 3/3/50/50 |
| O3_TERM_CIEGO | 45 | 3/9 | 3 | 0.556 | 0.25 | 7/9/13/16 |
| CTRL_O3_SINTERM | 28 | 0/9 | 3 | 0.333 | 0.5 | 11/7/6/4 (idéntico a O3: TERMINAL no se disparó antes de t = 12000) |

Controles del humo: coherencia física 36/36, t_fund reconstruible 36/36, 0 escrituras en la pizarra.
Lo que el humo sí muestra:
- **ERR-103 en vivo:** el clasificador físico llama "voluntarias" a 81 de 106 muertes de un cuerpo lesionado.
- **P4, dirección:** O3_TERM_CIEGO va en la dirección que yo predije para refutarla (persiste más a corto plazo).
- **Ancla:** a T = 12000 el ancla no es evaluable; hacen falta 100 000 pasos.

## Qué queda (para el coordinador)
- **Serie:** `python experimentos/subida_n9/corre_n9.py --serie --desde 13301 --n 20 --pool 6`
- **Réplica:** `python experimentos/subida_n9/corre_n9.py --serie --desde 13321 --n 20 --pool 6`
- **Costo:** 80 tareas por serie, de 240 a 400 s de CPU cada una. Son 5.3–8.9 h de CPU y ~1–1.5 h de reloj con Pool 6, por serie.
- **Antes:** `python experimentos/subida_n9/identidad_n9.py` tiene que dar 22/22 (~7 min).
- **Candidato a ERR:** la métrica de R0 real y el clasificador de muerte voluntaria (ERR-102/103) no distinguen "morir en el
  momento" de "morir más". La serie da el primer número que los separa (O3 contra O3_TERM_CIEGO).
- **Puntos (propuesta, decide el director):**

| resultado | puntos |
|---|---|
| FUNCIONA | +10 |
| HAY ALGO MODESTO, sólo por H-SI | +3 a +5 |
| HAY ALGO MODESTO, sólo por H-RES | +5 |
| NO | 0, y recomiendo bajar la propuesta de 65 a 55 % |

## Refutado y no verificado
- **Refutado por mí antes de la serie:** que la cola sorteada paso a paso iguala la tasa de muerte programada (L-COLA: 0.33).
  También que la historia del cuerpo da la misma marginal.
- **No verificado:**
  - si la serie en 100 000 pasos repite la marginal del arnés o la del humo;
  - el tiempo real por tarea con los dos Pools del coordinador en marcha;
  - que MANIFEST.txt, que aparece modificado en el árbol, no es mío. Mis scripts no lo escriben; no corrí `manifiesto.py`.
