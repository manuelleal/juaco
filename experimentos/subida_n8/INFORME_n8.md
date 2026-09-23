# INFORME — subida del nivel 8 (creador, 23-sep-2026)

**Veredicto de los humos: HAY ALGO MODESTO, por confirmar.** En dos semillas de práctica, el tronco sigue aprendiendo lo nuevo
con 90 celdas a lo largo de 200 estímulos y olvida lo ausente. La fusión de celdas **no** ayuda: fue peor en las dos. La serie
12601–12620 y la réplica 12621–12640 no se corrieron (necesitan Pool). Decide el coordinador con `PREREGISTRO_n8.md`.

## Qué hice
- **(a) El 100 % del nivel 8, pieza por pieza, con archivo:línea** (tabla del §0 del preregistro). Faltan cuatro piezas:
  - mundo sin techo con criterio "sigue aprendiendo";
  - retener lo ausente;
  - un órgano que libere capacidad;
  - un currículo propio y un dominio distinto.
- **(b) El bloque:** el "experimento único más informativo" que dejó escrito `nivel8_aprendizaje_abierto.md:122-125` y nunca se
  corrió. Es el tronco sin órgano contra el tronco con fusión, en un mundo sin techo, con controles de fusión al azar, de novedad
  falsa (RECIC), de valencias permutadas (NULO) y de lo que sabe gratis (PRIOR).
- **Instrumento por anclas:** `construye_n8.py` → `organismo_flujo.py` (`14afed5aa16e09bf`), desde `organismo_capBD_on.py`
  (`506b5c08441fd54e`), con 5 anclas.
  - Mundo: `mundo_n8.py` (`b0b57d7ff02afe4e`). Runner: `corre_n8.py` (`1d78fd3ad1113eec`), con `--humo` y entrada campo a campo
    (regla 14, 100 campos, 0 distintos).
  - El arnés ancla el instrumento **al tronco congelado** `organismo_v142`: W, muertes, divisiones, celdas, mordidas y visitas
    idénticas en 3 semillas.

## Salida del arnés (`identidad_n8_salida.txt`, 16:10:13)
```
(0a) origen capBD_on 506b5c08441fd54e OK · (0b) tronco v142 OK · (0c) organismo_flujo == construye_n8, 14afed5aa16e09bf OK
(A) x3 ventana=0 fusion=0 == capBD_on, 27 claves   OK · (A1) x2 retina 12, 30 estimulos, fotos == capBD_on   OK
(A2) x3 == organismo_v142 en W, muertes, divisiones, celdas, mordidas, visitas   OK
(B) x2 fusion 1/2 inerte sin agotar el pool   OK · (C1-C5) funde solo con el pool agotado, <= 90 celdas, dirigida != azar,
identica a base hasta agotar   OK · (D) determinismo OK · (E1-E4) valencias 5/5 por bloque, 200 patrones de peso 3, RECIC
repite con su valencia, visitas a viejos 0.214   OK · (F1) 3 llamadas nuevas al rng, en el mundo · (F2) la fusion no lee
valencias   OK · (G) regla 14   OK
TOTAL 26/26 en 45.9s
```

## Qué falló (declarado)
- **Mis predicciones refutadas en práctica** (las traía del documento, `nivel8…md:172-178`, antes del humo):
  1. «el tronco sin órgano cae a azar pasado el agotamiento». **Refutada 2/2**: ADQ_tarde 0.78 y 0.72; comida 0.56 y 0.44 contra un
     a priori de 0.16.
  2. «la fusión sostiene lo nuevo». **Refutada 2/2**: FUS está 0.08–0.16 por debajo de BASE y empata con FUS_AZAR.
  Las dos quedaron invertidas en el preregistro (P3, P8) y se declara.
- **Arnés.** La primera corrida dio **24/26** por dos comprobaciones mal escritas, no por el instrumento:
  - E4 contaba como "viejos" a estímulos que habían estado en la ventana durante ese cuarto.
  - F1 restaba `_rngf.` de un conteo que no lo incluía.
  Se corrigieron y dio 26/26 dos veces.
- **Medida corregida después del humo 1.** La ventana deslizante de 10 pasó a medirse por entrada, y se añadieron PRIOR, NULO y
  el acierto por clase. El motivo: **el a priori es negativo casi siempre**, así que el veneno sale gratis y el acierto balanceado
  (0.78) exagera; lo aprendido es la comida. La medida principal pasó a ser comida − a priori.
- **Corridas usadas: 5 humos de un proceso**, todas de T = 200 000, con 12690 ×3 y 12691 ×2. Más el arnés ×3.

## Qué queda
- **La serie y la réplica con Pool**, en el §9 del preregistro. Cuestan unos 20 min de CPU cada una.
- **P3 es la que puede caer.** En 12691, la comida bajó de 0.53 (temprano) a 0.44 (tarde), −0.09: casi en el borde de −0.10.
- **Límites declarados:**
  - 200 estímulos son 2.2 veces las celdas, no "muchas veces" (`nivel8…md:106`). Con peso 3 sobre 12 píxeles el techo es 220.
    Ir más lejos exige peso 4 o más píxeles y T ≥ 500 000 (sólo en serie).
  - El organismo apenas muerde comida nueva, porque su a priori dice veneno. Eso es neofobia, y conecta con la pieza 4 (explorar).
- **Siguiente bloque, si FUNCIONA:** la pieza 2 (retener lo ausente) con consolidación o repaso, en este mismo instrumento.
- **No verifiqué:**
  - La rama `Pool` del runner no la ejecuté (prohibido). Es `Pool.map` sobre una función de módulo.
  - El número de "N\* 51" del instrumento de origen es del registro, no lo recalculé.
