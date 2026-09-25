# EXPLORATORIO, no es dato
"""corre_puenteo.py — UNA corrida del hibrido de puenteo (un proceso). La corrida ES la de corre_v143.tarea / juez.tarea:
pista.run(seed, 9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje (solo fisica).
Se agrega aparte la telemetria del hibrido (d['carro']['hib'] y las tablas de O1), que NO puntua.

Uso: python corre_puenteo.py --puente patas --seed 36001 [--T 100000]
Escribe datos/<puente>_s<seed>.json (ERR-54: el crudo se escribe antes de resumir nada).
"""
import argparse, json, os, sys, time, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))), 'bundle')   # JUACO/bundle
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
sys.path.insert(0, PISTA)
import pista as P
import juez as J

DATOS = os.path.join(AQUI, 'datos')
PUENTES = {
    'v143p': dict(),                                                     # control: HIB sin puentear (== V143)
    'patas': dict(patas=1),
    'boca_buena': dict(boca_buena=1),
    'boca_mala': dict(boca_mala=1),
    'boca': dict(boca_buena=1, boca_mala=1),
    'memoria': dict(memoria=1),
    'patas_boca': dict(patas=1, boca_buena=1, boca_mala=1),               # == O1 en la fisica (arnes (4)); aqui solo como control
    'patas_bmala': dict(patas=1, boca_mala=1),
    'patas_bbuena': dict(patas=1, boca_buena=1),
    'patas_memoria': dict(patas=1, memoria=1),
    'boca_memoria': dict(boca_buena=1, boca_mala=1, memoria=1),
    'todo': dict(patas=1, boca_buena=1, boca_mala=1, memoria=1),
}


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--puente', required=True, choices=sorted(PUENTES))
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--T', type=int, default=100000)
    a = ap.parse_args()
    os.makedirs(DATOS, exist_ok=True)
    fin = os.path.join(DATOS, f"{a.puente}_s{a.seed}.json")
    spec = importlib.util.spec_from_file_location('HIB', os.path.join(AQUI, 'carros', 'HIB.py')); HIB = importlib.util.module_from_spec(spec); spec.loader.exec_module(HIB)
    HIB.PUENTES = dict(patas=0, boca_buena=0, boca_mala=0, memoria=0); HIB.PUENTES.update(PUENTES[a.puente])
    t0 = time.time()
    r = P.run(a.seed, [(f"HIB_{a.puente}", HIB)] * 9, T=a.T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    L = [J.resumen_linaje(d, a.seed) for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    tel = [dict(hib=d['carro']['hib'], puentes=d['carro']['puentes'], o1_tabla=d['carro']['o1'].get('tabla'), o1_n=d['carro']['o1'].get('n'),
                v143=d['carro']['v143'].get('v143')) for d in r['linajes']]
    x = dict(seed=a.seed, puente=a.puente, puentes=dict(HIB.PUENTES), T=a.T, seg=round(time.time() - t0, 1), linajes=L, pista=r['pista'],
             R0_pista=round(sd / (sm + len(L)), 4), tel=tel)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    import statistics as st
    print(f"{a.puente} s{a.seed} T{a.T} {x['seg']}s · R0 real mediana {st.median([l['R0_real'] for l in L]):.3f} · "
          f"establecidos {sum(1 for l in L if l['fund_post10k'] == 0)}/9 · R0 real {[l['R0_real'] for l in L]}", flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
