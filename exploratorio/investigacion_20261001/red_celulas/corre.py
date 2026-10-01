"""corre.py — corre los brazos de la red de celulas en SUMA mod 7 (30 vistos / 19 retenidos), cambio de regla a RESTA,
olvido, tamano y costo. Exploracion (sin preregistro). Un proceso, numpy puro, segundos por corrida.

Uso:  python corre.py --prior onehot --n0 40 --semillas 10 --TA 3000 --TB 3000 --out datos/onehot_n40.json
      python corre.py --tarea medio ...   (medio sumador: XOR+AND, 4 patrones, 3 clases, sin retenidos)
"""
import argparse, json, time, os
import numpy as np
from red_celulas import RedCelulas, MLP, codifica, tarea, particion, P

BRAZOS = {
    # nombre: (constructor, kwargs)
    'a_red_completa':   dict(plasticidad=True,  vida=True,  credito='individual', barajar=False),
    'b_plast_sin_vida': dict(plasticidad=True,  vida=False, credito='individual', barajar=False),
    'c_vida_sin_plast': dict(plasticidad=False, vida=True,  credito='individual', barajar=False),
    'd_piso':           dict(plasticidad=False, vida=False, credito='individual', barajar=False),
    'e_barajado':       dict(plasticidad=True,  vida=True,  credito='individual', barajar=True),
    'g_grupo':          dict(plasticidad=True,  vida=True,  credito='grupo',      barajar=False),
    'e2_barajado_sin_vida': dict(plasticidad=True, vida=False, credito='individual', barajar=True),
    'g2_grupo_sin_vida': dict(plasticidad=True, vida=False, credito='grupo',     barajar=False),
    'h_solo_boca':      dict(plasticidad=True,  vida=False, credito='individual', barajar=False, eta_in=0.0),
    'f_techo_mlp':      None,
}


def arma_tarea(nombre_tarea, rng):
    if nombre_tarea == 'medio':
        pares = [(0, 0), (0, 1), (1, 0), (1, 1)]
        cod = lambda a, b: np.array([1 - a, a, 1 - b, b], float)
        return pares, [], cod, (lambda regla, a, b: (a + b) if regla == 'suma' else (a - b) % 3), 3, 4
    vistos, ret = particion(rng)
    return vistos, ret, None, tarea, P, None


def evalua(red, pares, cod, fn, regla):
    if not pares: return float('nan')
    return float(np.mean([red.predice(cod(a, b)) == fn(regla, a, b) for a, b in pares]))


def corre_una(brazo, seed, args):
    rng = np.random.default_rng(1000 + seed)
    vistos, ret, cod, fn, K, D = arma_tarea(args.tarea, rng)
    prior = args.prior
    if cod is None: cod = lambda a, b: codifica(a, b, prior)
    if brazo == 'f_techo_mlp':
        red = MLP(seed, H=args.n0, prior=prior if args.tarea != 'medio' else 'onehot', lr=args.lr, n_salidas=K)
        if args.tarea == 'medio': red.D = 4; red.W1 = red.rng.normal(0, 0.5, (4, args.n0))
    else:
        kw = dict(n0=args.n0, prior=prior, eta_in=args.eta_in, eta_out=args.eta_out,
                  sigma=args.sigma, F=args.F, c_exist=args.c_exist, n_salidas=K, directo=not args.sin_directo,
                  regla_in=args.regla_in, c_emit=args.c_emit, E_div=args.E_div, sigma_mut=args.sigma_mut)
        kw.update(BRAZOS[brazo])   # lo que define el brazo manda sobre la linea de comandos
        red = RedCelulas(seed, **kw)
        if args.tarea == 'medio':
            red.D = 4; red.Win = red.rng.normal(0, 1.0, (args.n0, 4)); red.Wdir = np.zeros((4, K))
    res = dict(brazo=brazo, seed=seed, N=[], acc_v=[], acc_r=[], t=[], fase=[])
    cada = args.cada
    hasta = {'A': None, 'B': None}
    rs = np.random.default_rng(2000 + seed)   # orden del flujo (mismo para todos los brazos de una semilla)

    def fase(nombre, regla, T):
        for k in range(T):
            a, b = vistos[rs.integers(len(vistos))]
            red.expone(cod(a, b), fn(regla, a, b))
            if (k + 1) % cada == 0:
                av = evalua(red, vistos, cod, fn, regla); ar = evalua(red, ret, cod, fn, regla)
                res['t'].append(k + 1); res['fase'].append(nombre); res['N'].append(int(red.N))
                res['acc_v'].append(av); res['acc_r'].append(ar)
                if hasta[nombre] is None and av >= 0.9: hasta[nombre] = k + 1

    t0 = time.time()
    fase('A', 'suma', args.TA)
    res['A_vistos'] = evalua(red, vistos, cod, fn, 'suma'); res['A_ret'] = evalua(red, ret, cod, fn, 'suma')
    res['A_hasta09'] = hasta['A']; res['N_finA'] = int(red.N); res['tramposas_A'] = red.tramposas()
    ops_A = red.ops
    fase('B', 'resta', args.TB)
    res['B_vistos'] = evalua(red, vistos, cod, fn, 'resta'); res['B_ret'] = evalua(red, ret, cod, fn, 'resta')
    res['B_hasta09'] = hasta['B']; res['N_finB'] = int(red.N)
    res['A_tras_B_vistos'] = evalua(red, vistos, cod, fn, 'suma')   # OLVIDO: cuanto queda de A tras aprender B
    res['A_tras_B_ret'] = evalua(red, ret, cod, fn, 'suma')
    res['ops_por_exposicion'] = ops_A / max(1, args.TA)
    res['nacimientos'] = getattr(red, 'nacimientos', 0); res['muertes'] = getattr(red, 'muertes', 0)
    res['seg'] = time.time() - t0
    return res


