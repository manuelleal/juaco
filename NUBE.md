# NUBE — cómo trabaja JUACO sin el PC del director

> Escrito el 23-sep-2026 por el coordinador, a pedido del director: *"la idea es dejar trabajando el proyecto solo, tú y él, y darle
> palo a ver qué resulta; llegar al borrador de la AGI; así puedes correr mundos más grandes, muy grandes, e ir modificando"*.
> Cada sesión en la nube empieza leyendo ESTE archivo.

## Crédito (texto oficial de la oferta, 23-sep-2026)
- **250 USD en créditos para sesiones en la nube.** Se aplican solos al iniciar una sesión en claude.ai/code con el repo conectado.
  Sólo para suscriptores Pro y Max. **Vencen el 5-nov-2026, 2:59 a.m. (GMT-5).** Cuando se acaban o vencen, rige el uso normal del plan.
- **NO valen para Proyectos ni para Rutinas.** Una rutina programada consumiría el plan normal, no el crédito; por eso las sesiones las
  lanza el director a mano (desde el PC o el celular), una por entregable.
- La sesión corre en un entorno aislado: se puede cerrar el computador y volver a revisar el resultado como **pull request**.
- **Presupuesto:** del 23-sep al 5-nov son unas 6 semanas, es decir ~40 USD por semana si se reparte parejo. La sesión 0 mide cuánto
  consume una sesión; con eso se fija el ritmo. Lo caro son los tokens de muchos agentes Opus en paralelo, así que en la nube se prefieren
  sesiones que corren series largas con pocos agentes. Los diseños con equipos de 3 van con medida (uno por frente).

## 0. Misión y lo que no cambia
- Misión: **llegar a la AGI por este camino** (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
  controles y réplicas). El método manda sobre el cómo. "Borrador de AGI" = los niveles 1–13 del brief (`BRIEF_ORIGINAL_y_estado.md`,
  `registro/HORIZONTE_frontera.md`) al 80–100 % con réplica, y JUACO-ECO produciendo una capacidad que nadie diseñó. Nada se declara sin dato.
- Reglas: `CLAUDE.md` y `registro/EQUIPO.md` (1–15). Tronco congelado (`python manifiesto.py --check`; **nunca** `manifiesto.py` sin
  `--check`, regenera `MANIFEST.txt`). Criterio de tronco vigente: `registro/CRITERIO_TRONCO_v4.md`.
- Protocolo de cada bloque: preregistro commiteado → arnés de identidad N/N → humo → serie → réplica en semillas nuevas → REGISTRO +
  ESTADO + HANDOFF → commit → push. Umbral cambiado tras ver datos = ERR numerado (regla 11). Vocabulario prohibido sin medida:
  planifica, entiende, población, evoluciona, especie, consciente.
- Agentes y skills del equipo están en `.claude/agents/` y `.claude/skills/` (creador Opus, compilador, auditor, cronista, probador,
  explorador; /juaco-estado, /juaco-bloque, /juaco-cierre, /juaco-err, /veredicto, /encargo). Cada encargo empieza con la misión.
- Decisiones difíciles sin el director: se toman y se escriben en `registro/ESTADO.md`, sección "Decisiones del coordinador en ausencia
  del director", con hora, opción tomada, alternativa descartada y porqué. **Los porcentajes de nivel los fija el director.**

## 1. Sesión 0 en la nube: calibración (obligatoria, barata)
Prompt para pegar:

```
Lee NUBE.md, CLAUDE.md y registro/ESTADO.md. Instala dependencias con `pip install -r requirements.txt` (Python 3.12+; anota la versión
real de Python, numpy y numba). Anota `nproc` y la RAM. No modifiques código ni criterios.
Corre estos arneses de identidad y compara su última línea con la salida guardada en el repo:
  python experimentos/subida_n8/identidad_n8.py        # debe dar TOTAL 26/26   (en el PC: ~55 s)
  python experimentos/generaciones/identidad_convive.py  # debe dar 37/37         (en el PC: ~134 s)
Si alguno NO da N/N, detente y reporta: puede ser otra versión de numpy (bits distintos); no corras series.
Si dan N/N, corre un humo corto: python experimentos/subida_n8/corre_n8.py --humo  (un proceso) y anota el tiempo.
Escribe datos/humo/nube_calibracion_<fecha>.md con: versiones, nproc, RAM, tiempos contra el PC, y cuántos procesos de Pool recomiendas
(nproc - 2). Commit en una rama nube/calibracion y push.
```

