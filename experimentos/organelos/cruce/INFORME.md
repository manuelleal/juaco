# INFORME — organelos/cruce (Opus C, 24-sep-2026). Una página

**Estado: LISTO PARA SERIE (la corre el coordinador). Sin dato: arnés 30/30 y tres humos de práctica de una semilla.** Mi lectura
antes de correr: **probablemente NO** (bloque: FUNCIONA 0.03 · MODESTO 0.15 · NO 0.72 · NO SE LEE 0.10). Nada commiteado, sin Pool, sin
matar procesos, sin tocar congelados ni nada fuera de `experimentos/organelos/cruce/`.

## Qué hice
- **Vivero evolutivo en la pista de la carrera, por anclas:**
  - `motor_cruce.py` sale de `pista.py`. Agrega genoma por cuerpo, error de copia en el parto, banco de padres con fundadores del
    banco sólo antes del corte, 8 sombras, AZAR y la lesión.
  - `carros/CRUCE.py` sale de `V143.py`. Es el cerebro de v14.3 **sin tocar**, más **36 genes de cableado** que nacen en 0:
    6 señales internas presentes (reserva, la otra necesidad, ventana de parto, edad, hijos en cola, sesgo) entran en 3 decisiones
    que el cuerpo ya tiene (morder según cómo valora la letra, a qué ir, parir).
  - No hay regla de O1 ni de O3: es una base lineal completa, simétrica en signo, sin sus umbrales (PREREGISTRO §2).
- **Diseño de dos fases por semilla:**
  - **Cría** de 200 000 pasos. La única selección es la natural: el que pare llena su cola y el banco.
  - **Lectura** en una carrera **nueva** de 100 000 pasos con la letra de la ENMIENDA 5. Cada linaje lleva un genoma del banco
    congelado. El fundador limpio es una instancia nueva **con el genotipo de su linaje**, igual que el de O1 es una instancia nueva
    del código O1.
  - Brazos: VIDA, placebo VIDA_P, AZAR, MUT0, V143, **DESF** (los mismos genomas leyendo el estado de un paso pasado al azar; el
    control que puede fallar) y O1 como techo.
- **Arnés `identidad_cruce.py`: RESULTADO 30/30.**
  - Motor sin cruce == pista, bit a bit.
  - **Genes apagados == V143 en la pista bit a bit, y la lectura == `corre_v143.tarea` campo a campo (regla 14).**
  - MUT0 == V143.
  - En la lectura el genotipo se conserva a través de los fundadores.
  - DESF difiere de VIDA y la historia de señales pasa al fundador.
  - Los genes mutan (media hijo-padre 1.06, esperada 1.08) y se heredan; AZAR no copia al padre (6.7).
  - Los genes cambian la conducta: con la boca forzada, 1 672 decisiones distintas y B+D pasa de 472 a 377; hay vetos de parto;
    las patas cambian el objetivo en 6 370 decisiones.
  - La marginal del desfasado está a ≤ 0.065.
  - La letra se comprueba en casos sintéticos. nube-9 queda atrapado. Las banderas malas abortan.
- **El humo escribe su JSON** (`datos/humo/cruce_humo_s24405_tc30000_tl20000_final_20260924_135019_resumen.json`,
  `1aa488358d82936f`):
  - 687 mutaciones y 109 partos en la cría VIDA; el 83 % del banco lleva genes ≠ 0.
  - Distancia hijo-padre [29, 44, 22, 11, 2, 1].
  - En la lectura: boca_dif 141, pata_dif 1 575 y 44 vetos de parto.

## Qué falló (declarado)
1. **Primer diseño retirado** (humo 1, antes de cualquier serie). Tras el corte el fundador volvía al genoma 0 y leía una ventana
   continua. Con eso, v14.3 fijo sacaba ≈ d/(d+1) en los linajes establecidos (ERR-102), y la comparación con O1 era injusta.
2. **Patas casi inertes.** Con el bono por contexto cambiaban 12 de 54 000 decisiones, porque el FILTRO ya quita lo malo. Las
   rediseñé como ganancia sobre el valor propio de la letra.
3. **Umbral mal calculado en el arnés 5c.** Puse ≥ 0.90 y el esperado es 0.87. Mi predicción de que «casi todos los hijos difieren
   en 0–2 genes» quedó refutada por mi propia aritmética.
4. **Humo largo** (1 semilla, sin valor): con 100 000 de cría, VIDA 0.233 contra v14.3 0.250. Por eso espero NO.
5. **Escribí fuera de mi carpeta sin querer.** Mis primeros imports de solo lectura dejaron `__pycache__` en `carrera_escuderias/` y
   `tronco_v14_3/` del worktree (13:12–13:17). Es bytecode ignorado por git; no lo borré porque otros agentes importan lo mismo. Desde
   entonces el runner y el arnés llevan `sys.dont_write_bytecode = True`, y el arnés se volvió a pasar: 30/30, sin escrituras nuevas.
   El humo final corrió con el runner anterior (`92fb8d8c`), que sólo difiere en esa línea.

