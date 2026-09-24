"""diagnostico_frank.py — por que viven 200 pasos y que hace el mapa (EXPLORATORIO, no es dato). Un proceso, SOLO LECTURA:
envuelve metodos del Frankenstein con contadores (no cambia ninguna decision; el arnes (D) de abajo lo comprueba: misma fisica
con y sin la envoltura). Uso: python experimentos/frankenstein/diagnostico_frank.py [--brazo TODO] [--seed 17001] [--T 10000]
"""
import argparse, json, os, sys, time
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--brazo', default='TODO'); ap.add_argument('--seed', type=int, default=17001); ap.add_argument('--T', type=int, default=10000)
    a = ap.parse_args()
    if not 17001 <= a.seed <= 17099: raise SystemExit('semilla fuera de 17001-17099')
    import comun_frank as C, pista as P
    M = C.frank(); K = M.Carro
    ref = P.run(a.seed, [C.carro(a.brazo)] * 9, T=a.T, fundador_limpio=1)
    st = Counter(); prim = Counter(); edad_1a = []
    orig_mapa, orig_boca, orig_nace = K._fk_mapa, K._fk_boca, K._fk_nace

    def mapa(self, pos, objs, t, base):
        val = self._fk_vals()
        paredes = sum(1 for k in objs.values() if val[k] < -M.UMBRAL_PARED); metas = sum(1 for k in objs.values() if val[k] > M.UMBRAL_META)
        st['llamadas'] += 1; st['paredes'] += paredes; st['metas'] += metas; st['sin_meta'] += int(metas == 0)
        # la meta mas cercana (por distancia) esta tapada por una pared del lado corto?
        L = self.L; near = None
        for x, k in objs.items():
            if val[k] > M.UMBRAL_META:
                dr = (x - pos) % L; dl = (pos - x) % L; d = min(dr, dl)
                if near is None or d < near[0]: near = (d, dr <= dl, x)
        if near is not None and near[0] > 0:
            d, der, x = near
            tapa = any(val[k] < -M.UMBRAL_PARED and 0 < ((y - pos) % L if der else (pos - y) % L) < d for y, k in objs.items())
            st['meta_cercana_tapada'] += int(tapa)
        r = orig_mapa(self, pos, objs, t, base)
        st['elige_meta'] += int(self._fk_tgt is not None)
        return r

    def boca(self, obs, kk, mordio, u9, pb):
        r = orig_boca(self, obs, kk, mordio, u9, pb)
        e = obs['t'] - self._fk_t0
        if r and not self._fk_1a: self._fk_1a = True; prim[kk] += 1; edad_1a.append(e)
        return r

    def nace(self, info):
        orig_nace(self, info); self._fk_1a = False; self._fk_t0 = info['t']

    K._fk_mapa, K._fk_boca, K._fk_nace = mapa, boca, nace
    _init = K._fk_init

    def init(self, ctx):
        _init(self, ctx); self._fk_1a = True; self._fk_t0 = 0   # el primer fundador no cuenta como recien nacido
    K._fk_init = init
    t0 = time.time()
    r = P.run(a.seed, [C.carro(a.brazo)] * 9, T=a.T, fundador_limpio=1)
    K._fk_mapa, K._fk_boca, K._fk_nace, K._fk_init = orig_mapa, orig_boca, orig_nace, _init
    fis = lambda x: json.dumps([{k: v for k, v in d.items() if k != 'carro'} for d in x['linajes']], default=str, sort_keys=True)
    ident = fis(ref) == fis(r)
    vidas = [v for d in r['linajes'] for v in d['vidas_h1'][:-1]]
    cc = Counter(c for d in r['linajes'] for c in d['_carrera']['causa_cuerpo'])
    n = max(1, st['llamadas'])
    res = dict(brazo=a.brazo, seed=a.seed, T=a.T, identidad_fisica_con_envoltura=ident,
               vidas_n=len(vidas), vidas_eq200=sum(1 for v in vidas if v == 200), vidas_le200=sum(1 for v in vidas if v <= 200),
               vidas_hist={f"<={b}": sum(1 for v in vidas if v <= b) for b in (50, 100, 199, 200, 400, 600, 1000, 5000)},
               primera_mordida_recien_nacido=dict(prim), edad_1a_mediana=(sorted(edad_1a)[len(edad_1a) // 2] if edad_1a else None),
               mapa=dict(llamadas=st['llamadas'], paredes_media=round(st['paredes'] / n, 2), metas_media=round(st['metas'] / n, 2),
                         frac_sin_meta=round(st['sin_meta'] / n, 4), frac_elige_meta=round(st['elige_meta'] / n, 4),
                         frac_meta_cercana_tapada=round(st['meta_cercana_tapada'] / n, 4)),
               causas=dict(cc), seg=round(time.time() - t0, 1))
    print(json.dumps(res, indent=1))
    p = os.path.join(AQUI, 'datos', f"diagnostico_{a.brazo}_s{a.seed}_T{a.T}_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(res, open(p, 'w', encoding='utf-8'), indent=1); print('JSON:', p)


if __name__ == '__main__':
    main()
