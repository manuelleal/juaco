# ERR-130..132: correcciones de protocolo antes de la serie del anfitrión (nube, 25-sep-2026, ~01:45)

Salen de la auditoría de sólo lectura (`juaco-auditor`), cuyo veredicto fue LISTO CON CORRECCIONES. Se escriben ANTES de correr cualquier semilla de 26001–26040.
Ninguna cambia el mecanismo, la letra, los umbrales ni el código. El `PREREGISTRO_anfitrion.md` no se edita, porque el runner registra su sha.

## ERR-130: cambio de forma de P2 sin ERR (regla 11 de EQUIPO)
- **Qué cambió.** La cohorte de P2 pasó de los vivos tras el corte a **todos los nacidos con t_nace ≥ 10 000**, vivero incluido y sin fundadores (`PREREGISTRO_anfitrion.md:110-113`).
- **Qué faltó.** Es un cambio de forma del criterio, y la regla 11 exige numerarlo aunque se haga antes de la serie. `INFORME.md:46` sólo cubre "nada cambió tras el humo".
- **Sesgo.** `calibra_poder.py:25` corre sólo el brazo `SIN_TRAGAR`, así que la calibración vio el tamaño de muestra y no quién ganaba. No hay indicio de sesgo.
- **Orden.** No es auditable por commits: calibración, preregistro y humo llegaron en un solo commit, `f088f26`. Se sostiene por inferencia.
- **Regla derivada.** El próximo paquete se commitea por pasos: calibración → enmienda → humo.

## ERR-131: sobre-afirmación en la calibración
- El texto dice "ni un mundo más grande arregla el poder", pero `calibra_poder.py` sólo varía `r_rep` (0.03 / 0.045) con `mundo_n` 30 fijo.
- El tamaño de mundo no se calibró en este paquete; lo respalda una cita cruzada a ECO v1.1 en w90.
- No afecta la letra.

## ERR-132: la sanción lee una tabla por letra, no el ΔS de la mordida
- **Cómo está hecho.** `control_anfitrion.py:86` precalcula `danina[k] = min(EFECTO[VAL_VIVO[k]]) < 0`, y `decision()` lo consulta (`:150-157`) antes de que `motor_anf.py:385` aplique el ΔS.
- **Por qué equivale en este mundo.** Es equivalente bit a bit al daño sentido: la mordida aplica exactamente `EFECTO[VAL_VIVO[kk]]`, y ni `VAL_VIVO` ni `EFECTO` se reasignan durante la corrida (se verificó con grep en `motor_anf.py`, `motor_endo.py` y `pista2.py`: sólo se asignan al arrancar).
- **Qué más usa.** La puerta usa además `mordio` y `b.sm[1][kk] > 0`, el canal del propio cuerpo; ninguna de las dos es información del mundo.
- **Lectura.** La sanción responde a la consecuencia física de la letra mordida. No "sabe" qué letra es mala más allá de lo que la mordida le hace.
- **Límite escrito.** En un mundo con cambio de valencia a mitad de corrida (por ejemplo, el A↔B de `codigo/`), la tabla quedaría vieja y sería información privilegiada. Ahí la sanción tiene que leer el `dS` de la mordida.