def med_rango(v):
    v = [x for x in v if x is not None and not (isinstance(x, float) and np.isnan(x))]
    if not v: return 'nunca'
    return f"{np.median(v):.2f} [{min(v):.2f}-{max(v):.2f}]" if isinstance(v[0], float) else f"{int(np.median(v))} [{min(v)}-{max(v)}]"


def resumen(todos, brazos, n_sem):
    lineas = []
    cab = "| brazo | A vistos | A retenidos | exp. hasta 0.9 (A) | N fin A | B vistos (readapt.) | exp. hasta 0.9 (B) | A tras B (olvido) | tramposas | ops/exp |"
    lineas.append(cab); lineas.append("|" + "---|" * 10)
    for b in brazos:
        rs = [r for r in todos if r['brazo'] == b]
        nh = sum(1 for r in rs if r['A_hasta09'] is not None); nhB = sum(1 for r in rs if r['B_hasta09'] is not None)
        lineas.append(f"| {b} | {med_rango([r['A_vistos'] for r in rs])} | {med_rango([r['A_ret'] for r in rs])} | "
                      f"{med_rango([r['A_hasta09'] for r in rs])} ({nh}/{n_sem}) | {med_rango([r['N_finA'] for r in rs])} | "
                      f"{med_rango([r['B_vistos'] for r in rs])} | {med_rango([r['B_hasta09'] for r in rs])} ({nhB}/{n_sem}) | "
                      f"{med_rango([r['A_tras_B_vistos'] for r in rs])} | {med_rango([r['tramposas_A'] for r in rs])} | "
                      f"{int(np.median([r['ops_por_exposicion'] for r in rs]))} |")
    return "\n".join(lineas)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--tarea', default='suma7', choices=['suma7', 'medio'])
    ap.add_argument('--prior', default='onehot', choices=['onehot', 'angulos'])
    ap.add_argument('--brazos', default=','.join(BRAZOS.keys()))
    ap.add_argument('--semillas', type=int, default=10); ap.add_argument('--semilla0', type=int, default=1)
    ap.add_argument('--n0', type=int, default=40); ap.add_argument('--TA', type=int, default=3000); ap.add_argument('--TB', type=int, default=3000)
    ap.add_argument('--cada', type=int, default=25)
    ap.add_argument('--eta_in', type=float, default=0.02); ap.add_argument('--eta_out', type=float, default=0.05)
    ap.add_argument('--sigma', type=float, default=0.3); ap.add_argument('--F', type=float, default=0.09); ap.add_argument('--c_exist', type=float, default=0.01)
    ap.add_argument('--lr', type=float, default=0.05); ap.add_argument('--sin_directo', action='store_true')
    ap.add_argument('--regla_in', default='tanteo', choices=['tanteo', 'hebb3'])
    ap.add_argument('--c_emit', type=float, default=0.002); ap.add_argument('--E_div', type=float, default=2.0)
    ap.add_argument('--sigma_mut', type=float, default=0.3)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()
    brazos = args.brazos.split(',')
    todos = []
    t0 = time.time()
    for b in brazos:
        for s in range(args.semilla0, args.semilla0 + args.semillas):
            todos.append(corre_una(b, s, args))
    print(f"# tarea {args.tarea} prior {args.prior} n0 {args.n0} TA {args.TA} TB {args.TB} semillas {args.semillas} ({time.time()-t0:.0f} s)")
    print(resumen(todos, brazos, args.semillas))
    if args.out:
        os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(dict(args=vars(args), resultados=todos, tabla=resumen(todos, brazos, args.semillas)), f, indent=1)
