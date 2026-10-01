"""sonda_reactor.py — SONDA DE VALIDEZ del Reactor (1-oct-2026). NO es un experimento: no declara nada.

Mision: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con controles
y replicas).

Pregunta: los tres supuestos NO verificados de investigacion_20261001/ENTREGA_1_reactor.md: (1) el motor de BLOQUES corre a esc
~900-1200; (2) el costo escala lineal; (3) la poblacion sube a cientos y se sostiene.

Como: ENVOLTURA de experimentos/organelos/bloques/opusM/corre_bloques.py (se IMPORTA, no se toca; sha fijado abajo). Lo unico que
cambia es, EN ESTE PROCESO, el dict MUNDO del nucleo (esc, n0, tope) antes de llamar a corre_bloques.corre(), y se restaura despues.
La telemetria extra (formas de regla, linajes, relojes, tiempos) se saca con ganchos de SOLO LECTURA sobre funciones Python del motor
(_bq_arranque, _bq_muestra, _py_reglas_hijo, _py_reglas_fund, run_solapadas/ind_cb): cada gancho llama al original con los mismos
argumentos y no escribe en el estado, ni en BQ_OUT, ni consume azar del motor (el rng del fundador se RECREA aparte con la misma
semilla, solo para saber que entrada del banco tomo). Arnes: identidad_reactor.py (esc 90, n0 90, tope 3000, ganchos PUESTOS ==
corre_bloques.corre a la misma semilla, todas las claves menos 'seg').

Un proceso, sin Pool. T <= 200 000. Semillas NUEVAS 49701-49705 (grep del 1-oct: 4970x libre).
Uso:
  python sonda_reactor.py --humo                      # 49709, esc 90, T 20 000; escribe JSON
  python sonda_reactor.py --corre 300:90:49702,900:90:49703 [--T 200000] [--brazo BLOQ_V]
  python sonda_reactor.py --tabla
"""
import argparse, glob, hashlib, json, os, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
OPUSM = os.path.join(ORG, 'bloques', 'opusM')
if OPUSM not in sys.path: sys.path.insert(0, OPUSM)
import corre_bloques as CB   # noqa: E402

NS = CB.NS
DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(OPUSM, 'corre_bloques.py'): 'a090b82eae9f1ee3'}
T_MAX = 200000
TEL = {}     # telemetria de la corrida en curso (fuera del motor)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica():
    CB.verifica()
    for p, h in SHAS.items():
        if h16(p) != h: raise SystemExit(f'{os.path.basename(p)} cambio: {h16(p)} != {h}')


# ================================================================ ganchos de solo lectura
def _formas(st, MB, v):
    """Formas de regla de los vivos: corre_bloques.tipo(r) = sentido(pixel) comparador -> accion signo (sin umbral ni magnitud)."""
    RG = st['RG']; RN = st['RN']; cnt = {}; nrech = 0; larg = []
    for s in v:
        rs = [RG[s, r].tolist() for r in range(int(RN[s]))]
        larg.append(len(rs))
        for f in set(CB.tipo(r) for r in rs): cnt[f] = cnt.get(f, 0) + 1
        nrech += int(any(CB.rechazo(r) for r in rs))
    n = max(1, len(v))
    return dict(largo=(float(np.mean(larg)) if larg else None), largo_max=(int(max(larg)) if larg else 0),
                formas=len(cnt), formas30=sum(1 for c in cnt.values() if c / n >= 0.30),
                formas50=sum(1 for c in cnt.values() if c / n >= 0.50), frac_rechazo=(nrech / n if v else None),
                top=sorted(((round(c / n, 3), f) for f, c in cnt.items()), reverse=True)[:6])


