# PREREGISTRO n10c: la familia pasa SÓLO LO QUE IMPORTA (niveles 10–13, tanda 3; frente 2: ¿persiste un linaje?)

**Misión:** llegar a la AGI por este camino.
**Autor:** coordinador de la nube, 24-sep-2026, ~03:28 UTC. Se escribió DESPUÉS de los datos exploratorios (§0) y ANTES del arnés, del
humo y de cualquier serie. Si algo cambia después del humo, es "candidato a ERR".
**No apunta al tronco.** No toca archivos congelados ni los carros de n10b: sólo los carga y los subclasea (`carros_n10c.py`).

## 0. De dónde sale (EXPLORATORIO, no es dato; `experimentos/exploratorio_nube_20260924/NOTA_EXPLORATORIA.md`)
- **n10b dio FUNCIONA + ACUMULA ×2 por la letra.** RES obtuvo 0.688 y 0.737; NADA 0.114 y 0.122; ORÁCULO 0.520 y 0.545.
- **Con la alarma del §8 activada en las dos series:** RES > ORÁCULO en 20/20 y 18/20.
- **Hipótesis que la explica, H-NEUTRAS.** La tabla del ORÁCULO trae 8 entradas, 4 de ellas neutras (R = 0: la letra no toca esa
  necesidad). Por la vía lenta, cada neutra entrena a 0 el valor de esa letra en esa necesidad y borra la generalización protectora
  entre letras que comparten píxeles. Las tablas de RES suelen estar incompletas (6–7 claves) y a menudo no las traen.
- **Revisión exploratoria** (T 100 000, mediana de R0_nacidos):
  - Práctica 12794–12797:

    | carro | R0_nacidos |
    |---|---|
    | ORÁCULO | 0.530 |
    | RES | 0.714 |
    | **ORA_SIN0** (verdad sin neutras) | **0.997** |

  - Exploratorias 24001–24004:

    | carro | R0_nacidos |
    |---|---|
    | RES | 0.671 |
    | **RES_SIN0** (la familia sin neutras) | **0.960** |
    | ORA_SIN0 | 0.994 |
    | NADA | 0.092 |

- **La ventaja no es universal.** En 24005, RES_SIN0 da 0.901 y RES 0.897 (casi empate), y ningún linaje persiste en ninguno de los
  dos: 0 linajes sin extinción, más de 3300 fundadores repuestos por corrida. En 24006, RES_SIN0 da 0.941 y RES 0.601; tampoco persiste ninguno (3453 fundadores). En total, RES_SIN0 > RES en 6/6 semillas exploratorias (márgenes +0.26, +0.17, +0.28, +0.41, +0.004, +0.34), y la persistencia es 0 de 2 en los dos.
- **Un R0 de nacidos cerca de 1 NO es persistencia.** Con R0 ≤ 1 el linaje es un proceso de ramificación crítico o subcrítico: se
  extingue, y el mundo lo refunda (ERR-118). Los fundadores nacen sin tabla y casi no se reproducen (R0_fund ~0.1).

## 1. Hipótesis
**H-n10c:** si en el parto la familia pasa su tabla SIN las entradas neutras (sólo lo que le hizo bien o mal), los nacidos tienen más
hijos:
- que con la tabla completa de n10b (RES);
- que con la misma tabla sin neutras y con las R barajadas (BAR_SIN0: el contenido importa);
- compitiendo por el mismo flujo de recurso (MIX).

**Calificadores** (no deciden el veredicto base; se reportan en él):
- R0N-90: R0 de nacidos ≥ 0.90 en ≥ 15/20 semillas. **No es H-1**: H-1 exige además 0 fundadores.
- PER-c: el carro RES_SIN0 persiste (algún linaje sin fundadores tras t = 10 000) en ≥ 15/20 semillas.

## 2. Mecanismo mínimo (memoria nueva: CERO; constantes nuevas: CERO)
- Filtro en `nace()` del hijo: de la tabla recibida se quitan las entradas con R == 0. Las R son categóricas: +1, 0, −3. Todo lo demás
  queda igual que en n10b:
  - la misma tabla que arma el padre (lo vivido más lo heredado; `al_parir` sin tocar);
  - la misma dosis (NODO_LEE copias);
  - la misma lectura (relevancia viva, vía lenta).
- Como el hijo instala la tabla sin neutras y la vuelve a pasar enriquecida con lo que vive, la acumulación de n10b se conserva.

| carro | qué es | papel |
|---|---|---|
| NADA | FAMB_NADA (== FABRICA) | piso y ancla |
| RES | FAMB_RES de n10b | comparador (la tabla completa) y segunda ancla |
| **RES_SIN0** | FAMB_RES + filtro | **candidato** |
| BAR_SIN0 | FAMB_BAR + filtro ANTES de su permutación | control de contenido que puede ganar |
| ORA_SIN0 | FAMB_ORACULO sin sus 4 entradas neutras | referencia (la verdad que importa); informa, no decide |

