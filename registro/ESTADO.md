# ESTADO — una página, se reescribe en cada cierre (skill `/juaco-cierre`)

> Última reescritura: **21-sep-2026, 19:10** (coordinador; junta sintetizada, ERR-91/92, tercera serie BA-v y tercera serie fase 9 en marcha). Si esta fecha tiene más de un día de atraso, el estado real está en la cola de
> `REGISTRO_etapas_1_2.md` y en la última sección de `HANDOFF.md`; corregir esta página antes de tocar nada.
> Historia completa: `REGISTRO_etapas_1_2.md` (sólo añadir). Narrativa: `HANDOFF.md`. Orden vigente: `PLAN.md`. Reglas: `EQUIPO.md` y `CLAUDE.md`.

## Tronco
**v14.2** (tag `v14.2-tronco`, 18-sep 21:25) = v14.1 + B-5 (división por conflicto disparada por R = 0 bajo retina distinta; repara el alias de
código). 20 archivos congelados (`python manifiesto.py` desde la raíz los verifica). Regla 1 en `CLAUDE.md`. Criterio para candidatos nuevos:
`CRITERIO_TRONCO_v2.md` (sobrevivir + generalizar + desdecirse + sin alias + no regresión conductual + coste + capacidad nueva declarada).

## Niveles del brief (porcentaje = lo declarado con réplica)
| nivel | estado | última evidencia |
|---|---|---|
| 1–4 (asociación, desaprender, generalizar, capacidad) | cerrados; nivel 4 con el negativo del alias reparado por B-5 (v14.2) | 18-sep |
| 5 (comunicación / transmisión) | **75 %**: N1 cerrado; referencia de FAMILIA exacta (k = 3) o de VARIANTE (sufijo), no ambas con la misma tabla; junta del 19-sep no cerró (C refutado ×2, B cae ×2, A pasa R1–R5 en una serie sin réplica, PAR 13 < 15) | 19-sep |
| 6 (mapa, dos metas y rodeo) | 50 % (consenso de la junta): replicado: elige entre dos comidas recordadas y rodea el veneno recordado; no planifica; canje del mapa estructural, v14 sin mapa | 17-sep |
| 7 (composición, XOR) | 70 % (consenso de la junta): 3T-k compone hasta 3; XOR CERRADA: prior estructural de pares (8 ejemplos, 1.000 ×2); hija dispersa en el tronco; **LÍNEA CERRADA (21-sep): memoria de pares en la vía lenta v15c–v15g, ninguno entra** | 21-sep |
| 8 (aprendizaje abierto) | 40 %: curiosidad por progreso refutada; mundo vivo con dos necesidades es el primer mundo con más de una dimensión de valor | 18-sep |
| 9 (autonomía / modelo de sí mismo) | 30 %: allostasis mínima medida; r = descendientes − muertes ordena como la supervivencia; H-1: la muerte real no sostiene linajes; **fase 9 bloque 1: serie 1501–1520 con 8/10 puertas y réplica 1521–1540 con el mismo patrón (7 pasan, 2 caen), pero CAE el ancla bloqueante F9-1 en la réplica (vida NADA 88.5 fuera de [90,170] por 1.5): nada se declara por la letra; ERR del rango del ancla pendiente** | 21-sep |
| 10–13 (alma, familias, vivo) | exploratorio: serie ALMA (el alma razonada no gana al azar; el nodo transmite contenido); mundo de familias construido | 18-sep |

## Pendiente con paquete verificado (correr en este orden, un Pool a la vez)
1. ~~v15f bajo el criterio v2~~ — **corrido y cerrado el 21-sep 12:37–12:54: NO ENTRA** (cae T-A, T-C, T-D, T-E; pasa T-B, T-F, T-G);
   `datos/v15f_v2_20260921_123755.json` (`58538f00d49d0f8e`), detalle en el registro y HANDOFF 15.13. Patrón v15d/v15e/v15f: recomendado cerrar la línea.
2. ~~dE5 bajo el criterio v2~~ — **corrido y cerrado el 21-sep 15:22–15:37: NO ENTRA** (cae T-A, T-C ii, T-E, T-G; pasa T-B, T-C i, T-D, T-F);
   recupera 3.23× más rápido (pareado 20/20; el control sin información recupera más lento que el apagado) pero muerde más veneno en los seis
   escenarios de T-E y 1.128× tras el cambio. `datos/dE5_v2_20260921_152224.json` (`ea74d601313d4ee9`); HANDOFF 15.19. Órgano medido, no candidato.
