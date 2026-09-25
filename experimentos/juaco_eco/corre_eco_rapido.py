"""corre_eco_rapido.py — corre_eco.py (runner y juez de JUACO-ECO) con el MOTOR GEMELO (motor_eco_rapido), SIN cambiar su letra.

MISION: llegar a la AGI por este camino. El gemelo solo vale mientras identidad_eco_rapido.py de N/N (regla 9 de EQUIPO.md).

Que hace: importa corre_eco.py tal cual (mismas banderas, mismos MUNDO/SERIE/JUEZ/LARGO/BRAZOS, mismo veredicto(), mismo
juez(), mismo trabajo()) y cambia UNA cosa: el modulo de motor que corre_eco usa (CR.ME) por una copia de motor_eco cuyo
run_solapadas es el del gemelo. Todo lo demas de motor_eco (genoma0, NOMBRES, ...) sigue siendo el original. ME_SHA()
anade los sha del gemelo y de este lanzador a los del original (quedan en RESUMEN.json de la serie).

Uso (SOLO el coordinador lanza --serie / --largo; ERR-115: banderas desconocidas o abreviadas abortan, como en corre_eco):
  python experimentos/juaco_eco/corre_eco_rapido.py --serie --desde 19101 --n 20 --pool 3
  python experimentos/juaco_eco/corre_eco_rapido.py --largo --desde 19301 --n 3 --pool 3 [--reanuda]
OJO: los checkpoints del gemelo NO son los del original (la firma los distingue y aborta): una serie empezada con un motor
se reanuda con el MISMO motor.
"""
import hashlib, os, sys, types

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_eco as CR   # pone generaciones/ en sys.path
import motor_eco as ME
import motor_eco_rapido as MR

ME_GEMELO = types.ModuleType('motor_eco_gemelo')
ME_GEMELO.__dict__.update({k: v for k, v in ME.__dict__.items() if not k.startswith('__')})
ME_GEMELO.run_solapadas = MR.run_solapadas
ME_GEMELO.__doc__ = 'motor_eco con run_solapadas = motor_eco_rapido.run_solapadas (gemelo numba)'
CR.ME = ME_GEMELO

_ME_SHA_ORIGINAL = CR.ME_SHA


def ME_SHA():
    d = dict(_ME_SHA_ORIGINAL())
    for p in ('motor_eco_rapido.py', 'corre_eco_rapido.py'):
        d[p] = hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    d['motor'] = 'GEMELO motor_eco_rapido'
    return d


CR.ME_SHA = ME_SHA

if __name__ == '__main__':
    CR.main()
