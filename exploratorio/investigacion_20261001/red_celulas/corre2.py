"""corre2.py — encargo 2: techo justo, segunda capa, codigos componibles, tramposo a escala, olvido.
Uso: python corre2.py --exp {techo,capas,codigos,tramposo,olvido} [--semillas 10]
Guarda datos/e2_<exp>.json y escribe la tabla en pantalla. Un proceso, numpy puro.
"""
import argparse, json, os, time
import numpy as np
from red2 import Red2, MLP2, arma_tarea, dim_cod

AZAR = {'suma7': 1 / 7, 'paridad3': 0.5, 'paridad4': 0.5}


def ev(red, pats, cod, fn, regla):
    if not pats: return float('nan')
    return float(np.mean([red.predice(cod(*p)) == fn(regla, *p) for p in pats]))


def corre(tarea, codigo, seed, modelo, kw, TA, TB, cada=25):
    rng = np.random.default_rng(1000 + seed)
    vistos, ret, cod, fn, K = arma_tarea(tarea, codigo, rng)
    D = len(cod(*vistos[0]))
    red = MLP2(seed, D, K, **kw) if modelo == 'mlp' else Red2(seed, D, K, **kw)
    rs = np.random.default_rng(2000 + seed)
    hasta = {}; curva = []

    def fase(nombre, T):
        for k in range(T):
            p = vistos[rs.integers(len(vistos))]; red.expone(cod(*p), fn(nombre, *p))
            if (k + 1) % cada == 0:
                av = ev(red, vistos, cod, fn, nombre); curva.append((nombre, k + 1, av, red.N))
                if nombre not in hasta and av >= 0.9: hasta[nombre] = k + 1
    t0 = time.time(); fase('A', TA)
    r = dict(seed=seed, A_v=ev(red, vistos, cod, fn, 'A'), A_r=ev(red, ret, cod, fn, 'A'), A_h=hasta.get('A'), N_A=red.N,
             tramp=red.tramposas(), ops=red.ops / max(1, TA))
    if TB:
        fase('B', TB)
        r.update(B_v=ev(red, vistos, cod, fn, 'B'), B_h=hasta.get('B'), A_tras_B=ev(red, vistos, cod, fn, 'A'), N_B=red.N,
                 A_tras_B_r=ev(red, ret, cod, fn, 'A'))
    r['nac'] = red.nacimientos; r['mue'] = red.muertes; r['seg'] = time.time() - t0; r['curva'] = curva
    return r


def mr(v, ent=False):
    v = [x for x in v if x is not None and not (isinstance(x, float) and np.isnan(x))]
    if not v: return 'nunca'
    return f"{int(np.median(v))} [{min(v)}-{max(v)}]" if ent else f"{np.median(v):.2f} [{min(v):.2f}-{max(v):.2f}]"


def fila(nombre, rs, n, conB=True):
    s = f"| {nombre} | {mr([r['A_v'] for r in rs])} | {mr([r['A_r'] for r in rs])} | {mr([r['A_h'] for r in rs], True)} ({sum(r['A_h'] is not None for r in rs)}/{n}) | {mr([r['N_A'] for r in rs], True)} | {mr([r['tramp'] for r in rs], True)} | {int(np.median([r['ops'] for r in rs]))} |"
    if conB and 'B_v' in rs[0]:
        s += f" {mr([r['B_v'] for r in rs])} | {mr([r['B_h'] for r in rs], True)} ({sum(r['B_h'] is not None for r in rs)}/{n}) | {mr([r['A_tras_B'] for r in rs])} |"
    return s


CAB = "| brazo | A vistos | A retenidos | exp. hasta 0.9 (A) | N | tramposas | ops/exp | B vistos | exp. hasta 0.9 (B) | A tras B |\n|---|---|---|---|---|---|---|---|---|---|"