3. ~~Fase 5, candidato BA~~ — **corrido 921–940 + réplica 941–960 (21-sep): misión cruda cumplida ×2 con BA y BA-v, pero ninguno pasa las
   cinco puertas relativas del bloque 6; BA-v muere 104 en la réplica; R6 incompleto (ERR-89).** Nada se declara; nivel 5 sigue en 75 %.
4. **Fase 9**: cuerpo nuevo que aprende en menos de una vida (nodo leído por relevancia; conexión desde el nacimiento; reproducción desacoplada
   de la saciedad). Sin preregistro todavía.

## Errores
Último: **ERR-92** (21-sep: ERR-91 criterio v2 sin placebo → criterio v3 en construcción; ERR-92 rango del ancla F9-1 → enmienda). Siguiente libre: **ERR-93**. Regla 15 de EQUIPO.
Reglas de equipo 1–14 en `EQUIPO.md`; regla derivada de ERR-87: "último JSON de un prefijo" siempre con prefijo + sello exacto.

## Datos
`datos/` plano (562 archivos, 84 MB). `datos/humo_no_registrado/` guarda humos y corridas sin dueño en el registro (no entran a git).
Desde el 21-sep los runners nuevos escriben sus humos en `datos/humo/`. Índice de carpetas de experimentos: `experimentos/INDICE.md`.

## Equipo y herramientas (21-sep-2026)
Agentes fijos (en `~/.claude/agents`, valen desde cualquier carpeta): `juaco-creador` (Opus), `juaco-compilador` (Opus), `juaco-auditor` (Sonnet,
solo lectura), `juaco-cronista` (Sonnet), `probador-haiku`, `explorador-haiku`. Skills: `/juaco-estado`, `/juaco-bloque`, `/juaco-cierre`,
`/juaco-err`, `/veredicto`, `/encargo`. Ninguno corre Pool, commitea ni mata procesos: sólo el coordinador. Coordinación de CPU: mirar los
procesos python vivos con su cmdline antes de lanzar (ERR-85, ERR-86).

## Decisiones del director (21-sep-2026, 16:30: "llena las 3 de una vez, manda grupos de agentes" → las tres tomadas con la recomendación)
1. **CERRADA** la línea de memoria de pares en la vía lenta (v15c–v15g); v15g sólo se reabre con preregistro propio y siete puertas. Registrada (HANDOFF 15.16).
2. **BA-v como candidato aparte (ERR-90, puertas absolutas): serie 961–980 corrida, CAE P6** (dist(PAR) 13/19 < 15, 2 semillas) y pasa las
   otras siete, incluida R6 con base b4b (única celda que la pasa). Misión cruda 2/3 series, letra 0/1. Réplica 981–1000 en cola después de dE5-v2;
   si cae P6 otra vez, BA-v se cierra. HANDOFF 15.17.
3. **Fase 9 corrida (1501–1520 y réplica 1521–1540)**: 8 de 10 puertas pasan y el patrón se repite en la réplica, pero el ancla F9-1 cae en la réplica por 1.5 (HANDOFF 15.20); (ancla exacta, "menos de una vida" sin costo en comida ni saciedad, relevancia > recencia
   y > azar, reproducción desacoplada); CAEN F9-4 (nodo barajado también alarga la vida, con cautela genérica) y F9-7 (conectarse tarde no cuesta).
   Nada se declara con la letra completa. Réplica 1521–1540 en cola tras dE5-v2 y la réplica de BA-v. HANDOFF 15.18.
Además: **dE5 bajo el criterio v2 corrido: NO ENTRA** (ver Pendiente, ítem 2). Observación transversal: v15f y dE5 caen T-A y T-C (ii) con A₁₂ 0.4–0.55, indistinguibles del tronco; posible ERR de criterio, no ahora.
Orden de corrida (un Pool a la vez): BA-v 961–980 ✅ → fase 9 1501–1520 ✅ → dE5-v2 ✅ → réplica BA-v 981–1000 (corriendo desde 15:52) → réplica fase 9 1521–1540.
