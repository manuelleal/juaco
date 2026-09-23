# INFORME — subida_n6b (creador, nivel 6, tanda 2; 23-sep-2026). Una página

**Estado: LISTO PARA SERIE.** No hay resultado: un humo de una semilla no es dato. **Aviso previo:** R-4 cae en el humo
(0.552). Si cae también en la serie, el techo por la letra es **HAY ALGO MODESTO**.

Misión: llegar a la AGI por este camino; el método manda sobre el cómo.

## Qué hice
1. **Elegí el bloque que ataca tres de los cinco faltantes a la vez**: V1 (mapa completo), dos metas en 2D y el port al
   tronco v14.2.
   - Hallazgo al releer la réplica sellada de subida_n6 (`af98c6148285a2be`): V1 no es sólo validez. En 6629, 6632 y
     6639, con la muralla incompleta en M, GF rodeó **0.0**. La mediana lo tapaba.
2. **Port a v14.2 por anclas.** `construye_subida_b.py` copia el delta v13 → v14.2 del tronco congelado (12 trozos, cada
   uno verificado tal cual en `organismo_v142.py`) sobre `mundo_subida.py`.
   - I-142: con los kwargs del tronco leídos con `inspect` y el mundo apagado, el resultado es bit a bit
     `organismo_v142.run`.
   - I-13: con las perillas apagadas, es bit a bit subida_n6.
3. **Mecanismo candidato: explora.** Saciado (`E ≥ 1`) y con la retina vacía, sube hacia la celda vecina que M no
   conoce. La celda pisada y vacía queda conocida en M.
   - Memoria nueva: cero. Constantes nuevas: cero (usa `gamma_M`).
   - En la prueba no actúa (`E_test = 0.3`).
   - Nació de una depuración: la **vista sola** (escribir en M lo que se ve a un paso) no completó el mapa, porque el
     organismo sólo iba y venía a una comida.
4. **Prueba de dos metas en el mundo partido.** Las salidas se clasifican por BFS del mundo real en dos clases:
   - *cruza*: la más cercana por camino está al otro lado; hay que rodear;
   - *desvía*: la más cercana por camino está del mismo lado, pero la otra queda más cerca en recta. Es una trampa.
5. **Arnés `identidad_subida_b.py`: RESULTADO: 75/75** (`bed318363156a827`):
   - 45 identidades I-13 y 9 I-142;
   - 15 controles que deben diferir;
   - 6 revisiones de clases con un BFS independiente, que también comprueba que el toro queda partido (ERR-117).
6. **Runner `corre_subida_b.py`.** Tiene 11 brazos y 13 puertas, y compara las entradas campo a campo contra subida_n6
   (regla 14). **Aborta** ante banderas desconocidas o abreviadas (ERR-115), ante semillas fuera de 14601–14640 y si el
   sha del mundo o del tronco cambió. Al final **imprime el veredicto por la letra**; con `--lee_replica` da la letra
   combinada.
7. **Humo** (semilla 14641, 6 corridas, T = 100 000, un proceso, 229 s). JSON
   `experimentos/subida_n6b/datos/humo/subida_b_humo_20260923_183110.json` (`0377b2a258056ea2`).

| brazo | limpio cruza / desvía | M (comidas / venenos) | comida | muertes |
|---|---|---|---|---|
| CIEGO | 0.0 / 0.05 | — | 1 240 | 6 |
| GF (subida_n6) | 1.0 / 0.75 | 1/2 · 18/21 | 1 953 | 2 |
| **GFX (candidato)** | **1.0 / 0.95** | **2/2 · 21/21** | **685** | **2** |
| BRÚJULA | 0.0 / 0.0 (va a la otra en *desvía*: 1.0) | — | 701 | 2 |
| INVERTIDO | 0.0 / 0.0 | — | 685 | 2 |
| UNA (v14.2 en el mundo de subida_n6) | 1.0 / 0.95 (rodeo / atajo) | 1/1 · 21/21 | 601 | 3 |

## Qué falló (declarado)
- **Predicción 7, refutada en el humo.** Con dos comidas, CIEGO come 1 240, no 250–600. Explorar saciado le cuesta a GFX
  la mitad de la comida de GF, aunque no le cuesta vidas. R-4 (≥ 0.90) da 0.552. **No la enmiendo:** hacerlo sería
  candidato a ERR.
- **Primera pasada del arnés: 74/75.** El control «vista difiere» salió bit a bit igual en 14644, porque la vista puede
  ser inerte. Lo arreglé antes del humo (vista con explora) y quedó en 75/75. Está declarado en PREREGISTRO §9.
- **Geometría condicionada:** acepta sólo ~2–7 % de las tiradas y deja 3–5 salidas *cruza* distintas por semilla.
  Está declarado.
- **Uso de cómputo:**
  - 3 corridas de depuración y un perfilado, en semillas del arnés;
  - las dos pasadas del arnés;
  - el humo de 6 corridas.

  No hubo Pool, `--serie`, commit ni `manifiesto.py`.

## Qué queda
- **Comandos** (los corre el coordinador; costo ≈ 9 000 s de CPU, 2.5 h, ≈ 25–30 min de pared con Pool 6, cada uno):
  ```
  python experimentos/subida_n6b/corre_subida_b.py --desde 14601 --n 20 --pool 6
  python experimentos/subida_n6b/corre_subida_b.py --desde 14621 --n 20 --pool 6
  python experimentos/subida_n6b/corre_subida_b.py --lee <serie.json> --sello <sha> --lee_replica <rep.json> --sello_replica <sha>
  ```
- **Puntos** (decide el director):
  - FUNCIONA (13/13 en las dos): nivel 6 → **80 %**;
  - HAY ALGO MODESTO (núcleo D-1a, D-1b, D-2 y D-3 en las dos): **65–70 %**;
  - NO: el nivel no cambia.
- **Para el 100 %:**
  - hueco que se mueve (desdecirse dentro del episodio): con `r_vis = 1` y el filtro, el organismo no pisa lo que
    recuerda como veneno, así que no puede descubrir el hueco nuevo. Necesita otra pieza;
  - rodeos compuestos más allá de `H_M`;
  - explorar sin pagar la comida: por ejemplo, dejar de explorar cuando M ya no crece.
- **No verificado:**
  - el nulo del margen (regla 15);
  - PLACEBO, BARAJADO, GFV, GFVX y GFX_13 sin humo;
  - la tasa de V1 en 20 semillas (p ≈ 0.6 de 20/20);
  - el tiempo de pared con 2 Pools en la máquina.
