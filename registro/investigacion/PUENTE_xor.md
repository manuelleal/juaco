# PUENTE — trío de agentes sobre XOR (bloque 3c). Escriban aquí; lean lo de los otros antes de cada paso.

Problema: en el mundo de regla (20 patrones de peso 3, `experimentos/nivel7_xor_lectura/organismo_v13q.py`), la vía lenta
con lectura cuadrática (6 px + 15 productos) representa XOR (`W(P0·P1) = −2.68`) pero clasifica los nunca vistos al azar
(0.50): los marginales de `P0`, `P1` quedan en cero. Diagnóstico del coordinador (hipótesis): la regla de la vía lenta
(dos canales no negativos `Wps/Wns`, actualización proporcional a `phi` con el error residual, drenaje `lam` de la parte
común) reparte el error por igual entre todas las entradas activas y no puede poner lo negativo sólo en el producto.
Objetivo del trío: UNA propuesta de regla local para la vía lenta (o de lectura) que separe XOR en nunca vistos (≥ 0.75)
sin romper `px0`/`azar` ni la identidad con `lectura='lineal'`, con predicción numérica y controles, lista para preregistrar.
Cada agente: escribe su sección (nombre, hipótesis, mini-prueba de UN proceso ≤ 3 corridas de 100000 pasos, números,
sugerencia), lee las de los otros, y al final los tres firman una propuesta única (o dos, si no hay acuerdo, con la razón).

## Agente A (regla delta con signo)

## Agente B (drenaje y canales)

## Agente C (lectura / término constante / muestreo)

## Propuesta única del trío (firmada por los tres)
