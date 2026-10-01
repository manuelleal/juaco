"""sonda_nl.py — SONDA DE SOLO LECTURA (rafaga, no cuenta): por que la senal no anuncia el oasis nuevo? 1-oct-2026.
MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

Gancho sobre Carro._sn_lee de O1_TODO y O1_TODO_SEN (en memoria, sin tocar archivos): ANTES de llamar al original cuenta, con las mismas
condiciones del original y sin escribir estado, cada lectura: (periodo entre mudanzas, linaje, bin, destino) con destino en
  'siembra' (nl[b] == 0 y lo oido supera lo guardado) · 'nada' (nl[b] == 0 y no supera) · 'rech' (nl[b] != 0: rechazada por memoria vivida).
CONTROL DE NO-PERTURBACION: la fila de la corrida sondeada debe ser IGUAL a la del humo 1 guardado (misma semilla y brazo).
Tambien: nl al final (cuantos bins con nl > 0 por linaje) y si nl baja alguna vez (max de nl por bin visto en cada lectura: monotono?).
  python experimentos/organelos/escalera/mixto/sonda_nl.py [--seed 738611] [--brazos mix,sen9]
"""
import argparse, collections, glob, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_mixto as CM
RJ = CM.RJ
NB = 30


def sondea(seed, brazo, T, mundo):
    C = collections.Counter(); baja = [0]; prev = {}
    mods = {n: CM.carga(n) for n in set(CM.BRAZOS[brazo])}; origs = {}
    for n, m in mods.items():
        orig = m.Carro._sn_lee; origs[n] = orig

        def gancho(self, obs, _orig=orig, _m=m):
            piz = obs.get('pizarra') or ()
            p = prev.get(self.yo)
            if p is not None and (self.nl < p).any(): baja[0] += 1
            for e in piz:
                t, quien, c = e[0], e[1], e[2]
                if t <= self._sn_ult or quien == self.yo or len(c) < 3: continue
                b = int(c[0])
                if not 0 <= b < _m.LG_NB: continue
                if _m.SN_BARAJA: b = (b + _m.LG_NB // 2) % _m.LG_NB
                if self.nl[b] != 0: d = 'rech+' if self.lugar[b].sum() > _m.LG_MIN else 'rech0'   # rech+ = lo vivido aun dice que es bueno; rech0 = vivido y ya no vale
                else: d = 'siembra' if (_m.np.array([float(c[1]), float(c[2])]) * _m.SN_W > self.lugar[b]).any() else 'nada'
                C[(int(obs['t']) // mundo['mueve'], self.yo, b, d, quien)] += 1
            r = _orig(self, obs)
            prev[self.yo] = self.nl.copy()
            return r
        m.Carro._sn_lee = gancho
    try:
        x = CM.tarea(seed, CM.BRAZOS[brazo], T, mundo)
    finally:
        for n, m in mods.items(): m.Carro._sn_lee = origs[n]
    return x, C, baja[0]


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--seed', type=int, default=738611); ap.add_argument('--brazos', default='mix,sen9'); ap.add_argument('--T', type=int, default=100000)
    a = ap.parse_args(argv)
    if not CM.verifica(print): return 1
    mundo = dict(RJ.MUNDO_J); out = {}
    humo = sorted(glob.glob(os.path.join(AQUI, 'datos', 'humo_s738611-738612_T100000_m20000_*')))[0]
    for brazo in a.brazos.split(','):
        t0 = time.time()
        x, C, baja = sondea(a.seed, brazo, a.T, mundo)
        f = CM.fila(x, a.T, CM.BRAZOS[brazo])
        ref = os.path.join(humo, f"prueba_i{a.seed - 738611:02d}_{brazo}.json"); igual = None
        if os.path.exists(ref) and a.T == 100000:
            g = json.load(open(ref, encoding='utf-8')); N = lambda d: json.loads(json.dumps({k: v for k, v in d.items() if k not in ('seg', 'tipo', 'i', 'brazo', 'aborto')}, default=str))
            igual = N(f) == N(g)
        oi = x['oasis_info']; L = x['pista']['L'] if 'L' in x['pista'] else 360; ids = x['pista']['ids']
        mud = oi['mudanzas']; W = 36
        bins = [sorted({(((z + j) % L) * NB) // L for j in range(W)}) for _, z in mud]
        print(f"\n=== s{a.seed} {brazo} ({time.time()-t0:.0f}s) · SONDA NO PERTURBA (fila == humo 1 guardado): {igual} · nl bajo alguna vez: {baja} veces · lat lectores {f['mixto']['lat_lectores_med']}")
        print(f"  mudanzas (t, z0): {mud} · bins del oasis por periodo: {bins}")
        nlf = [t['lugar']['n'] for t in x['tel']]
        print(f"  nl al final: bins con nl > 0 por linaje {[sum(z > 0 for z in n) for n in nlf]} de {NB}")
        exp = ids[CM.EXPLORADOR] if brazo.startswith('mix') else None
        filas = []
        print("  per | lecturas | siembra | nada | rech+ | rech0 || AL OASIS NUEVO: lecturas | siembra | nada | rech+ | rech0 | % rech || al oasis VIEJO: lecturas | siembra | rech+ | rech0 || a otro bin: lecturas")
        for p in range(len(mud)):
            lec = lambda cond: {d: sum(v for (pp, yo, b, dd, q), v in C.items() if pp == p and dd == d and yo != exp and cond(b)) for d in ('siembra', 'nada', 'rech+', 'rech0')}
            tod = lec(lambda b: True); nue = lec(lambda b: b in bins[p]); vie = lec(lambda b: p > 0 and b in bins[p - 1] and b not in bins[p])
            otr = lec(lambda b: b not in bins[p] and not (p > 0 and b in bins[p - 1]))
            s = lambda d: sum(d.values()); rn = nue['rech+'] + nue['rech0']
            filas.append(dict(per=p, todas=tod, nuevo=nue, viejo=vie, otro=otr))
            print(f"  {p:3d} | {s(tod):8d} | {tod['siembra']:7d} | {tod['nada']:4d} | {tod['rech+']:5d} | {tod['rech0']:5d} || {s(nue):24d} | {nue['siembra']:7d} | {nue['nada']:4d} | {nue['rech+']:5d} | {nue['rech0']:5d} | "
                  f"{(100 * rn / s(nue) if s(nue) else float('nan')):6.1f} || {s(vie):24d} | {vie['siembra']:7d} | {vie['rech+']:5d} | {vie['rech0']:5d} || {s(otr):8d}")
        P = [f for f in filas if f['per'] > 0]; tn = sum(sum(f['nuevo'].values()) for f in P); rn = sum(f['nuevo']['rech+'] + f['nuevo']['rech0'] for f in P)
        r0 = sum(f['nuevo']['rech0'] for f in P); sn = sum(f['nuevo']['siembra'] for f in P)
        print(f"  TRAS MUDANZA (periodos 1+), lectores: lecturas hacia el oasis NUEVO {tn} · rechazadas por nl != 0: {rn} ({(100 * rn / tn if tn else float('nan')):.1f} %) "
              f"[de ellas con memoria propia ya sin valor (rech0) {r0}] · sembradas {sn}")
        out[brazo] = dict(igual_humo=igual, nl_baja=baja, mudanzas=mud, bins=bins, filas=filas, nl_final_bins=[sum(z > 0 for z in n) for n in nlf],
                          tras_mudanza=dict(lecturas_nuevo=tn, rechazadas=rn, rech0=r0, siembras=sn))
    d = os.path.join(AQUI, 'datos', 'sonda'); os.makedirs(d, exist_ok=True)
    rj = os.path.join(d, f"sonda_nl_s{a.seed}_T{a.T}_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(dict(seed=a.seed, T=a.T, mundo=mundo, sha_sonda=CM.h16(os.path.abspath(__file__)), sha_runner=CM.h16(CM.__file__), res=out), open(rj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"\n  JSON {rj}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
