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

## 1. Sesión 0 en la nube: calibración — **HECHA el 23-sep (19:14–19:35): FUNCIONA, bits idénticos al PC**
Informe: `datos/humo/nube_calibracion_20260924.md`.
- Máquina: 4 núcleos (Xeon Emerald Rapids, AVX-512) y 15.7 GiB. Por proceso es 1.3–2.2× más rápida que el PC.
- **Pool 3 en la nube** (nproc − 1; rinde lo mismo que el PC con Pool 6). Decisión del coordinador: en la nube nadie más usa la máquina.
- Python 3.13.12 en venv (github.com está bloqueado y no se puede bajar 3.14.2); la salida es idéntica.
- scipy va en `requirements.txt` porque la necesitan los gemelos numba.

**Setup script del entorno** (menú del entorno → Setup script), para que cada sesión arranque lista:
```
uv venv --seed --python /usr/bin/python3.13 /root/venv-juaco
/root/venv-juaco/bin/pip install numpy==2.4.3 numba==0.67.0 llvmlite==0.49.0 scipy==1.17.1
echo 'export PATH=/root/venv-juaco/bin:$PATH' >> ~/.bashrc
```
La tercera línea la propuso la sesión 0: el shell de la sesión toma el PATH de `~/.bashrc`. Se verifica en la siguiente sesión con
`python --version`, que debe dar 3.13.12. Si no da eso, se usa `/root/venv-juaco/bin/python` en cada comando.

El prompt original de la sesión 0 queda abajo como referencia:
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
Pool = 3 (nproc − 1; en la nube nadie más usa la máquina) y con /root/venv-juaco/bin/python, evalúala contra la letra de su preregistro, regístrala (REGISTRO, ESTADO, HANDOFF), commit y push a la rama
nube/<fecha>. Cuando la cola se vacíe, trabaja en los 2 frentes del plan vigente (§3; no en puntajes por nivel) con, a lo sumo, un
equipo de agentes por frente (ver .claude/agents), y si sobra tiempo experimenta según registro/LABORATORIO.md. Toma las decisiones
difíciles y escríbelas con su porqué. No toques el tronco congelado; los niveles los fija el director. Al cerrar, deja todo escrito para
la siguiente sesión.
```

## 2b. Sesión de NOCHE del 23→24-sep-2026 (el director: "que corra de noche; le doy la libertad para probar y experimentar")
Prompt para pegar en la sesión de la nube. El PC del director corre esa noche v14.3, 9b, 6b, 8c y 8b; la nube corre lo demás.

```
Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas). El método manda sobre el cómo. Principio del director: la misión es la AGI, no llenar benchmarks.

1. Antes de nada: git pull de main. Lee NUBE.md (§0, §1, §3 y §4), registro/ESTADO.md (PLAN VIGENTE: máximo 2 frentes) y
   registro/LABORATORIO.md (en especial "Huecos de ciencia"). Verifica que `python --version` dé 3.13.12. Si no, usa
   /root/venv-juaco/bin/python en cada comando. Pool = 3.
2. SERIES (en este orden; antes de cada una, su arnés de identidad debe dar N/N o no se corre):
   a) subida_n10b (decisión del director): python experimentos/subida_n10b/identidad_familia_b.py (42/42), luego
      corre_n10b.py --serie --desde 12701 --n 20 --pool 3 y la réplica --desde 12721.
   b) JUACO-ECO, frente 2: python experimentos/juaco_eco/identidad_eco.py (41/41), después
      corre_eco.py --serie --prueba_pool --desde 19031 --n 2 --pool 2, luego la serie --desde 19101 --n 20 --pool 3, y la réplica
      --desde 19121 si hay tiempo. Si la sesión va a cortarse, sube los checkpoints para retomar con --reanuda.
   Evalúa cada serie contra la LETRA de su preregistro: el runner imprime VEREDICTO. No muevas umbrales: si hace falta, es ERR y se
   anota, no se aplica.
3. LIBERTAD PARA EXPERIMENTAR (el director te la da esta noche): usa el núcleo libre (un proceso a la vez) para prototipos
   EXPLORATORIOS en experimentos/exploratorio_nube_20260924/, con NOTA_EXPLORATORIA.md cuya primera línea diga "EXPLORATORIO — no es
   dato". Temas, en orden:
   (i) "arriesgar según la reserva": probar lo desconocido y limpiar sólo cuando min(E, Ag) es alto. Aparece en v14.3, nivel 8,
       Frankenstein y O1. Sobre APR/FABRICA en la pista de la carrera.
   (ii) "aprender prediciendo": un órgano local que predice en cada paso lo que verá o sentirá y aprende del error.
   (iii) lo que tú veas más prometedor para que el MISMO bicho sostenga su vida con comida limitada.
   Cada número con su comando y su semilla. Ablaciones al menos contra FABRICA/APR y O1.
4. PRESUPUESTO: el crédito es de 250 USD hasta el 5-nov. Esta noche, como máximo 2 agentes de apoyo en total (por ejemplo un auditor
   al final). Lo demás lo haces tú. Correr series gasta poco; muchos agentes gastan mucho.
5. PROHIBIDO: editar el tronco congelado, manifiesto.py o MANIFEST.txt (la guardia lo bloquea); congelar; mover umbrales tras ver datos;
   declarar porcentajes de nivel; hacer merge a main; borrar datos; forzar push.
6. REGISTRO SIN CONFLICTOS: NO edites registro/ESTADO.md, REGISTRO_etapas_1_2.md ni HANDOFF.md (el PC los está usando). Escribe todo en
   registro/NUBE_BITACORA_20260924.md: qué corriste, con hora, comando, sha y veredicto por la letra; lo exploratorio aparte y
   marcado; decisiones difíciles con su porqué; qué falló y qué propones para mañana. Haz commit y push a la rama nube/noche-20260924
   al menos cada hora, para que nada se pierda. Mañana el coordinador lo integra.
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
