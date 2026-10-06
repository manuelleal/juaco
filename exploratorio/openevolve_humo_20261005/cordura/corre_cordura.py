"""corre_cordura.py — CORDURA DEL EVALUADOR (el arnes), antes de cualquier busqueda. Un proceso a la vez.
Semillas de CALIBRACION 270001-270002 (no son de busqueda ni de examen). Fundador NO limpio.
  O1 de fabrica, T 100k, 2 semillas       -> debe cruzar 5-8 de 9 (puntaje alto)
  CTRL_O1_SINLIMPIA, T 100k, 2 semillas   -> debe dar 0 de 9
  raiz/programa_inicial.py == CTRL_O1_SINLIMPIA (misma fisica) a T 25k
  O1 a T 25k (para fijar el umbral de la cascada)
"""
import json, os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(AQUI)
PY = sys.executable
PLAN = [("O1", 270001, 25000), ("CTRL_O1_SINLIMPIA", 270001, 25000), (os.path.join(BASE, "raiz", "programa_inicial.py"), 270001, 25000),
        ("O1", 270001, 100000), ("CTRL_O1_SINLIMPIA", 270001, 100000), ("O1", 270002, 100000), ("CTRL_O1_SINLIMPIA", 270002, 100000)]
log = open(os.path.join(AQUI, "cordura.log"), "a", encoding="utf-8")
def di(s):
    print(s, flush=True); log.write(s + "\n"); log.flush()
t00 = time.time()
for ruta, seed, T in PLAN:
    nom = os.path.splitext(os.path.basename(ruta))[0]
    sal = os.path.join(AQUI, f"{nom}_s{seed}_T{T}.json")
    r = subprocess.run([PY, "-B", os.path.join(BASE, "corre_carro.py"), ruta, str(seed), str(T), sal], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        di(f"FALLA {nom} s{seed} T{T}: {r.stderr[-800:]}"); continue
    d = json.load(open(sal, encoding="utf-8"))
    di(f"{nom:22s} s{seed} T{T:6d} {d['seg']:6.1f}s  persisten {d['persisten']}/9  cruzan(R0 real) {d['cruzan_real']}/9  R0 real med {d['R0_real_med']}  "
       f"vida med {d['vida_med']}  fund>10k {d['fund_post10k']}  muertes vol {d['frac_vol']}  sin nada bueno {d['frac_sin_bueno_mundo']}  coherente {d['coherente']}/9")
di(f"total {time.time() - t00:.0f}s")
