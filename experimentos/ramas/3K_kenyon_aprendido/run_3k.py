"""
run_3k.py - experimento 3K. Malla preregistrada, 20 semillas, mundo-regla.
Salida: datos/3K_kenyon_<ts>.csv y .json con cabecera de procedencia. No sobrescribe.
Uso: python run_3k.py [semillas]
"""
import sys, os, json, csv, hashlib, platform, datetime
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import numpy as np
from multiprocessing import get_context
import organismo_3k as o3

T = 200000
F2 = 100000
LRS = [0.003, 0.01, 0.03]
MODOS = ['hebb_visita', 'hebb_mordida', 'error']
VARIANTES = [('congelado', True), ('aprende', False)]


def celdas():
    """Las 10 celdas de la malla preregistrada: fijo + 3 modos x 3 lr."""
    c = [('fijo', 0.0)]
    for m in MODOS:
        for lr in LRS:
            c.append((m, lr))
    return c


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


# ---------------- metricas ----------------
def tasas(r, pats, bins):
    """tasa macro de mordida por visita, por clase, sobre `pats`, sumando `bins`."""
    out = {}
    for cls in ('comida', 'veneno'):
        ks = [k for k in pats if o3.valencia_regla(k) == cls]
        rr = []
        for k in ks:
            v = sum(r['vis'][k][b] for b in bins)
            m = sum(r['mord'][k][b] for b in bins)
            if v > 0:
                rr.append(m / v)
        out[cls] = float(np.mean(rr)) if rr else float('nan')
        out[cls + '_vis'] = int(sum(sum(r['vis'][k][b] for b in bins) for k in ks))
    return out


def precision(r, pats, bins):
    t = tasas(r, pats, bins)
    return 0.5 * t['comida'] + 0.5 * (1 - t['veneno']), t['comida'], t['veneno']


def estructura_kw(KW, codes, pats):
    px = o3.PX_REL
    sd = KW.std(axis=0)
    ratio_disp = float(sd[px] / np.mean([sd[j] for j in range(6) if j != px]))
    mu = KW.mean(axis=0)
    ratio_media = float(mu[px] / np.mean([mu[j] for j in range(6) if j != px]))
    food = [k for k in pats if o3.valencia_regla(k) == 'comida']
    pois = [k for k in pats if o3.valencia_regla(k) == 'veneno']
    f = np.zeros(o3.NK); p = np.zeros(o3.NK)
    for k in food: f[codes[k]] += 1
    for k in pois: p[codes[k]] += 1
    f /= len(food); p /= len(pois)
    usadas = (f + p) > 0
    sel = float(np.mean(np.abs(f[usadas] - p[usadas]))) if usadas.any() else float('nan')
    ks = sorted(pats)
    intra, inter = [], []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            ov = len(set(codes[ks[i]]) & set(codes[ks[j]]))
            (intra if o3.valencia_regla(ks[i]) == o3.valencia_regla(ks[j]) else inter).append(ov)
    mi, me = float(np.mean(intra)), float(np.mean(inter))
    return dict(ratio_disp=ratio_disp, ratio_media=ratio_media, sel_clase=sel,
                solap_intra=mi, solap_inter=me,
                ratio_solap=float(mi / me) if me > 1e-9 else float('nan'),
                celdas_usadas=int(usadas.sum()), uso_max=int((f * len(food) + p * len(pois)).max()))


