"""diagnostico.py — DIAGNOSTICO (solo lectura, cero CPU de pista) sobre los JSON ya corridos de TERMO (serie 39101-39120, replica
39121-39140). EXPLORATORIO, no es dato.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles
y replicas).

Pregunta: en las semillas donde TERMO NO tiene mayoria de linajes que cruzan y O1 SI, que pasa? Linaje por linaje: F (fundadores),
F antes/despues de t 10 000, D (muertes), R0 real = (D - F)/(D + 1), vida del primer fundador, cuantos fundadores antes del primer
parto real, causas de muerte, mordidas.

    python experimentos/organelos/dinamita/diagnostico.py [--detalle]
"""
import json, os, sys, glob, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
TD = os.path.join(os.path.dirname(AQUI), 'termo', 'datos')
CARP = sorted(d for d in glob.glob(os.path.join(TD, 'termo_s391*_T100000_*')) if os.path.isdir(d))


def med(x):
    x = [v for v in x if v is not None]
    return round(st.median(x), 3) if x else None


def lin_info(l):
    t = l['telem']; org = t['origen']; v = t['vidas']; dpv = t['desc_por_vida']; cc = t['causa_cuerpo']
    # fundadores: origen 0 (el indice 0 es el fundador de t = 0)
    tf = t['t_fund']
    # tiempo hasta el primer nacimiento real (primer cuerpo con origen 1)
    t_acum = 0; t_first = None
    for i in range(len(v)):
        if org[i] == 1 and t_first is None: t_first = t_acum
        t_acum += v[i]
    # fundadores antes del primer nacido real
    f_antes = 0
    for i in range(len(org)):
        if org[i] == 1: break
        if i > 0: f_antes += 1
    # fundadores despues del primer nacimiento real (el linaje se cayo y volvio a empezar)
    f_despues = (len(org) - 1 - sum(org)) - f_antes if t_first is not None else 0
    fvid = [v[i] for i in range(len(v)) if org[i] == 0]
    fcau = {}
    for i in range(min(len(cc), len(org))):
        if org[i] == 0: fcau[cc[i]] = fcau.get(cc[i], 0) + 1
    hij = [i for i in range(len(v)) if org[i] == 1]
    hvid = [v[i] for i in hij]; hdesc = [dpv[i] for i in hij]
    hcau = {}
    for i in hij:
        if i < len(cc): hcau[cc[i]] = hcau.get(cc[i], 0) + 1
    return dict(F=l['fundadores'], Fpost=l['fund_post10k'], D=l['muertes'], R0=l['R0_real'], cruza=l['cruza_real'], ev=l['evaluable'],
                t_first=t_first, f_antes=f_antes, f_despues=f_despues, fvid0=v[0], fvid_med=med(fvid), fcau=fcau,
                hvid_med=med(hvid), hdesc_med=med(hdesc), hn=len(hij), hsin=(round(sum(1 for x in hdesc if x == 0) / len(hdesc), 3) if hdesc else None),
                hcau=hcau, mord=l['mord'], cola=l['cola_final'], tf=tf[:12])


def carga(carpeta, brazo):
    out = {}
    for f in glob.glob(os.path.join(carpeta, f'{brazo}_s*.json')):
        d = json.load(open(f, encoding='utf-8'))
        out[d['seed']] = [lin_info(l) for l in d['linajes']]
    return out


def clase(x):
    """clasifica un linaje que no cruza."""
    if x['cruza']: return 'CRUZA'
    if x['Fpost'] > 0:
        return 'NO_ESTAB_nunca' if x['t_first'] is None else ('NO_ESTAB_tardio' if x['f_despues'] == 0 else 'NO_ESTAB_cae')
    if not x['ev']: return 'casi_inmortal'
    return 'ESTAB_bajo'   # establecido (0 fund tras 10k) pero R0 real < 0.90


def main():
    det = '--detalle' in sys.argv
    tot = {}
    for carpeta in CARP:
        nom = os.path.basename(carpeta)
        print(f"\n######## {nom}")
        T = carga(carpeta, 'termo'); O = carga(carpeta, 'o1'); V = carga(carpeta, 'v143')
        for s in sorted(T):
            mt = sum(x['cruza'] for x in T[s]); mo = sum(x['cruza'] for x in O[s]); mv = sum(x['cruza'] for x in V[s])
            marca = '  <== TERMO no, O1 si' if (mt * 2 <= 9 and mo * 2 > 9) else ''
            print(f"  s{s}: cruzan termo {mt}/9 · o1 {mo}/9 · v143 {mv}/9{marca}")
            for b, D in (('termo', T), ('o1', O), ('v143', V)):
                for x in D[s]:
                    c = clase(x); k = (b, 'mala' if marca else 'buena')
                    tot.setdefault(k, {}).setdefault(c, []).append(x)
                    tot.setdefault((b, 'todas'), {}).setdefault(c, []).append(x)
            if marca and det:
                for b, D in (('termo', T), ('o1', O)):
                    for i, x in enumerate(D[s]):
                        print(f"     {b:5s}#{i} {clase(x):16s} F {x['F']:3d} (post10k {x['Fpost']:3d}, antes del 1er nacido {x['f_antes']:3d}) D {x['D']:3d} "
                              f"R0 {x['R0']:.3f} · t 1er nacido {x['t_first']} · fund vida med {x['fvid_med']} causas {x['fcau']} · "
                              f"hijos n {x['hn']} vida {x['hvid_med']} desc {x['hdesc_med']} sin {x['hsin']} · mord {x['mord']} · t_fund {x['tf'][:6]}")
    print("\n================ RESUMEN POR CLASE (linajes)")
    for k in sorted(tot):
        print(f"\n  {k[0]:6s} semillas {k[1]:6s}:")
        for c, xs in sorted(tot[k].items()):
            fc = {}
            for x in xs:
                for a, n in x['fcau'].items(): fc[a] = fc.get(a, 0) + n
            print(f"    {c:16s} n {len(xs):3d} · F med {med([x['F'] for x in xs])} · f_antes med {med([x['f_antes'] for x in xs])} · D med {med([x['D'] for x in xs])} "
                  f"· R0 med {med([x['R0'] for x in xs])} · t1er nacido med {med([x['t_first'] for x in xs])} · fund vida med {med([x['fvid_med'] for x in xs])} "
                  f"· hijos vida med {med([x['hvid_med'] for x in xs])} desc med {med([x['hdesc_med'] for x in xs])} sin hijos {med([x['hsin'] for x in xs])} "
                  f"· mord B+D med {med([x['mord']['B'] + x['mord']['D'] for x in xs])} A+C {med([x['mord']['A'] + x['mord']['C'] for x in xs])} · causas fund {fc}")


if __name__ == '__main__':
    main()