def pon_ganchos(MB, seed):
    orig = dict(arr=MB._bq_arranque, mue=MB._bq_muestra, hij=MB._py_reglas_hijo, fun=MB._py_reglas_fund, run=MB.run_solapadas)
    TEL.clear()
    TEL.update(serie=[], EV={}, SRC={}, BRK=[], rows={}, n_hook_hijo=0, n_hook_fund=0, desinc=0, t_ini=None)
    OPS = ('n_campo', 'n_dup', 'n_del', 'n_ins', 'n_hgt')

    def arr(st, n):
        r = orig['arr'](st, n)
        TEL['st'] = st; TEL['t_ini'] = time.perf_counter()
        C = MB._CTX['BQC']
        TEL['BRK'] = ([('S', i, 0) for i in range(n)][-int(C['banco']):] if (C['on'] and C['banco']) else [])
        return r

    def mue(st, t):
        r = orig['mue'](st, t)
        v = MB._vivos(st); bi = st['bi']
        d = dict(t=int(t), reloj=time.perf_counter() - TEL['t_ini'], vivos=len(v),
                 linajes=len(set(int(bi[s, MB.I_LIN]) for s in v)), nacidos=sum(1 for s in v if not bi[s, MB.I_FUND]),
                 gen_media=(float(np.mean([bi[s, MB.I_GEN] for s in v])) if v else None),
                 gen_max=(int(max(bi[s, MB.I_GEN] for s in v)) if v else None), ranuras=int(bi.shape[0]))
        d.update(_formas(st, MB, v))
        TEL['serie'].append(d)
        return r

    def hij(lin, k, rp, rv):
        O = MB.BQ_OUT; a = sum(O[x] for x in OPS)
        ch = orig['hij'](lin, k, rp, rv)
        TEL['EV'][(int(lin), int(k))] = sum(O[x] for x in OPS) - a
        TEL['n_hook_hijo'] += 1
        C = MB._CTX['BQC']
        if C['banco']:
            TEL['BRK'].append(('P', int(lin), int(k)) if C['donante'] == 'padre' else ('S', int(lin), int(k)))
            if len(TEL['BRK']) > C['banco']: TEL['BRK'].pop(0)
        if len(TEL['BRK']) != len(MB._CTX['BR']): TEL['desinc'] += 1
        return ch

    def fun(lin, nac):
        O = MB.BQ_OUT; a = sum(O[x] for x in OPS); BR = MB._CTX['BR']; C = MB._CTX['BQC']
        src = None
        if BR:   # el MISMO sorteo que hara el original, con un rng APARTE (misma semilla): no consume azar del motor
            rr = np.random.default_rng([MB._CTX['seed'], int(lin), 7702, int(nac)])
            src = TEL['BRK'][int(rr.integers(len(BR)))] if len(TEL['BRK']) == len(BR) else None
        ch = orig['fun'](lin, nac)
        TEL['EV'][(int(lin), int(nac))] = sum(O[x] for x in OPS) - a
        TEL['SRC'][(int(lin), int(nac))] = src
        TEL['n_hook_fund'] += 1
        if C['donante'] == 'azar' and C['banco']:
            TEL['BRK'].append(('S', int(lin), int(nac)))
            if len(TEL['BRK']) > C['banco']: TEL['BRK'].pop(0)
        return ch

    def run(*a, **k):
        eco = k.get('eco')
        if eco is not None and eco.get('ind_cb') is not None:
            cb0 = eco['ind_cb']

            def cb(li, row, g):
                TEL['rows'][(int(li), int(row[0]))] = (int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]))
                return cb0(li, row, g)
            k = dict(k); k['eco'] = dict(eco, ind_cb=cb)
        t0 = time.perf_counter()
        r = orig['run'](*a, **k)
        TEL['seg_motor'] = time.perf_counter() - t0
        return r

    MB._bq_arranque = arr; MB._bq_muestra = mue; MB._py_reglas_hijo = hij; MB._py_reglas_fund = fun; MB.run_solapadas = run
    return orig


def quita_ganchos(MB, orig):
    MB._bq_arranque = orig['arr']; MB._bq_muestra = orig['mue']; MB._py_reglas_hijo = orig['hij']
    MB._py_reglas_fund = orig['fun']; MB.run_solapadas = orig['run']


