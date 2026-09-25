"""sondeo_pool.py — H-6 del auditor (coordinador, 25-sep-2026): ¿el monkeypatch de corre_serie llega a los hijos de Pool en Windows (spawn)?
Corre la semilla de humo 30190 (quieto; PROMETEO y MUDO) con Pool(2) y la compara con el JSON del humo 3 (un proceso), sin campos de tiempo.
Uso (desde serie/): python sondeo_pool.py
"""
import json, os, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI); sys.dont_write_bytecode = True
import corre_serie as CS

HUMO = os.path.join(AQUI, 'datos', 'humo', 'humo_quieto_20260925_103239', 'quieto')
FUERA = {'seg', 'shas', 'ts', 'hora', 'fecha', 't_wall'}


def limpio(x):
    if isinstance(x, dict): return {k: limpio(v) for k, v in x.items() if k not in FUERA}
    if isinstance(x, list): return [limpio(v) for v in x]
    return x


if __name__ == '__main__':
    tmp = tempfile.mkdtemp(prefix='sondeo_prometeo_')
    from multiprocessing import Pool
    with Pool(2) as p:
        R = p.map(CS.trabajo, [('quieto', CS.SEM_HUMO, b, tmp, False) for b in ('PROMETEO', 'MUDO')])
    ok = True
    for x in R:
        ref = json.load(open(os.path.join(HUMO, f"{x['brazo']}_s{CS.SEM_HUMO}.json"), encoding='utf-8'))
        a, b = limpio(x), limpio(ref)
        dif = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
        print(f"{x['brazo']}: abortado={x.get('abortado')} · campos distintos del humo de un proceso: {dif}", flush=True)
        ok = ok and not dif and not x.get('abortado')
    print('SONDEO POOL', 'PASA' if ok else 'FALLA', '·', tmp)
