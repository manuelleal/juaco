"""diagnostico_mensaje.py — SUBIDA N10b, DIAGNOSTICO (no es dato, no puntua): que lleva el mensaje de FAMILIA_PARTO (tanda 1).

MISION: llegar a la AGI por este camino.

Pregunta: por que PARTO no le gana a BAR (11/20 en 12301-12320)? Hipotesis del creador: el mensaje (nodo heredado + ultimas 20
mordidas del padre VIVO) casi no trae R negativas (el padre que llega a parir casi no muerde B/D en sus ultimas 20 mordidas), asi
que permutar las R entre entradas (BAR) casi no cambia nada: no hay contenido discriminante que barajar.
Un proceso, semilla de PRACTICA 12392 (tanda 1: practica 12391-12399), T = 20000, monocultivo PARTO. Solo LEE los carros de
experimentos/subida_n10/carros (no los edita): envuelve al_parir para contar (letra, necesidad, R) de cada mensaje entregado.
"""
import collections, importlib.util, json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones'); sys.path.insert(0, GEN)
import pista2 as P2, motor_convive as MC

KNOWN = {'--T', '--seed'}
args = sys.argv[1:]
for x in args:
    if x.startswith('--') and x not in KNOWN: raise SystemExit(f"diagnostico_mensaje: bandera desconocida {x}")
T = int(args[args.index('--T') + 1]) if '--T' in args else 20000
SEED = int(args[args.index('--seed') + 1]) if '--seed' in args else 12392
if not 12391 <= SEED <= 12399: raise SystemExit("diagnostico_mensaje: solo semillas de practica 12391-12399")

p = os.path.join(RAIZ, 'experimentos', 'subida_n10', 'carros', 'FAMILIA_PARTO.py')
spec = importlib.util.spec_from_file_location('diag_parto', p); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
CF = P2.cfg_fabrica(); PAT = CF['PAT']
def letra(v): return next(k for k in 'ABCD' if [float(z) for z in PAT[k]] == [float(z) for z in v])

CUENTA = collections.Counter(); NMSG = [0]; NEG = []; NEG_PROPIO = []; LEN = []
orig = M.Carro.al_parir
def al_parir(self, info):
    m = orig(self, info); NMSG[0] += 1; LEN.append(len(m))
    neg = 0
    for pv, r, n in m:
        CUENTA[(letra(pv), n, r)] += 1; neg += int(r < 0)
    NEG.append(neg / max(1, len(m)))
    prop = m[-min(len(m), self.NODO_K):]; NEG_PROPIO.append(sum(1 for _, r, _ in prop if r < 0))
    return m
M.Carro.al_parir = al_parir
t0 = time.time()
r = P2.run(SEED, [('FAMILIA_PARTO', M)] * 9, T=T, diag=0, solapadas=1, reposicion='fija', tope_cuerpos=MC.TOPE_DEF, r_rep=MC.R_REP)
tot = sum(CUENTA.values())
out = dict(seed=SEED, T=T, seg=round(time.time() - t0, 1), mensajes=NMSG[0], largo_med=sorted(LEN)[len(LEN) // 2] if LEN else None,
           frac_neg_media=round(sum(NEG) / max(1, len(NEG)), 4),
           frac_msg_sin_neg_propio=round(sum(1 for x in NEG_PROPIO if x == 0) / max(1, len(NEG_PROPIO)), 4),
           entradas={f"{k[0]}|n{k[1]}|R{k[2]:+.0f}": v for k, v in sorted(CUENTA.items())}, total=tot)
print(json.dumps(out, indent=1))
os.makedirs(os.path.join(AQUI, 'datos', 'humo'), exist_ok=True)
json.dump(out, open(os.path.join(AQUI, 'datos', 'humo', f'diag_mensaje_parto_s{SEED}_T{T}.json'), 'w'), indent=1)