def brazos_de(exp):
    """(nombre, tarea, codigo, modelo, kwargs, TA, TB)"""
    CEL = dict(credito='cadena', plasticidad=True, vida=False, directo=True)
    if exp == 'techo':
        L = [(f"techo Adam+CE lr {lr}", 'suma7', 'onehot', 'mlp', dict(capas=(40,), lr=lr), 3000, 3000) for lr in (0.003, 0.01, 0.03, 0.1)]
        L.append(("celulas 1 capa (informe 1)", 'suma7', 'onehot', 'cel', dict(CEL, capas=(40,)), 3000, 3000))
        return L
    if exp == 'capas':
        # suma7 one-hot SIN lectura directa (la boca sola debe fallar); tasas de 2 capas: eta_in 0.03, axon intermedio 0.01
        H = dict(CEL, directo=False, eta_in=0.03, eta_med=0.01)
        L = [("solo boca (debe fallar)", 'suma7', 'onehot', 'cel', dict(CEL, capas=(), directo=True), 3000, 0)]
        for prof in (1, 2, 3, 4):
            L.append((f"{prof} capa(s) de 40 CONGELADAS + boca", 'suma7', 'onehot', 'cel', dict(H, capas=(40,) * prof, eta_in=0.0, eta_med=0.0), 3000, 0))
            for cred in ('cadena', 'fa', 'rpe'):
                L.append((f"{prof} capa(s) de 40, aviso {cred}", 'suma7', 'onehot', 'cel', dict(H, capas=(40,) * prof, credito=cred), 3000, 0))
            L.append((f"{prof} capa(s) de 40, TECHO Adam lr 0.01", 'suma7', 'onehot', 'mlp', dict(capas=(40,) * prof, lr=0.01), 3000, 0))
        return L
    if exp == 'capas_scan':
        L = []
        for prof in (1, 2):
            for cred in ('cadena', 'rpe', 'fa'):
                for ei in (0.03, 0.3):
                    for eo in (0.05, 0.2):
                        L.append((f"paridad3 {prof} capa(s) de 6 {cred} eta_in {ei} eta_out {eo}", 'paridad3', None, 'cel',
                                  dict(CEL, capas=(6,) * prof, credito=cred, directo=False, eta_in=ei, eta_out=eo), 3000, 0))
        return L
    if exp == 'codigos':
        L = []
        for codigo in ('onehot', 'binario', 'termometro', 'angulos4'):
            L.append((f"{codigo} celulas 1 capa 40", 'suma7', codigo, 'cel', dict(CEL, capas=(40,)), 3000, 3000))
            L.append((f"{codigo} celulas 2 capas 40", 'suma7', codigo, 'cel', dict(CEL, capas=(40, 40), directo=False, eta_in=0.03, eta_med=0.01), 3000, 3000))
            L.append((f"{codigo} TECHO Adam 40", 'suma7', codigo, 'mlp', dict(capas=(40,), lr=0.003), 3000, 3000))
            L.append((f"{codigo} TECHO Adam 40-40", 'suma7', codigo, 'mlp', dict(capas=(40, 40), lr=0.003), 3000, 3000))
        return L
    if exp == 'codigos_largo':   # sonda: el techo con 10x mas exposiciones, generaliza (grokea) con algun codigo?
        return [(f"{codigo} TECHO Adam 40-40, 30000 exp.", 'suma7', codigo, 'mlp', dict(capas=(40, 40), lr=0.003), 30000, 0)
                for codigo in ('onehot', 'binario', 'angulos4')]
    if exp == 'tramposo':
        V = dict(CEL, capas=(320,), vida=True)
        return [("320 vida, pago individual (informe 1)", 'suma7', 'onehot', 'cel', dict(V), 3000, 3000),
                ("320 vida, impuesto a emision constante 0.01", 'suma7', 'onehot', 'cel', dict(V, c_const=0.01), 3000, 3000),
                ("320 vida, impuesto 0.05", 'suma7', 'onehot', 'cel', dict(V, c_const=0.05), 3000, 3000),
                ("320 vida, pago por camino (grupos de 4)", 'suma7', 'onehot', 'cel', dict(V, camino=4), 3000, 3000),
                ("320 vida, pago por camino (grupos de 16)", 'suma7', 'onehot', 'cel', dict(V, camino=16), 3000, 3000),
                ("320 vida, camino 4 + impuesto 0.01", 'suma7', 'onehot', 'cel', dict(V, camino=4, c_const=0.01), 3000, 3000)]
    if exp == 'olvido':
        S = dict(CEL, capas=(40,), directo=False)
        return [("sin directo, sin vida (base)", 'suma7', 'onehot', 'cel', dict(S), 3000, 3000),
                ("consolida kappa 2, sin vida", 'suma7', 'onehot', 'cel', dict(S, kappa=2.0), 3000, 3000),
                ("consolida kappa 0.5, sin vida", 'suma7', 'onehot', 'cel', dict(S, kappa=0.5), 3000, 3000),
                ("vida sola", 'suma7', 'onehot', 'cel', dict(S, vida=True), 3000, 3000),
                ("vida + consolida kappa 2 (viejas se congelan, nacen nuevas)", 'suma7', 'onehot', 'cel', dict(S, vida=True, kappa=2.0), 3000, 3000),
                ("vida + consolida kappa 0.5", 'suma7', 'onehot', 'cel', dict(S, vida=True, kappa=0.5), 3000, 3000),
                ("TECHO Adam 40", 'suma7', 'onehot', 'mlp', dict(capas=(40,), lr=0.003), 3000, 3000)]
    raise ValueError(exp)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--exp', required=True); ap.add_argument('--semillas', type=int, default=10)
    args = ap.parse_args(); t0 = time.time(); salida = {}
    print(f"## exp {args.exp} ({args.semillas} semillas)\n" + CAB)
    for nombre, tarea, codigo, modelo, kw, TA, TB in brazos_de(args.exp):
        rs = [corre(tarea, codigo, s, modelo, kw, TA, TB) for s in range(1, args.semillas + 1)]
        salida[nombre] = rs; print(fila(nombre, rs, args.semillas), flush=True)
        os.makedirs('datos', exist_ok=True)
        with open(f'datos/e2_{args.exp}.json', 'w', encoding='utf-8') as f: json.dump(salida, f)
    print(f"({time.time() - t0:.0f} s)")
