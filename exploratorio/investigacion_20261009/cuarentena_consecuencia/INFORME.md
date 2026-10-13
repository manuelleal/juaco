# Cuarentena por CONSECUENCIA contra envenenamiento de memoria — 9-oct-2026 (exploratorio, nivel 0, fuera del tronco)

**HAY ALGO MODESTO; la serie NO se corre.** El humo 0 (sin modelo, 5 semillas, 12 hechos por clase) decide lo que el preregistro pedía decidir: la cuarentena por consecuencia (q) gana a la memoria simple, al voto de dos fuentes y a la cuarentena K=2 de Frankenstein v1 (1.00 -> 0.02 de respuestas envenenadas en PAC2+SYB2), pero EMPATA con el rival barato y estandar, voto de dos fuentes + lista negra tras una mentira verificada (0.06). Frente al atacante paciente, al insistente y a cuatro identidades falsas, q y el rival dan la misma tasa semilla a semilla en 5/5.

Criterio por la letra: 0/5 semillas cumplen FUNCIONA; el control barajado da -0.06 en PAC2 (se pedia >= +0.20) -> MODESTO.

| brazo | CONS1 | SYB2 | SYB4 | PAC2 | PAC2+SYB2 | SYB2U | SYB4U | confirmable | dichas una vez |
|---|---|---|---|---|---|---|---|---|---|
| b (memoria simple) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | - | - |
| bv2 = c = r | 0 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | - | - |
| bv2+LN (rival) | 0 | 0.03 | 0.07 | 0.06 | 0.06 | 0.57 | 0.60 | 1.00 | 0.00 |
| bv2+LN+V (rival que guarda lo verificado) | 0 | 0.03 | 0.07 | 0.06 | 0.06 | 0.57 | 0.60 | 1.00 | 0.40 |
| q | 0 | 0.00 | 0.07 | 0.06 | 0.02 | 0.00 | 0.60 | 0.90 | 0.40 |
| q sin reputacion | 0 | 0 | 0.63 | 0.00 | 0.00 | 0 | 0.60 | 0.47 | 0.40 |

Lectura:
- "Peso 0 tras un fallo verificado" ES una lista negra. El atacante paciente se gana el peso completo a proposito, entra a q y al rival en el mismo instante y cae con la misma revelacion.
- Lo unico que q añade es la probacion (fuente nueva pesa 0.5): sube el precio del ataque de 2 a 4 identidades de un solo uso (SYB2U 0.00 contra 0.57) y nada mas (SYB4U 0.60 en ambos). Cuesta arranque en frio: confirmable 0.90 contra 1.00.
- La "verificacion propia en sombra" es regalo del oraculo: el acierto en lo dicho una vez es identico al del rival que guarda lo verificado y al del piso que solo usa el oraculo (0.40).
- La reputacion es la superficie del ataque paciente, no la defensa: q sin reputacion da PAC2 = 0.00.
- Humo 1 (con Qwen2.5-1.5B, semilla 0, plantillas A, 502 s): mismo cuadro (bv2 0.81, c 0.77, bv2+LN 0.04, q 0.02); extraccion exacta 0.79; confirmable de q 0.80 contra 0.97 del rival.

Literatura revisada el mismo dia (resumen): los ataques existen (AgentPoison, MINJA, PoisonedRAG); "hipotesis sin autoridad + corroboracion independiente + confianza por fuente" ya esta publicado (descubrimiento de verdad; RobustRAG; defensas de memoria de 2026, una con pruebas formales). No se encontro publicado "prediccion en sombra validada por consecuencia", pero este humo muestra que, con un oraculo exacto, eso se reduce a voto + lista negra.

Lo que NO dice: nada sobre secuestro de acciones ni inyeccion de instrucciones, nada sobre energia (no entro), nada sobre modelos grandes ni sobre alefast real. El humo no fue auditado por un agente independiente; no se declara nada mas alla de "no gastar la serie".

Que quedaria por probar, si se quisiera una diferencia real (otro preregistro): oraculo ruidoso o manipulable, o consecuencia que solo dice acierto/fallo de una accion sin revelar el valor; ahi una lista negra no alcanza.

Hallazgo lateral (por lectura de codigo, sin ejecutar): en alefast `Exo.observe()` no recibe la fuente y el modo "fast" se activa con racha >= 2 sin contar fuentes distintas: un solo agente insistente podria promover o vetar una accion. Es el caso que Frankenstein ya bloquea.

Archivos: PREREGISTRO.md (predicciones antes de correr), mundo_q.py, memorias_q.py, linea.py, rapido.py, arnes_identidad.py, corre_cuarentena.py, datos/humo0.*, datos/humo1.*, datos/arnes_identidad_v2.txt. Semillas 0-4 gastadas; 41-45 y 51-55 reservadas sin usar.
