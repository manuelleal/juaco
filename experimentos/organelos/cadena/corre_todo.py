# EXPLORATORIO, no es dato
"""corre_todo.py — lanza las corridas de la cadena, un proceso por corrida, máximo 4 a la vez (subprocess.Popen, sin Pool)."""
import subprocess, sys, os, time
AQUI = os.path.dirname(os.path.abspath(__file__))
T = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
TRABAJOS = [('EVO', s, 1, 1) for s in (32001, 32002, 32003, 32004)] + [('FIJO', 32001, 0, 1), ('FIJO', 32002, 0, 1), ('SINVENENO', 32001, 1, 0), ('SINVENENO', 32002, 1, 0)]
MAX = 4
vivos = []; cola = list(TRABAJOS); t0 = time.time()
while cola or vivos:
    vivos = [p for p in vivos if p.poll() is None]
    while cola and len(vivos) < MAX:
        brazo, seed, evo, ven = cola.pop(0)
        out = os.path.join(AQUI, 'datos', f'{brazo}_{seed}.json')
        log = open(os.path.join(AQUI, 'datos', f'{brazo}_{seed}.log'), 'w')
        p = subprocess.Popen([sys.executable, os.path.join(AQUI, 'cadena.py'), '--seed', str(seed), '--T', str(T), '--evo', str(evo), '--veneno', str(ven), '--out', out, '--cada', '50'], stdout=log, stderr=subprocess.STDOUT)
        vivos.append(p); print(f'lanzado {brazo} {seed} pid {p.pid} {time.time()-t0:.0f}s', flush=True)
    time.sleep(5)
print(f'TODO TERMINADO {time.time()-t0:.0f}s')