**Salida del arnés** (`identidad_cruce_salida.txt`; runner `0d10b5e3ac033e81`, motor `6cfff5c04fdc2c8f`, carro `63ac38bac2d0bbcd`):
```
[1-5] OK (0a-e) shas · por anclas · revisa_carro · sin tabla verdadera · 36 genes
[6-7] OK (1) motor(cruce=None)==pista 9 V143 / 9 O1 + rng     [8-9] OK (2a) CRUCE sin cruce == V143 (147/87 muertes)
[10-11] OK (2b) regla 14 == corre_v143.tarea: R0 pista 0.0806/0.0806 · 0.1143/0.1143
[12-14] OK (3) cria MUT0 == v14.3 (mut 0, banco !=0 0) · lectura mut0 == v143
[15] OK (4a) genotipo conservado: 225 fundadores, hist [52,0,0]   [16] OK (4b) desf != vida, 70 799 lecturas, historia 287/287
[17] OK (4c) muestra determinista, placebo distinto   [18] OK (5a) determinista
[19] OK (5b) n_mut 339, sombras 2 861, banco !=0 22/57   [20] OK (5c) hijo-padre 1.06 (esperada 1.08)   [21] OK (5d) AZAR 6.70
[22] OK (6a) boca_dif 1 672, B+D 472->377   [23] OK (6b) 37 vetos   [24] OK (6c) pata_dif 6 370   [25] OK (6d) 365
[26] OK (7) marginal <= 0.065, iguales 0.001   [27] OK (8) letra sintetica   [28] OK (9a) nube-9   [29] OK (9b) banderas   [30] OK (9c) masa 3
RESULTADO: 30/30   (157 s; datos/humo/identidad_cruce_20260924_135750.json 648681078498796b)
```

## Costo (Python, un proceso, medido) y gemelo
| tarea | s por corrida | por serie |
|---|---|---|
| cría 200 000 (vida, azar, mut0) | ~200–250 | 60 → ~13 500 s |
| lectura 100 000 (6 brazos v14.3) | ~100–125 | 120 → ~13 800 s |
| lectura O1 100 000 | ~210 | 20 → ~4 200 s |

- Serie ≈ **8.7 h de CPU ≈ 1.5–2 h de pared con Pool 6** (dos etapas: crías y lecturas). La réplica cuesta lo mismo. No pasa de
  ~2 h, así que **el gemelo no es obligatorio para esta serie**.
- Para **acelerar** (lo pide el director; una cría de 10⁶–2·10⁶ pasos), la especificación para el `juaco-compilador`:
  - **Qué portar:**
    - el bucle de `motor_cruce.run` con `cruce` (fases A y B, reposición y olvido escalado, cola FIFO, fundador limpio, `_muta`,
      banco, sombras, `_foto`);
    - el carro `CRUCE`: cerebro FABRICA con B-5, NODO al nacer, opción TD de APR, FILTRO/META con CACHE, más `_senal`,
      contextos, `_cr_pb`, `_see_cr`, `quiere_parir` y el búfer desfasado.
  - **Partir de** `organismo_f9c_rapido.py` y del gemelo de v14.3 que planea ESTADO. **Mismo consumo de rng** que el original.
  - **Arnés `identidad_cruce_rapido.py`:**
    - `cruce=None` con 9 V143 == `motor_cruce` bit a bit (física + telemetría v143), 3 semillas, T 4 000;
    - crías VIDA, AZAR y MUT0 con T 12 000: el `cruce` completo idéntico (n_mut, ham, banco y sombras del corte);
    - lecturas vida y desf con genomas fijos, T 12 000, idénticas;
    - velocidad ≥ ×30.
  - O1 sigue en Python.

## Riesgos
- **Selección débil:** ~1 000 partos y ~2 000–4 000 refundaciones por semilla para 36 genes.
- **La letra premia morir (ERR-102):** se mide y se reporta. La cría selecciona parir y vivir, no morir.
- **El fundador con el genotipo del linaje** es mi decisión de diseño. Si el coordinador prefiere genoma 0, cambia una línea del
  motor y la lectura mide otra cosa.
- **DESF al inicio de la lectura:** los primeros ~2 000 pasos leen un búfer corto; la lesión es más débil ahí.
- **MUT0 es degenerado** (== v14.3). Se corre por la letra; son ~13 % del costo.

## No verificado
- La ruta con Pool (prohibida para mí).
- El costo con los Pools del PC cargados.
- Que 200 000 pasos alcancen.
- El placebo con datos reales.
- Si VIDA_P y la guardia de AZAR se comportan como la nula.

## Qué queda
- El coordinador corre el arnés y después la serie y la réplica (PREREGISTRO §10).
- Si sale MODESTO o NO, el paso siguiente es el gemelo, con una cría de 10⁶ con las mismas semillas y la misma letra, en un
  preregistro nuevo.