## 2. Sesión de trabajo autónomo (después de calibrar)
Prompt para pegar (se puede repetir; cada sesión retoma de ESTADO.md):

```
Lee NUBE.md, CLAUDE.md, registro/ESTADO.md (bloque más reciente y "Decisiones del coordinador") y la cola de registro/HANDOFF.md.
Trabaja de forma autónoma siguiendo la §3 de NUBE.md: toma la siguiente serie de la cola, verifica su arnés de identidad, córrela con
Pool = nproc - 2, evalúala contra la letra de su preregistro, regístrala (REGISTRO, ESTADO, HANDOFF), commit y push a la rama
nube/<fecha>. Cuando la cola se vacíe, lanza la siguiente tanda del nivel más lejos de 80 % con un equipo de 3 agentes
(explorador -> creador -> auditor, ver .claude/agents) y sigue. Toma las decisiones difíciles y escríbelas con su porqué en ESTADO.md.
No toques el tronco congelado; los niveles los fija el director. Al cerrar, deja ESTADO.md al día para la siguiente sesión.
```

## 3. Orden de trabajo en la nube (se actualiza en cada cierre) — PLAN VIGENTE del 23-sep: **máximo 2 frentes**
> Director, 23-sep: *"¿qué sentido tendría llenar benchmarks si el bicho no hace nada? Esa es la misión real: llegar a la AGI"*.
> Por eso no se persiguen puntajes por nivel en cajas separadas: cuenta lo que el MISMO organismo hace en un mundo común.
> Frente 1 = v14.3 (punto 2 de abajo). Frente 2 = gemelo rápido + JUACO-ECO por escalones (punto 3). Nada nuevo hasta cerrar uno.
1. **Series pendientes con paquete verificado** (ver ESTADO.md, "Cola de series"): cada una con su arnés antes.
2. **v14.3** (`experimentos/tronco_v14_3/`): tronco v14.2 + mapa (n6) + boca aprendida (aprende_barrer) + reparación N del nivel 7
   (si su réplica repitió) → pista de la carrera del 22-sep contra O1 → examen de tronco v4 → congelar con manifiesto propio.
3. **JUACO-ECO** (`experimentos/juaco_eco/`): mundos grandes y muy grandes con el organismo real, energía finita, herencia con mutación,
   juez automático, control de mutación sin selección. Escalar por pasos: primero medir pasos/s, después 10×, después 100× del tamaño
   de la pista de la carrera, con checkpoints reanudables. La nube existe para esto: corridas largas sin el PC.
4. **Órganos** pendientes (uno a la vez, por límite medido): curiosidad con presupuesto (n8b), modelo de sí que predice (n9b), memoria
   lenta con repaso (n8c), herencia de lo vivido (n10b), interruptor explorar/explotar. El Frankenstein (`experimentos/frankenstein/`)
   es EXPLORATORIO: sólo inspira qué rehacer con protocolo.

## 3b. Laboratorio de agentes investigadores
Ver `registro/LABORATORIO.md`: rondas investigar → criticar → diseñar → auditar → correr → registrar → integrar, con 70/20/10 de
presupuesto (protocolo / riesgo alto / exploratorio). Cuando la cola se vacía, la sesión autónoma lanza una ronda de investigación.

## 4. Presupuesto y frenos
- **Guardia mecánica** (`.claude/settings.json` → `.claude/guardia.sh` → `.claude/guardia.py`, hook PreToolUse). Bloquea sola:
  - `manifiesto.py` sin `--check`;
  - editar congelados, `MANIFEST.txt` o `manifiesto.py`;
  - commitear con `MANIFEST.txt` sucio o con un congelado roto;
  - `git push --force`, `git reset --hard`, `git clean` y `rm -r` de datos, experimentos, registro u organismo;
  - `corre_*.py --help` (ERR-115).

  Única llave: la variable de entorno `JUACO_CONGELAR=1`, que la pone un humano en el entorno de la sesión para congelar una versión
  nueva con permiso del director. Probada el 23-sep con 22 casos, más 5 de commit en un repo de juguete.
- Antes de lanzar algo largo, estimar CPU (el humo da el tiempo por corrida) y escribirlo en el preregistro.
- Un bloque que su propio creador espera NO (p ≥ 0.9) va al final de la cola.
- Si dos series seguidas de la misma línea dan NO, se cierra la línea y se registra; no se insiste con variaciones sin hipótesis nueva.
- Nada destructivo: no borrar datos, no reescribir historia de git, no forzar push a main. Trabajo en ramas `nube/<fecha>`; el director
  (o el coordinador en su PC) integra a main.
