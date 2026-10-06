# Cola desatendida de la nube (24-sep-2026) — copia para el PC

Scripts que corrieron las series de la tarde sin turnos del coordinador, una a la vez (Pool 3), con commit y push tras cada serie.
- `cola_eco.sh`: ECO v3 serie → v2.1 serie y réplica → v3 réplica → v1.2 serie y réplica (murió con el reinicio del contenedor ~14:3x).
- `cola_eco2.sh`: la misma, relanzada desde ECO v2.1 serie con `--reanuda`. Se detuvo a mano a las 17:07 (ECO v1.2 colgada: nube-9).
- `cola_eco3.sh`: ECO v4 serie y réplica.
- `cola_eco.log`: la bitácora de la cola (hora UTC de cada paso y commit).
- `diag_nube9.py` y su salida: reproduce en UN proceso la muerte silenciosa de ECO v1.2 (reanuda `VIDA_T` s19701 desde su checkpoint y
  el motor sale con `SystemExit` por la guardia de ERR-60: más de 100 000 cuerpos en un linaje). El checkpoint no está en el repo
  (`ckpt/` queda fuera por exclusión local): para reproducirlo hay que volver a correr esa semilla hasta ~770 000 pasos.
Las rutas de los scripts apuntan al scratchpad de la sesión de la nube; en el PC hay que cambiarlas.
