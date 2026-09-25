"""calibra_poder.py — CALIBRACION DE PODER (paquete anfitrion, Opus B, 24-sep-2026). EXPLORATORIO de instrumento, no es dato.
Un proceso, <= 6 corridas, semillas de practica 26991-26992. Brazo SIN_TRAGAR de motor_endo (el bicho solo + libres aislados):
mide cuantos cuerpos quedan tras el corte con fundadores sembrados desde el banco de VIDA de ECO v1.1 y dos tasas de comida.
No mira ninguna diferencia entre brazos (sin simbiontes no hay nada que comparar).
"""
import json, os, sys, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
for _d in (os.path.join(RAIZ, 'experimentos', 'generaciones'), os.path.join(RAIZ, 'experimentos', 'juaco_eco'), os.path.join(os.path.dirname(AQUI), 'darwin')):
    if _d not in sys.path: sys.path.insert(0, _d)
sys.dont_write_bytecode = True
import motor_endo as MD, corre_eco as CR, glob, pista2
POOL = []
for v in ('eco_v11_serie_s19401-19420', 'eco_v11_serie_s19421-19440'):
    for f in sorted(glob.glob(os.path.join(RAIZ, 'experimentos', 'juaco_eco', 'datos', v, 'VIDA_s*.json'))):
        POOL += json.load(open(f, encoding='utf-8'))['corte']['banco']
G0 = MD.genoma0(pista2.cfg_fabrica()); lo, hi = MD.rangos(G0)
def huespedes(seed, n=30):
    idx = np.random.default_rng([seed, 0, 33, 0]).choice(len(POOL), size=n, replace=False)
    g = np.array([list(POOL[i]) + [0.9] * 7 for i in idx], float); return np.clip(g, lo, hi)
out = []
for tag, rr, tc, T in (('A r0.03 c40k', 0.03, 40000, 100000), ('B r0.045 c40k', 0.045, 40000, 100000)):
    for s in (26991, 26992):
        t0 = time.time(); e = CR.eco_cfg('VIDA', tc); e['genoma'] = huespedes(s).tolist()
        r = MD.run_solapadas(s, ['FABRICA_SIMB'] * 30, T=T, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=1000, eco=e, r_rep=rr, simb=dict(brazo='SIN_TRAGAR'))
        tt = r['pista']['tam_total']; post = tt[tc // 1000:-1]
        coh = [f for f in r['simb']['ind'] if f[2] <= T - 20000]
        d = dict(cfg=tag, seed=s, seg=round(time.time() - t0, 1), pre_med=float(np.median(tt[10:tc // 1000])), post_med=float(np.median(post)),
                 post_min=int(min(post)), area_post=int(sum(post)), vivos_T=len(r['eco']['vivos_final']), max_vivos=r['pista']['max_vivos'],
                 coh_post=len(coh), r0_post=(round(float(np.mean([f[4] for f in coh])), 3) if coh else None), t_ext=r['eco']['t_ext'], pool=len(POOL))
        print(json.dumps(d), flush=True); out.append(d)
json.dump(out, open(os.path.join(AQUI, 'calibra_poder_salida.json'), 'w'), indent=1)
