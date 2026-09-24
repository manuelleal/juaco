"""tabla_frank.py — junta los JSON de datos/ en una tabla por mundo y brazo (EXPLORATORIO, no es dato). Solo LEE datos/.
Uso: python experimentos/frankenstein/tabla_frank.py --mundo carrera --T 30000 --etiqueta a
"""
import argparse, glob, json, os, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 3) if xs else None


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--mundo', required=True); ap.add_argument('--T', type=int, required=True); ap.add_argument('--etiqueta', default='')
    a = ap.parse_args()
    R = {}
    pat = os.path.join(AQUI, 'datos', f"frank_{a.mundo}_*_T{a.T}{('_' + a.etiqueta) if a.etiqueta else ''}_2*.json")
    for p in sorted(glob.glob(pat)):
        for c in json.load(open(p, encoding='utf-8'))['corridas']:
            R.setdefault(c['brazo'], {})[c['seed']] = c
    orden = [b for b in ('TODO', 'OFF', 'V142', 'SIN_MAPA', 'SIN_CURIOSIDAD', 'SIN_MODELO', 'SIN_LENTA', 'SIN_HERENCIA', 'SIN_INTERRUPTOR',
                         'O1', 'FABRICA', 'APR') if b in R] + sorted(b for b in R if b not in ('TODO', 'OFF', 'V142', 'O1', 'FABRICA', 'APR') and not b.startswith('SIN_'))
    out = {}
    for b in orden:
        cs = [R[b][s] for s in sorted(R[b])]
        cz = {}; mord = {k: 0 for k in 'ABCD'}; org = {}
        for c in cs:
            for k, v in c['conducta']['causas'].items(): cz[k] = cz.get(k, 0) + v
            for k, v in c['conducta']['mord'].items(): mord[k] += v
            for k, v in c['conducta']['organos'].items(): org[k] = org.get(k, 0) + v
        tot = sum(cz.values()) or 1
        o = dict(semillas=sorted(R[b]), cz_frac={k: round(v / tot, 3) for k, v in cz.items()}, mord=mord, organos=org)
        if a.mundo == 'carrera':
            o.update(R0_real=[c['R0_real_med'] for c in cs], R0=[c['R0_med'] for c in cs], persisten=sum(c['persisten'] for c in cs),
                     cruzan_real=sum(c['cruzan_real'] for c in cs), n_lin=9 * len(cs), muertes=med([c['muertes_med'] for c in cs]),
                     vida=med([c['vida_med'] for c in cs]), malas=med([c['conducta']['frac_malas'] for c in cs]),
                     limp=med([c['limpiezas'] for c in cs]), sac=med([c['sac_frac_med'] for c in cs]),
                     sin_bueno=med([c['frac_sin_bueno_mundo'] for c in cs]),
                     comp_BD=med([round(c['comp_mundo']['B'] + c['comp_mundo']['D'], 3) for c in cs]))
            print(f"{b:16s} R0real {o['R0_real']} (med {med(o['R0_real'])}) R0 {o['R0']} persisten {o['persisten']}/{o['n_lin']} cruzan_real {o['cruzan_real']} "
                  f"muertes {o['muertes']} vida {o['vida']} malas {o['malas']} limp {o['limp']} sac {o['sac']} mundoBD {o['comp_BD']} "
                  f"causas {o['cz_frac']} mord {mord} org {org}")
        else:
            o.update(persisten=sum(c['persisten'] for c in cs), sin_ext=sum(c['sin_extincion'] for c in cs), n_lin=9 * len(cs),
                     persiste_carro=sum(bool(c['persiste_carro']) for c in cs), R0_coh=[c['R0_coh_med'] for c in cs],
                     fund=[c['ERR118']['R0_fundadores'] for c in cs], nac=[c['ERR118']['R0_nacidos'] for c in cs],
                     n_fund=sum(c['ERR118']['n_fundadores'] for c in cs), n_nac=sum(c['ERR118']['n_nacidos'] for c in cs),
                     cuerpos=[c['cuerpos_media'] for c in cs], gen=[c['gen_max'] for c in cs], malas=med([c['conducta']['frac_malas'] for c in cs]),
                     vida=med([c['vida_med'] for c in cs]))
            print(f"{b:16s} sin_ext {o['sin_ext']}/{o['n_lin']} persisten {o['persisten']} carro_persiste {o['persiste_carro']}/{len(cs)} R0coh {o['R0_coh']} "
                  f"R0 fund {o['fund']} (n {o['n_fund']}) nacidos {o['nac']} (n {o['n_nac']}) cuerpos {o['cuerpos']} gen {o['gen']} vida {o['vida']} "
                  f"malas {o['malas']} causas {o['cz_frac']} mord {mord} org {org}")
        out[b] = o
    if 'TODO' in R:
        print('\npareado contra TODO (R0 real de la corrida, por semilla): brazo  gana TODO / empata / pierde'
              if a.mundo == 'carrera' else '\npareado contra TODO (sin_extincion por semilla)')
        k = 'R0_real_med' if a.mundo == 'carrera' else 'sin_extincion'
        for b in orden:
            if b == 'TODO': continue
            ss = [s for s in R[b] if s in R['TODO']]
            g = sum(1 for s in ss if R['TODO'][s][k] > R[b][s][k]); e = sum(1 for s in ss if R['TODO'][s][k] == R[b][s][k])
            print(f"  {b:16s} {g}/{e}/{len(ss) - g - e}")
    return out


if __name__ == '__main__':
    main()