def analiza(r):
    tren, test = r['tren'], r['test']
    pats = sorted(list(tren) + list(test))
    Wa = r['W_apriori']
    # acc de signo sobre el valor a priori de los patrones de test
    acc = []
    for k in test:
        w = Wa[k]
        good = (w > 0) if o3.valencia_regla(k) == 'comida' else (w < 0)
        acc.append(0.5 if abs(w) < 0.02 else (1.0 if good else 0.0))
    # correlaciones sobre los 10 de test, codigos y pesos en t=F2
    clase = np.array([1.0 if o3.valencia_regla(k) == 'comida' else -1.0 for k in test])
    W = np.array([Wa[k] for k in test])
    O = []
    for k in test:
        c = set(r['codes_f2'][k])
        O.append(sum((1.0 if o3.valencia_regla(y) == 'comida' else -1.0) * len(c & set(r['codes_f2'][y]))
                     for y in tren))
    O = np.array(O, float)

    def pr(a, b):
        if a.std() < 1e-12 or b.std() < 1e-12:
            return float('nan')
        return float(np.corrcoef(a, b)[0, 1])

    d = dict(deaths=r['deaths'], acc_signo=float(np.mean(acc)),
             r_clase=pr(W, clase), r_solap=pr(W, O),
             Wa_test_comida=float(np.median([Wa[k] for k in test if o3.valencia_regla(k) == 'comida'])),
             Wa_test_veneno=float(np.median([Wa[k] for k in test if o3.valencia_regla(k) == 'veneno'])),
             Wa_tren_comida=float(np.median([Wa[k] for k in tren if o3.valencia_regla(k) == 'comida'])),
             Wa_tren_veneno=float(np.median([Wa[k] for k in tren if o3.valencia_regla(k) == 'veneno'])))
    # precision fase 2 completa y por cuarto, en test y en entrenamiento
    p, tc, tv = precision(r, test, [4, 5, 6, 7])
    d.update(prec_test=p, tasa_test_comida=tc, tasa_test_veneno=tv)
    for qi in range(4):
        p4, c4, v4 = precision(r, test, [4 + qi])
        d[f'prec_test_q{qi+1}'] = p4
        d[f'tasaC_test_q{qi+1}'] = c4
        d[f'tasaV_test_q{qi+1}'] = v4
    pt, tct, tvt = precision(r, tren, [4, 5, 6, 7])
    d.update(prec_tren=pt, tasa_tren_comida=tct, tasa_tren_veneno=tvt)
    p1, c1, v1 = precision(r, tren, [0, 1, 2, 3])
    d.update(prec_tren_f1=p1)
    # mordidas totales
    d['mord_comida'] = int(sum(sum(r['mord'][k]) for k in pats if o3.valencia_regla(k) == 'comida'))
    d['mord_veneno'] = int(sum(sum(r['mord'][k]) for k in pats if o3.valencia_regla(k) == 'veneno'))
    # estructura de KW: final, y en t=F2 (antes de ver los de test)
    for suf, KW, codes in (('', r['KW'], r['codes_fin']), ('_f2', r['KW_f2'], r['codes_f2'])):
        for kk, vv in estructura_kw(KW, codes, pats).items():
            d[kk + suf] = vv
    d['deriva_kw'] = float(np.abs(r['KW'] - r['KW0']).mean())
    return d


def _job(a):
    s, modo, lr, var, cong = a
    r = o3.run(s, T=T, mundo='regla', kenyon_mode=modo, k_lr=lr,
               fase2_en=F2, congelar_fase2=cong)
    d = analiza(r)
    d.update(seed=s, modo=modo, k_lr=lr, variante=var)
    return d


if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seeds = list(range(1, S + 1))
    jobs = [(s, m, lr, var, cong) for (m, lr) in celdas() for (var, cong) in VARIANTES for s in seeds]
    print(f"3K: {len(jobs)} corridas de {T} pasos ({len(celdas())} celdas x {len(VARIANTES)} variantes x {S} semillas)")
    t0 = datetime.datetime.now()
    with get_context('spawn').Pool() as pool:
        rows = pool.map(_job, jobs, chunksize=1)
    dt = (datetime.datetime.now() - t0).total_seconds()
    print(f"hecho en {dt:.0f} s")

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    proc = dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),
                rama='3K_kenyon_aprendido', T=T, fase2_en=F2, semillas=S,
                python=platform.python_version(), numpy=np.__version__,
                plataforma=platform.platform(),
                sha256_16=dict(organismo_3k=sha(os.path.join(HERE, 'organismo_3k.py')),
                               run_3k=sha(os.path.join(HERE, 'run_3k.py')),
                               PREREGISTRO=sha(os.path.join(HERE, 'PREREGISTRO.md')),
                               organismo_v6=sha(os.path.join(ROOT, 'organismo', 'organismo_v6.py'))),
                malla=dict(celdas=[list(c) for c in celdas()], variantes=[v[0] for v in VARIANTES]),
                mundo=dict(n_patrones=20, px_activos=o3.N_ACT, px_relevante=o3.PX_REL,
                           tren=10, test=10, particion_rng='default_rng(10000+seed)'),
                segundos=dt)
    base = os.path.join(ROOT, 'datos', f'3K_kenyon_{ts}')
    with open(base + '.json', 'w', encoding='utf-8') as f:
        json.dump(dict(procedencia=proc, filas=rows), f, indent=1)
    cols = ['seed', 'modo', 'k_lr', 'variante'] + [k for k in rows[0] if k not in ('seed', 'modo', 'k_lr', 'variante')]
    with open(base + '.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow([f'# procedencia: {json.dumps(proc)}'])
        w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols])
    print("escrito:", base + '.csv', '/', base + '.json')
