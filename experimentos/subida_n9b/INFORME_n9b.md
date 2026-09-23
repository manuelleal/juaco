# INFORME — nivel 9, segunda tanda: ¿la predicción de sí APRENDIDA por el organismo es causal? (creador, 23-sep-2026)

**Veredicto de la entrega: paquete LISTO PARA SERIE. No hay dato: arnés 48/48 y un humo de una semilla (sin valor).**
Nada commiteado, sin Pool, sin tocar congelados ni carpetas ajenas. Todo en `experimentos/subida_n9b/`.

## Qué elegí y por qué
`subida_n9` lesiona a O3, cuya política escribió un LLM. Esta tanda lesiona a **APR**: el cerebro REL de FABRICA más una
corrección de la boca aprendida por TD y heredada. Es el único carro con réplica cuya decisión sale de lo que aprende el
organismo (gana a FABRICA 20/20 en dos series; no cruza, R0 0.385). Uno de sus rasgos es una **predicción de su propio
estado**: `post`, el nivel que tendría su necesidad más baja si mordiera esa letra, calculado con lo que el linaje sintió. Pregunta:
¿la ventaja pasa por esa predicción o sólo por contenerse? Cinco brazos: APR, FABRICA, PLANA (`post = u`), CRUZ (efecto aplicado
a la otra necesidad) y MUNDO (control de especificidad: la misma operación sobre los rasgos del mundo). Memoria nueva: cero.
Descarté: O3_DECIDE_MORIR (otra política escrita a mano), portar dE5 (candidato a tronco pendiente) y APR_AZAR (P9 de otra carpeta).

## Arnés `identidad_n9b.py`: **48/48** en 172 s (`identidad_n9b_salida.txt`)
- **Shas y construcción:** los 6 shas de origen OK. Construcción por anclas reproducible. APR y FABRICA son copias verbatim
  (4402aa5142065c72, 2ebee3e99ea5a33a). Los 6 carros pasan `revisa_carro`.
- **Identidades:**
  - identidad corta del juez: dif [];
  - APR con OPCION 0 == FABRICA;
  - **APR_LES_OFF == APR bit a bit** en toda la salida de `pista.run` (s13592 y s13593, T = 8000, con 5648 y 6115 decisiones);
  - con `ALFA_Q = 0` las tres lesiones == APR: la lesión sólo entra por lo aprendido.
- **Las lesiones actúan:**
  - no son inertes y cada una toca sólo lo suyo (PLANA/CRUZ cambian `post` en el 87–89 % de las decisiones; MUNDO cambia los
    rasgos del mundo en el 99 %);
  - la ejecución es determinista.
- **Runner:**
  - entrada campo a campo == `juez.tarea`, y la mini identidad pasa;
  - **16 formas malas abortan** (`--help`, `-h`, `--se`, `--pool=6`, sin `--pool`, semillas ajenas, humo > 6 corridas, …) y
    5 formas válidas parsean.

## Humo (un proceso, s13591, T = 20000, 5 corridas, 100 000 pasos, 181 s; sin valor) — `datos/humo/n9b_humo_…_164054{.log,_crudo.json,_resumen.json}`
| brazo | R0 mediana (9 linajes) | R0 real eval | muertes (mediana) | tasa de mordida de la opción (FABRICA habría) | lesión: `post` real / usado |
|---|---|---|---|---|---|
| APR | 0.319 | 0.243 | 42 | 0.123 (0.183) | — |
| FABRICA | 0.296 | 0.262 | 43 | — | — |
| PLANA | 0.282 | 0.275 | 44 | 0.125 (0.193) | 0.550 / 0.868 (sesgada, como se declaró) |
| CRUZ | 0.333 | 0.289 | 39 | 0.103 (0.173) | 0.594 / 0.606 (V-M se cumple) |
| MUNDO | 0.333 | 0.295 | 32 | 0.116 (0.171) | — (cambia el mundo en 0.994) |
- **Controles del humo:** coherencia 45/45, t_fund 45/45, 0 escrituras.
- **Lo único que dice el humo:** el instrumento funciona. En PLANA, Q aprende pesos iguales para `u` y `post`, que son colineales.
  Con una semilla no se lee nada.

## Qué falló (declarado)
- El primer (6) del arnés habría fallado: los contadores de telemetría que se agrupan por `post`/`g0` cambian aunque la conducta
  no cambie. Los excluí antes de correr, sólo en esa comparación; la física y las decisiones se comparan completas.
- Ningún umbral cambió después del humo. **Enmiendas: ninguna.**

## Qué queda (sólo el coordinador; después de n8 y n9, según la cola)
```
python experimentos/subida_n9b/identidad_n9b.py                                   # 48/48, ~3 min
python experimentos/subida_n9b/corre_n9b.py --serie --desde 13501 --n 20 --pool 6  # serie
python experimentos/subida_n9b/corre_n9b.py --serie --desde 13521 --n 20 --pool 6  # replica
python experimentos/subida_n9b/corre_n9b.py --veredicto <resumen 13501>,<resumen 13521>
```
**Costo:** 100 tareas por serie, de 165 a 210 s cada una. Son 4.6–5.8 h de CPU y ~50–75 min de reloj con Pool 6, por serie.

**Puntos (propuesta; decide el director).** Sumados a lo que dé `subida_n9`:

| resultado | puntos |
|---|---|
| FUNCIONA | +8 |
| MODESTO | +3 |
| NO | 0 |

Mejor caso de las dos tandas: **~68 %, no 90 %.** Para llegar a 90 falta un linaje cuyo cerebro sea el organismo propio y que cruce
H-1, con este modelo de sí causal en él y resistente a un cambio de reglas del mundo.

## Refutado y no verificado
- **Mi predicción central P2 la doy por refutada con p 0.65:** creo que la ventaja de APR es contención general, no predicción
  de sí.
- **No verificado:**
  - que la serie repita la ganancia de APR (P1) con estos shas y otras semillas;
  - el tiempo real con los Pools del coordinador en marcha;
  - que `experimentos/subida_n8/identidad_n8_salida.txt`, que aparece modificado en el árbol, no es mío (no lo toqué).
- La reserva **ERR-104** aplica: el mundo repone al instante lo mordido. La comparación pareada vale, pero el R0 absoluto no
  vale para un mundo con recurso limitado.