# ================================================================ relojes (post hoc, con la genealogia completa)
def relojes(T, t_corte):
    """rows[(lin, k)] = (gen, padre_k, tn, tm, hijos, fund). Profundidad mutacional de un cuerpo = eventos de operadores (campo, dup,
    del, ins, hgt) sumados a lo largo de su ascendencia GENETICA (nacido: su padre; refundado: el padre del parto que dejo esa entrada
    en el banco). prof_cambios = cuantos pasos de esa ascendencia tuvieron >= 1 evento."""
    rows = TEL['rows']; EV = TEL['EV']; SRC = TEL['SRC']; memo = {}; falt = [0]

    def padre_gen(key):
        g, pk, tn, tm, hij, fund = rows[key]
        if not fund: return (key[0], pk)
        if key[1] == 0: return None
        src = SRC.get(key)
        if src is None: return None
        if src[0] == 'S': return (src[1], src[2])
        r2 = rows.get((src[1], src[2]))
        return None if r2 is None else (src[1], r2[1])

    def prof(key):
        pila = []; k = key
        while k is not None and k not in memo:
            if k not in rows: falt[0] += 1; memo[k] = (0, 0, 0); break
            pila.append(k); k = padre_gen(k)
        for k in reversed(pila):
            p = padre_gen(k); b = memo.get(p, (0, 0, 0)) if p is not None else (0, 0, 0)
            e = EV.get(k, 0)
            memo[k] = (b[0] + e, b[1] + int(e > 0), b[2] + 1)
        return memo[key]

    out = {}
    cortes = sorted(set([t for t in (T // 4, T // 2, 3 * T // 4, T) if t > 0]))
    for tt in cortes:
        viv = [k for k, r in rows.items() if r[2] < tt and (r[3] < 0 or r[3] >= tt)]
        if tt == T: viv = [k for k, r in rows.items() if r[3] < 0]
        pr = [prof(k) for k in viv]
        out[str(tt)] = dict(vivos=len(viv), prof_eventos=(float(np.mean([p[0] for p in pr])) if pr else None),
                            prof_eventos_max=(int(max(p[0] for p in pr)) if pr else None),
                            prof_cambios=(float(np.mean([p[1] for p in pr])) if pr else None),
                            prof_pasos=(float(np.mean([p[2] for p in pr])) if pr else None))
    ven = {}
    for a, b in ((0, T // 2), (T // 2, T)):
        nac = sum(1 for r in rows.values() if not r[5] and a < r[2] <= b)
        ref = sum(1 for r in rows.values() if r[5] and a < r[2] <= b)
        mue = sum(1 for r in rows.values() if a <= r[3] < b)
        ven[f'{a}-{b}'] = dict(nacimientos=nac, refundados=ref, muertes=mue)
    return dict(prof=out, ventanas=ven, sin_fila=falt[0], n_cuerpos=len(rows), n_ev=len(EV))


# ================================================================ una corrida
def corre_reactor(seed, brazo, T, esc, n0, carpeta, tope=None, ganchos=True):
    if T > T_MAX: raise SystemExit('T > 200 000 no se corre aqui (regla del creador)')
    if not 1 <= n0 <= CB.NS.ME_PY.ECO_NMAX: raise SystemExit(f'n0 fuera de [1, ECO_NMAX = {CB.NS.ME_PY.ECO_NMAX}]')
    if not 1 <= esc <= CB.NS.ME_PY.ECO_ESC_MAX: raise SystemExit(f'esc fuera de [1, ECO_ESC_MAX = {CB.NS.ME_PY.ECO_ESC_MAX}]')
    viejo = dict(NS.MUNDO)
    NS.MUNDO.update(esc=int(esc), n0=int(n0))
    if tope is not None: NS.MUNDO['tope'] = int(tope)
    mundo = dict(NS.MUNDO)
    MB = CB.usa_bloques()
    orig = pon_ganchos(MB, seed) if ganchos else None
    t0 = time.perf_counter()
    try:
        o = CB.corre(seed, brazo, T, carpeta)
    finally:
        seg = time.perf_counter() - t0
        if orig is not None: quita_ganchos(MB, orig)
        NS.MUNDO.clear(); NS.MUNDO.update(viejo)
    if not ganchos: return o, None
    nuc = json.load(open(os.path.join(carpeta, f'{brazo}_s{seed}.json'), encoding='utf-8'))
    tt = nuc.get('tam_total') or []; m = mundo['muestra']
    t_corte = o.get('t_corte')
    i_c = (T // 2) // m
    cp = float(np.sum(tt[:-1])) * m if len(tt) > 1 else 0.0          # cuerpos x pasos (tam_total se muestrea cada `muestra` pasos)
    ser = TEL['serie']
    seg_motor = TEL.get('seg_motor', seg)
    # tramos de 2000 pasos: segundos y cuerpos x pasos de cada uno (para separar costo por cuerpo de costo fijo del mundo)
    tramos = []
    for a, b in zip([dict(t=0, reloj=0.0, vivos=n0)] + ser[:-1], ser):
        tramos.append([b['t'], round(b['reloj'] - a['reloj'], 4), (a['vivos'] + b['vivos']) / 2])
    R = dict(seed=seed, brazo=brazo, T=T, esc=esc, n0=n0, mundo=mundo, t_corte=t_corte, seg=round(seg, 2), seg_motor=round(seg_motor, 2),
             s_por_100k=round(seg_motor * 100000 / T, 2), cuerpo_pasos=cp,
             us_cuerpo_paso=(round(seg_motor * 1e6 / cp, 3) if cp else None),
             vivos_media=(float(np.mean(tt)) if tt else None), vivos_min=(int(min(tt)) if tt else None),
             vivos_media_2a=(float(np.mean(tt[i_c:])) if tt else None), vivos_min_2a=(int(min(tt[i_c:])) if tt else None),
             vivos_max=nuc.get('max_vivos'), vivos_T=nuc.get('vivos_T'), linajes_T=nuc.get('linajes_T'), gen_max_T=nuc.get('gen_max_T'),
             persiste=o.get('persiste'), bloqueados=o.get('bloqueados'), aborto=o.get('aborto'), K=o.get('K'), K_nac=o.get('K_nac'),
             frac_rechazo=o.get('frac_rechazo'), n_nac=o.get('n_nac'), n_refund=o.get('n_refund'), mundo_out=o.get('mundo'),
             ops={k: v for k, v in (o.get('bloques') or {}).items() if k.startswith('n_')},
             tam_total=tt, serie=ser, tramos=tramos, ganchos=dict(hijo=TEL['n_hook_hijo'], fund=TEL['n_hook_fund'], desinc=TEL['desinc']),
             relojes=relojes(T, t_corte),
             shas={os.path.basename(p): h16(p) for p in list(CB.SHAS) + list(SHAS) + [os.path.abspath(__file__)]})
    fn = os.path.join(carpeta, f'R_{brazo}_esc{esc}_n{n0}_s{seed}.json')
    with open(fn + '.tmp', 'w', encoding='utf-8') as f: json.dump(R, f)
    os.replace(fn + '.tmp', fn)
    return o, R


def linea(R):
    s = {x['t']: x for x in R['serie']}; T = R['T']
    a = s.get(20000) or (R['serie'][0] if R['serie'] else {}); z = s.get(T) or (R['serie'][-1] if R['serie'] else {})
    pr = R['relojes']['prof']; pT = pr.get(str(T), {}); pM = pr.get(str(T // 2), {})
    v2 = R['relojes']['ventanas'].get(f'{T // 2}-{T}', {})
    rec = (v2.get('nacimientos', 0) / R['vivos_media_2a']) if R.get('vivos_media_2a') else None
    return (f"esc {R['esc']:5d} n0 {R['n0']:3d} s{R['seed']} {R['brazo']}: vivos media {R['vivos_media']:.1f} (2a mitad {R['vivos_media_2a']:.1f}, "
            f"min 2a {R['vivos_min_2a']}, max {R['vivos_max']}, T {R['vivos_T']}) · {R['us_cuerpo_paso']} us/cuerpo·paso · {R['s_por_100k']} s/100k · "
            f"linajes t20k {a.get('linajes')} -> T {R['linajes_T']} · largo {a.get('largo')} -> {z.get('largo')} · "
            f"formas {a.get('formas')} -> {z.get('formas')} (>=50 %: {a.get('formas50')} -> {z.get('formas50')}) · "
            f"prof eventos T/2 {pM.get('prof_eventos')} -> T {pT.get('prof_eventos')} · reemplazos/cuerpo 2a mitad "
            f"{None if rec is None else round(rec, 2)} · persiste {R['persiste']} · bloqueados {R['bloqueados']} · rechazo {R['frac_rechazo']} · "
            f"ganchos {R['ganchos']}")


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--corre', default=None); ap.add_argument('--T', type=int, default=200000)
    ap.add_argument('--brazo', default='BLOQ_V'); ap.add_argument('--carpeta', default='sonda'); ap.add_argument('--tabla', action='store_true')
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
    car = os.path.join(DATOS, a.carpeta)
    if a.tabla:
        for f in sorted(glob.glob(os.path.join(car, 'R_*.json'))): print(linea(json.load(open(f, encoding='utf-8'))))
        return
    verifica()
    if a.humo:
        o, R = corre_reactor(49709, 'BLOQ_V', 20000, 90, 90, os.path.join(DATOS, 'humo'))
        print(f"[{time.strftime('%H:%M:%S')}] HUMO " + linea(R), flush=True); return
    if not a.corre: raise SystemExit('usa --humo, --corre esc:n0:semilla[,...] o --tabla')
    for x in a.corre.split(','):
        esc, n0, seed = [int(z) for z in x.split(':')]
        if not 49701 <= seed <= 49709: raise SystemExit(f'semilla {seed} fuera de las declaradas (49701-49709)')
        o, R = corre_reactor(seed, a.brazo, a.T, esc, n0, car)
        print(f"[{time.strftime('%H:%M:%S')}] " + linea(R), flush=True)


if __name__ == '__main__':
    main()