BAR_SIN0 tiene las mismas claves, la misma multiset de R, la misma dosis y el mismo número de entradas que RES_SIN0; sólo están
barajadas las R.

## 3. Instrumento
- `corre_n10c.py` importa `corre_n10b.py` (b7808bbb83fb038e) y usa sus funciones `tarea`, `agrega` y `pareado` sin tocarlas. El
  mundo, el juez y las medidas son los de n10b:
  - `pista2` 4d2bee16e7961261 y `motor_convive` d10cb9021f5d0f41;
  - `solapadas=1`, reposición `'fija'`, r_rep 0.03, tope 300, T = 100 000;
  - juez: `corre_convive` e6dadfdad9c379cd.
- Sólo se reasigna QUÉ carros se cargan: `corre_n10b.carga`, `MONO`, `MIX`, `PARES` y `PARES_MIX`, en el proceso y en cada worker.
- Carros: `carros_n10c.py` (**67f149c81f880cb1**). El sha quedó fijado en `corre_n10c.SHA_CARROS_N10C` tras el arnés y antes del humo.
  - El arnés atrapó un bug ANTES del humo, y se corrigió. `base()` cargaba vía `corre_n10b.carga`, que corre_n10c reasigna: eso daba
    una recursión infinita. Ahora carga el archivo del carro por ruta, con el mismo código que `corre_n10b.carga`.
  - Fue un error de construcción, no un cambio de criterio.
- Arnés: **16/16** (03:32 UTC, 95 s), salida en `identidad_n10c_salida.txt`.
- **Arnés `identidad_n10c.py`, antes del humo:**
  - (I) filtro apagado == carro base, bit a bit, en toda la física (3 pares × 2 semillas);
  - (F) el filtro quita exactamente lo neutro;
  - (O) ORA_SIN0 = las 4 entradas no neutras de la verdad;
  - (T) ningún hijo de RES_SIN0 ni de BAR_SIN0 instala una entrada neutra;
  - (E) `corre_n10c.tarea` == `corre_n10b.tarea` en NADA y RES;
  - (D) determinismo;
  - (R) el parser aborta ante banderas malas y un subproceso con bandera desconocida no escribe nada (ERR-115).

## 4. Semillas NUEVAS (grep del 24-sep en preregistros y corredores: ninguna se usa)
- Práctica: **12891–12899** (arnés 12892–12893; humo 12891).
- Serie: **12801–12820**.
- Réplica: **12821–12840**.

`corre_n10c.parsea` rechaza cualquier otra.

## 5. Medidas
**Decide:** `R0_nacidos`, con la misma definición que n10b: hijos por cuerpo nacido (no fundador) de la cohorte t ≤ T/2, pareado por
semilla.

**Secundarias:**
- `persiste_carro` y `linajes_sin_ext` (juez de convive: 0 fundadores tras t = 10 000);
- `vida_nacidos`, `nac`, `exceso`, `gen_max`;
- `frac_mala_nacidos` (fracción de muertes de nacidos por veneno o sal): es el mecanismo, y H-NEUTRAS predice que baja.

**Telemetría del carro** (informa; ERR-96): claves de la tabla instalada, fracción con B|hambre = −3, D|sed = −3, y A o C marcadas malas.

## 6. Criterio por la letra (umbral pareado ≥ 15/20; implementado en `corre_n10c.veredicto`)
**Validez** (si cae cualquiera: NO SE LEE):
- V-ANCLA-c: mediana de R0_nacidos de NADA en [0.085, 0.135], y NADA persiste_carro ≤ 5/20. Es la misma ancla de n10b (ERR-116).
- V-RES-c: mediana de R0_nacidos de RES en [0.60, 0.82]. n10b dio 0.688 y 0.737 con el mismo instrumento; si cae, el mundo o el
  instrumento no son los de n10b.

**Puertas:**

| puerta | condición |
|---|---|
| S-1 | RES_SIN0 > RES en R0_nacidos ≥ 15/20 |
| S-2 | RES_SIN0 > BAR_SIN0 ≥ 15/20 |
| S-3 | MIX: RES_SIN0 > NADA en el mismo mundo ≥ 15/20 |
| S-4 | MIX: RES_SIN0 > BAR_SIN0 en el mismo mundo ≥ 15/20 |

**Veredicto:**

| veredicto | condición |
|---|---|
| **FUNCIONA** | S-1..S-4. Se le añade " + R0 DE NACIDOS ≥ 0.90" si R0N-90 y " + PERSISTE" si PER-c |
| **HAY ALGO MODESTO** | S-1 y S-2, con los mismos añadidos |
| **NO** | otro caso |

- **Informativos:** ORA_SIN0 > RES_SIN0 (semillas); persiste_carro por brazo; BAR_SIN0 contra NADA; frac_mala_nacidos RES_SIN0 contra RES.
- **Declarar exige réplica** (12821–12840) con el mismo veredicto o uno mejor. Si da uno peor, vale el peor.
- **Sin recalibración.**

