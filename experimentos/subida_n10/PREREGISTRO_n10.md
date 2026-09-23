# PREREGISTRO n10: la familia que hereda en vida (niveles 10–13, pieza "familias heredan vivas")

**Misión:** llegar a la AGI por este camino.
**Autor:** creador del equipo del nivel 10, 23-sep-2026. Escrito DESPUÉS de un humo en semilla de práctica (12391) y ANTES de cualquier serie.
**No apunta al tronco.** Es un bloque de nivel (10–13). No toca archivos congelados. Nada de `experimentos/generaciones/` se edita: se importa con sha fijado.

## 1. Hipótesis
En el mundo con capacidad de carga (pista v2, generaciones que conviven, quimiostato), el organismo real del proyecto (FABRICA = mitad cerebro del brazo REL de `organismo_f9c`) **perdió su único canal de herencia**. Su nodo se llenaba al morir el padre, y en v2 ningún cuerpo nace de un muerto (`generaciones/INFORME_CONVIVE.md`: "FABRICA pierde su nodo REL").

**H-n10:** si el nodo viaja en el parto, desde el padre vivo, el éxito reproductivo de los hijos (R0 de los nacidos) sube por el **contenido** del mensaje y no por el canal. Se predice que sube en monocultivo y que la familia no llega a sostenerse (H-1 sigue en pie).

## 2. Mecanismo mínimo (memoria nueva: CERO)
- **Qué recibe el hijo:** en `al_parir`, el padre vivo entrega lo que él heredó (`self._nodo`) más sus últimas `NODO_K = 20` mordidas. Son las mismas que `muere()` añade al nodo en v1.
- **Cómo lo lee:** en `nace`, el hijo instala el mensaje como su nodo y lo lee con la regla de F9, sin cambios: relevancia viva (`nodo_rel = 1`), `NODO_LEE = 50`, vía lenta.
- **Fundadores:** siguen limpios (ENMIENDA 5).
- **Sin constantes nuevas.**

| carro | MODO | papel |
|---|---|---|
| `FAMILIA_NADA` | nada | == FABRICA bit a bit (piso; hereda = 'nada') |
| `FAMILIA_PARTO` | parto | **candidato** |
| `FAMILIA_BAR` | bar | control de **contenido**. Mismo canal, mismos patrones, mismas necesidades, misma multiset de R. Las R se permutan entre mensajes, como `nodo_baraja` de F9/ALMA2. El rng es propio (`[860000] + entropía de rng_hijo`) y no consume ningún rng del mundo, del cuerpo ni del hijo (arnés B2). |
| `FAMILIA_ORACULO` | oraculo | **techo**: tabla verdadera (patrón, necesidad) → R, en `NODO_LEE` copias, por el mismo canal y con la misma lectura (como `nodo_or` de F9C) |

## 3. Instrumento y anclas
- **Construcción:** `construye_familia.py`, 6 anclas sobre `carrera_escuderias/carros/FABRICA.py` (sha `2ebee3e99ea5a33a`; sólo se lee).
- **Carros resultantes:** NADA `f7ae98715f170153`, PARTO `e8aeb6efd6307162`, BAR `46c09162e6d1ab55`, ORACULO `55df592f57671b54`. Entre ellos cambia UNA línea (`MODO`).
- **Mundo:** `generaciones/pista2.py` `4d2bee16e7961261` + `motor_convive.py` `d10cb9021f5d0f41`, con `solapadas=1`, `reposicion='fija'`, `r_rep = 0.03`, tope 300, sin cambios.
- **Juez:** `resumen_linaje` de `corre_convive.py` `e6dadfdad9c379cd` (importado, no copiado) más las medidas de esta pregunta en `corre_n10.py`. Sólo lee la física (ERR-96).
- **Arnés `identidad_familia.py` (`0fdd2599832e7e2c`): 26/26.**
  - (I) NADA == FABRICA en toda la salida en 6 configuraciones: v2 con quimiostato ×2, v2 con reposición inmediata, v1 con 9 carros, v1 con `fundador_limpio`, v1 `compat=1`.
  - (P) Antes del primer parto, los 4 modos son idénticos.
  - (B) Canal: BAR conserva las marginales y no consume rng; ORÁCULO recibe la tabla verdadera; la lectura mueve la vía lenta sólo si hay mensaje.
  - (D) Determinismo.
  - (C) En marcha.
