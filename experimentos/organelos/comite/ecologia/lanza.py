# EXPLORATORIO, no es dato
"""lanza.py — lanzador del comite de ecologia: un proceso por corrida, a lo sumo MAXP a la vez (subprocess.Popen, SIN Pool).
Uso: python lanza.py <esc> <T> <MEC1,MEC2,...> <seed_desde> <seed_hasta> [carpeta]
Salta las corridas cuyo JSON ya existe. Escribe progreso en <carpeta>/lanza.log.
"""
import os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
MAXP = 6

esc, T = int(sys.argv[1]), int(sys.argv[2]); mecs = sys.argv[3].split(','); s0, s1 = int(sys.argv[4]), int(sys.argv[5])
carpeta = sys.argv[6] if len(sys.argv) > 6 else os.path.join(AQUI, 'datos')
os.makedirs(carpeta, exist_ok=True)
log = open(os.path.join(carpeta, 'lanza.log'), 'a', encoding='utf-8')
jobs = [(m, s) for s in range(s0, s1 + 1) for m in mecs if not os.path.exists(os.path.join(carpeta, f"{m}_w{esc}_s{s}.json"))]
log.write(f"[{time.strftime('%H:%M:%S')}] lanza w{esc} T{T} {mecs} s{s0}-{s1}: {len(jobs)} corridas\n"); log.flush()
vivos = []
t0 = time.time()
while jobs or vivos:
    while jobs and len(vivos) < MAXP:
        m, s = jobs.pop(0)
        p = subprocess.Popen([sys.executable, os.path.join(AQUI, 'corre_ecologia.py'), m, str(s), str(esc), str(T), carpeta],
                             stdout=open(os.path.join(carpeta, f"{m}_w{esc}_s{s}.out"), 'w'), stderr=subprocess.STDOUT)
        vivos.append((p, m, s))
    time.sleep(2)
    for v in list(vivos):
        if v[0].poll() is not None:
            vivos.remove(v)
            log.write(f"[{time.strftime('%H:%M:%S')}] fin {v[1]} s{v[2]} rc {v[0].returncode} ({round(time.time() - t0)} s)\n"); log.flush()
log.write(f"[{time.strftime('%H:%M:%S')}] LISTO ({round(time.time() - t0)} s)\n"); log.close()