## 7. Predicciones firmadas (serie 12801–12820)

| # | predicción | rango / resultado | p firmada |
|---|---|---|---|
| P1 | mediana de NADA | [0.085, 0.135] | 0.95 |
| P2 | mediana de RES | [0.60, 0.82] | 0.85 |
| P3 | mediana de RES_SIN0 | [0.82, 1.02] | 0.75 |
| **P4** (puede caer) | S-1: RES_SIN0 > RES | ≥ 15/20 | 0.75 |
| P5 | S-2 | ≥ 15/20 | 0.90 |
| P5 | mediana de BAR_SIN0 | [0.03, 0.30] | — |
| P6 | S-3 | ≥ 15/20 | 0.85 |
| P6 | S-4 | ≥ 15/20 | 0.85 |
| **P7** (puede caer) | R0N-90 | ≥ 15/20 | 0.45 |
| **P8** (contra mí) | PER-c | ≥ 15/20 | 0.05 |
| P8 | RES_SIN0 persiste_carro | ≤ 5/20 | 0.85 |
| P9 | frac_mala_nacidos: RES_SIN0 < RES | mediana | 0.85 |
| P10 | ORA_SIN0 > RES_SIN0 | en ≥ 10/20 | 0.65 |

**Veredicto más probable según mis propias predicciones:** FUNCIONA, sin PERSISTE. R0N-90 queda casi a cara o cruz.

## 8. Controles y qué refuta
- **BAR_SIN0:** con el mismo número de entradas y la misma dosis, separa "menos entradas" de "contenido". Si BAR_SIN0 ≥ RES_SIN0, la
  ganancia no es el contenido. Ojo: BAR_SIN0 puede marcar mala la comida (A o C = −3) y dañar; por eso "por contenido" exige S-1 **y**
  S-2.
- **RES:** si RES ≥ RES_SIN0 (S-1 cae), H-NEUTRAS no se sostiene en semillas nuevas.
- **MIX** comparte el flujo del quimiostato.
- **Refuta H-n10c:** S-1 o S-2 caen.
- **Refuta el mecanismo (informativo):** frac_mala_nacidos de RES_SIN0 ≥ la de RES.

## 9. Cuatro trampas
1. **Dosis:** RES_SIN0 lee sus NODO_LEE copias sobre menos entradas distintas. BAR_SIN0 lo iguala; la dosis no puede explicar S-2.
2. **El filtro usa R == 0 exacto.** Las R son categóricas (+1, 0, −3); el arnés (F) lo comprueba.
3. **Mundo que se come la comida:** quimiostato de flujo fijo, sin cambios; ERR-104 está resuelto por construcción.
4. **Fundadores repuestos (ERR-118):** R0_nacidos no cuenta fundadores, y la persistencia se reporta aparte. No se escribe
   "persiste" ni "se sostiene" sin PER-c.

## 10. Vocabulario
**Permitido si FUNCIONA:** "en un mundo con flujo fijo de comida y generaciones que conviven, cuando la familia pasa en el parto sólo lo
que le hizo bien o mal (sin lo neutro), los nacidos tienen más hijos que con la tabla completa y que con la misma tabla barajada,
también compitiendo en el mismo mundo (X/20, replicado)".
- Con R0N-90: "… y el R0 de los nacidos llega a ≥ 0.90 en X/20 semillas".
- Sin PER-c se añade: "ningún linaje se sostiene sin fundadores repuestos".

**Prohibido:** "cultura", "enseña", "la familia se sostiene" (salvo PER-c), "cruza H-1", "evoluciona", "población".

## 11. Puntos del nivel (propuesta; decide el director)
Es una mejora de la pieza de herencia de n10b en el mismo nivel. Como propuesta:

| resultado | puntos |
|---|---|
| FUNCIONA replicado | +3 |
| R0N-90 replicado | +2 |
| PER-c replicado | +5 |
| MODESTO | +1 |
| NO | 0 (H-NEUTRAS queda como explicación de la alarma de n10b, sin más) |

## 12. Comandos y costo
**Sólo el coordinador ejecuta; nunca `--serie` desde un agente (ERR-115).**
```
/root/venv-juaco/bin/python experimentos/subida_n10c/identidad_n10c.py                                  # N/N antes de todo
/root/venv-juaco/bin/python experimentos/subida_n10c/corre_n10c.py --humo                               # 12891, T 20000, 6 brazos
/root/venv-juaco/bin/python experimentos/subida_n10c/corre_n10c.py --serie --desde 12801 --n 20 --pool 3
/root/venv-juaco/bin/python experimentos/subida_n10c/corre_n10c.py --serie --desde 12821 --n 20 --pool 3
```
**Costo:** 120 tareas por serie, como n10b. En la nube, n10b tardó 2796 s de pared con Pool 3, unos 47 min. Con Pool 1 serían unas 2.5 h.