- **Brazos:** 4 monocultivos (9 fundadores del mismo carro, L = 360, 36 objetos) y **MIX**: 3 NADA + 3 PARTO + 3 BAR en el mismo mundo (compiten por el mismo flujo de recurso).

## 4. Semillas (NUEVAS; verificadas con grep en `bundle` y en los worktrees `anclado`, `aprende`, `carrera`, `convive`, `criterio`, `escuela`, `exploracion`, `fanin`)
- Práctica: 12391–12399 (usadas: 12391–12393 en el arnés y el humo).
- **Serie: 12301–12320.**
- **Réplica: 12321–12340.**

`corre_n10.py` aborta con cualquier otro rango en `--serie`.

## 5. Medidas
- **Medida que decide:** `R0_nacidos` = hijos por cuerpo nacido (no fundador) de la cohorte t ≤ T/2. Se compara pareado por semilla.
  - Los que siguen vivos en T cuentan con los hijos que llevan. Es una cota inferior, conservadora contra el candidato si vive más.
- **Secundarias:**
  - `vida_nacidos` (mediana de los nacidos muertos);
  - `exceso` = cuerpos vivos por encima de 1 por linaje (t ≥ T/2);
  - `nac`;
  - `gen_max`;
  - `persiste_carro` (≥ 1 linaje sin fundadores tras t = 10000);
  - causas de muerte de los nacidos.
- **Por qué no el tamaño del carro:** en v2 un linaje extinto se repone con un fundador, así que `tam_carro` ≥ 9 por construcción. En el humo, el tamaño apenas separa los brazos: 9.48 / 9.64 / 9.50 / 11.11.

## 6. Criterio por la letra (umbral pareado ≥ 15/20; implementado en `corre_n10.veredicto`)
**Validez:**
- **V-ANCLA:** mediana de `R0_nacidos` de NADA en [0.00, 0.10] y NADA `persiste_carro` en ≤ 5/20. Si cae: **NO SE LEE**.
- **V-TECHO:** ORÁCULO > NADA en `R0_nacidos` ≥ 15/20. Si cae: **NO SE LEE COMO CAPACIDAD** (el contenido no tiene dónde actuar en este mundo).

**Puertas del candidato:**

| puerta | condición |
|---|---|
| F-1 | PARTO > NADA ≥ 15/20 |
| F-2 | PARTO > BAR ≥ 15/20 |
| F-3 | en MIX: PARTO > NADA ≥ 15/20 |
| F-4 | en MIX: PARTO > BAR ≥ 15/20 |

**Veredicto:**

| veredicto | condición |
|---|---|
| **FUNCIONA** | F-1..F-4 |
| **HAY ALGO MODESTO** | F-1 y F-2 |
| **HAY ALGO MODESTO SIN CONTENIDO** | sólo F-1 |
| **NO** | nada de lo anterior |

- **Informativos, no deciden:** C-BAR (BAR ≥ PARTO en ≥ 10/20: el control gana) y L-PERSISTE.
- **Declarar exige réplica:** la frase se declara sólo si la réplica 12321–12340 da el mismo veredicto o uno mejor. Si da uno peor, vale el peor.
- **Sin recalibración (ERR-94):** si una ancla cae, no se tocan umbrales.

## 7. Predicciones firmadas (serie 12301–12320, T = 100000; humo s12391 T = 20000 entre paréntesis)

| # | predicción | rango / resultado | p firmada |
|---|---|---|---|
| P1 | mediana de `R0_nacidos` de NADA (0.020) | [0.00, 0.10] | 0.85 |
| P2 | mediana de `R0_nacidos` de PARTO (0.213) | [0.10, 0.35] | — |
| P2 | PARTO > NADA | ≥ 15/20 | 0.75 |
| **P3** (puede caer) | mediana de BAR (0.068) | [0.02, 0.12] | — |
| **P3** (puede caer) | PARTO > BAR | ≥ 15/20 | 0.60 |
| P4 | mediana de ORÁCULO (0.544) | [0.35, 0.80] | — |
| P4 | ORÁCULO > NADA | ≥ 15/20 | 0.90 |
| **P4b** (puede caer) | ORÁCULO `R0_nacidos` < 0.90 (el muro sigue en el mundo aun con la tabla verdadera) | en ≥ 15/20 semillas | 0.80 |
| P5 | razón `vida_nacidos` PARTO/NADA (1.66) | [1.2, 2.2] | — |
| **P6** (contra mí) | en MIX, PARTO > NADA ≥ 15/20 **NO** se cumple (humo invertido: 0.059 contra 0.25 con cohortes de 12–17) | predigo que no | 0.65 |
| **P7** (puede caer hacia arriba) | PARTO con `persiste_carro` = 0 | en ≥ 15/20 | 0.85 |
| P8 | `exceso` PARTO − NADA, mediana (0.16) | [0.0, +0.5] cuerpos | — |
| P9 | `gen_max` PARTO ≥ NADA (3 contra 2) | en ≥ 12/20 | — |

