"""pasajes_juguete.py — JUGUETE EXPLORATORIO de Fable (28-sep-2026, reunion): pasajes seriados en ECO (base ING: FABRICA_ECO + vivero
permanente), para decidir LARGO del pasaje y NUMERO de pasajes. NO es el experimento de Opus A. Sin preregistro. Sin commits.
Mecanismo: cadena de n_pas pasajes de T_p pasos. Al final de cada pasaje, 90 genomas sorteados CON REPOSICION (rng propio, declarado) de
los vivos en T (vivos_final[i][4:], 18 genes) siembran los 90 fundadores del siguiente (motor_eco eco['genoma']). Genetica CEREBRO
(15 genes, p 0.05, sigma 0.15, banco 200, 8 sombras), la de ECO_SEL_ING. Control RES: cada pasaje siembra con G0 (sin herencia entre
pasajes). Semilla del mundo por pasaje = base*10 + k (base 4700x: libre al grep de 18:50).
Uso: python pasajes_juguete.py --Tp 50000 --npas 8 --semillas 47001,47002,47003 --salida juguete_T50k
"""
import argparse, json, os, sys, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(ORG, 'eco_sel_ing'))
import nucleo_eco_sel_ing as N
N.usa_gemelo()
NOM = ('alpha', 'tau_e', 'aversion', 'rep_umbral', 'eta_s', 'memoria_rechazo')


def corre_pasaje(seed, Tp, gs):
    k2 = []
    def cb(li, row, g):
        if row[4] < 0 or row[4] >= Tp // 2: k2.append((row[3], row[4], row[6]))
    r = N.CR.ME.run_solapadas(seed, N.carros_de(N.FAB), T=Tp, diag=0, mundo_n=N.MUNDO['esc'], tope_cuerpos=N.MUNDO['tope'],
                              muestra=N.MUNDO['muestra'], eco=N.eco_de('CEREBRO', Tp, genoma=gs, ind_cb=cb))
    E = r['eco']; P = r['pista']
    ex = N._extra_ing(k2, Tp)
    G = list(E['genes']); V = np.array([v[4:] for v in E['vivos_final']]) if E['vivos_final'] else np.zeros((0, len(G)))
    med = {n: (round(float(np.median(V[:, G.index(n)])), 4) if len(V) else None) for n in NOM}
    G0 = np.array(E['G0']); dist = (round(float(np.mean(np.abs(np.log(V / G0)))), 4) if len(V) else None)
    return dict(vivos_T=len(V), K=round(ex['K_nac'] + ex['K_fund'], 3), K_nac=ex['K_nac'], fund_2a=ex['fund_2a'], n_nac=E['n_nac'],
                n_refund=E['n_refund'], genes=med, dist_G0=dist, bloqueados=P['bloqueados']), V, list(E['G0'])


def cadena(base, Tp, npas, brazo, muestra_n=90):
    gs = None; filas = []; rng = np.random.default_rng(base * 7 + {'SEL': 1, 'RES': 2, 'BAR': 3}[brazo])
    for k in range(npas):
        t0 = time.time()
        res, V, G0 = corre_pasaje(base * 10 + k, Tp, gs)
        res.update(pasaje=k, seed=base * 10 + k, brazo=brazo, seg=round(time.time() - t0, 1)); filas.append(res)
        print(f"  {brazo} s{base} p{k}: vivos_T {res['vivos_T']} K {res['K']} K_nac {res['K_nac']} fund_2a {res['fund_2a']} "
              f"alpha {res['genes']['alpha']} tau_e {res['genes']['tau_e']} avers {res['genes']['aversion']} dist {res['dist_G0']} ({res['seg']} s)", flush=True)
        if brazo in ('SEL', 'BAR'):
            if len(V) == 0: print('  cadena extinta'); break
            M = V[rng.integers(len(V), size=muestra_n)]
            if brazo == 'BAR':   # RESORTEO: cada gen barajado entre los 90 cuerpos (misma distribucion marginal, sin genotipo heredado)
                M = M.copy()
                for j in range(M.shape[1]): M[:, j] = M[rng.permutation(M.shape[0]), j]
            gs = M.tolist()
        else:
            gs = None   # RES: G0 de fabrica en cada pasaje
    return filas


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--Tp', type=int, default=50000); ap.add_argument('--npas', type=int, default=8)
    ap.add_argument('--semillas', default='47001'); ap.add_argument('--brazos', default='SEL,RES'); ap.add_argument('--salida', default='juguete')
    a = ap.parse_args()
    out = {}
    for s in [int(x) for x in a.semillas.split(',')]:
        for b in a.brazos.split(','):
            out[f"{b}_s{s}"] = cadena(s, a.Tp, a.npas, b)
            with open(os.path.join(AQUI, a.salida + '.json'), 'w') as f: json.dump(dict(Tp=a.Tp, npas=a.npas, cadenas=out), f)
    print('listo', a.salida)
