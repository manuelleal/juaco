# VEREDICTO — MURO MÍNIMO, PIEZA POR PIEZA (serie 885001–885020, 14-oct-2026)

**NO SE LEE.** El control bajo MINIMO tuvo mayoría en 15/20 semillas; la letra (`PREREGISTRO.md:124`) dice que con MINIMO en ≥ 15/20 no hay brecha que cerrar y no se declara nada. Por `PREREGISTRO.md:68`, una tanda que no se lee hace NO SE LEE al bloque: la réplica (885021–885040) no puede cambiar el veredicto y **no se corre**.

Salida completa: `serie_consola.txt` (120/120 corridas; la primera ejecución se cortó en 68/120 sin error, probablemente por apagado del PC, y se reanudó: el runner salta los JSON ya escritos).

| brazo | mayoría (≥ 15/20 = cierra) | suma de linajes que cruzan |
|---|---|---|
| HUMO (control alto) | 20/20 | 159 |
| M_RECICLA (P3) | 18/20 | 134 |
| MINIMO (control bajo) | **15/20** | 102 |
| M_PIZARRA (P1) | 13/20 | 108 |
| M_URGENCIA (P4) | 9/20 | 88 |
| M_RADIO (P2) | 8/20 | 87 |

## Lo que sí dice, sin declararlo
- **El control bajo no es estable entre semillas:** MINIMO dio 10/20 y 11/20 en el bloque anterior (884xxx no; 883xxx y siguientes) y 15/20 aquí. La "brecha" MINIMO–HUMO que motivó el bloque es más chica y más ruidosa de lo que suponía el preregistro.
- Descriptivo: M_RECICLA suma +32 linajes sobre MINIMO (el umbral de MUEVE era +20) y es la única pieza por encima de MINIMO en las dos medidas, como predijo el creador. M_RADIO y M_URGENCIA quedan por debajo de MINIMO solo.
- Nada de esto se declara: la tanda no se lee.

## Qué sigue (propuesta, no decidido)
Antes de otro bloque de piezas: medir la tasa de cruce de MINIMO con 40 semillas nuevas, sola, para saber si hay brecha que cerrar. Si MINIMO cruza ≥ 70 % de las veces, la pregunta "¿qué pieza falta?" pierde sentido y el muro mínimo ya es la decisión de dos modos.

No se numera ERR: el control bajo hizo su trabajo (podía fallar y falló). Siguiente ERR libre: ERR-203.