**Veredicto más probable según mis propias predicciones:** HAY ALGO MODESTO (F-1 y F-2 sí; F-3 no).

## 8. Controles y qué refuta
- **BAR** es el control que puede ganarle al candidato. Si BAR ≥ PARTO (C-BAR), lo que ayuda es la cautela genérica del canal (muchas R = −3), no el contenido. En ese caso no se declara transmisión.
- **NADA** también puede ganar: leer el nodo podría volver al hijo demasiado cauto y hacerlo parir menos. En el humo, PARTO tuvo 95 nacimientos contra 102 de NADA.
- **ORÁCULO** mide el techo. Si ni la tabla verdadera sube el R0 de los nacidos, la pregunta no tiene sentido en este mundo.
- **MIX** separa "vale en su propio mundo" de "vale compitiendo por el mismo recurso" (trampa del mundo que se come la comida: quimiostato con flujo fijo).
- **Refuta H-n10:** F-1 cae, o F-2 cae con C-BAR verdadero.

## 9. Cuatro trampas
1. **Canal simétrico:** el mensaje lleva R positivas y negativas de las dos necesidades, y BAR conserva sus marginales.
2. **Acierto sin balancear:** la medida es el éxito reproductivo, no un acierto.
3. **Mundo que se come la comida:** quimiostato con flujo fijo (ERR-104 corregido por la pista v2). En MIX, NADA, PARTO y BAR comparten ese flujo.
4. **Sitios fijos:** la reposición cae en una celda libre al azar con una letra al azar. No hay sitios fijos.

## 10. Vocabulario
**Permitido, si FUNCIONA o HAY ALGO MODESTO:** "en un mundo con capacidad de carga y generaciones que conviven, cuando el padre vivo pasa al hijo, en el parto, lo que heredó y sus últimas mordidas, los hijos tienen más hijos que sin ese mensaje y que con el mensaje barajado (X/20 semillas, replicado); ningún linaje se sostiene todavía: H-1 sigue en pie en este mundo".

**Prohibido:** "cultura", "enseña", "población", "evoluciona", "la familia se sostiene" (salvo que L-PERSISTE ≥ 15/20 con réplica), y citar `R0_nacidos` como si fuera el R0 del linaje (los fundadores no entran).

## 11. Puntos del nivel 10–13 (propuesta; decide el director; hoy ~10 %, propuesta pendiente 15 %)

| resultado | puntos |
|---|---|
| FUNCIONA replicado | **+8** (familias heredan contenido en vida y ganan compitiendo) |
| HAY ALGO MODESTO replicado | **+4** |
| MODESTO sin contenido | **+1** |
| NO / NO SE LEE | **0** (se cierra la línea "herencia del nodo en v2" y queda registrado dónde está el muro) |

Ningún resultado de este bloque lleva el nivel al 100 %: la familia que persiste (H-1 sin la reserva ERR-104) y el alma que le gana al azar quedan fuera.

## 12. Comandos (sólo el coordinador; Pool ≤ 6) y costo
```
python experimentos/subida_n10/identidad_familia.py                                   # 26/26 antes de todo (~2 min)
python experimentos/subida_n10/corre_n10.py --serie --desde 12301 --n 20 --pool 6     # serie
python experimentos/subida_n10/corre_n10.py --serie --desde 12321 --n 20 --pool 6     # réplica
```

**Costo, medido en el humo** (T = 20000, máquina con 12 procesos ajenos): 26–31 s por brazo y semilla.
- Por brazo y semilla a T = 100000: ~130–160 s.
- Por serie: 100 tareas ≈ 15 000 s de CPU (~4.2 h), **≈ 45–60 min con Pool 6**.
- Réplica: igual.

Esperar a que termine uno de los dos Pools en curso (regla de 2 Pools / 14 procesos).
