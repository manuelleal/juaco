"""corre_frankenstein.py — SUELTA el Frankenstein en un mundo (EXPLORATORIO, no es dato). UN proceso, sin Pool.

MISION: llegar a la AGI por este camino.

Mundos:
  carrera  pista escalada de la carrera de escuderias (carrera_escuderias/pista.py, N = 9 carros del MISMO brazo, L = 360,
           36 objetos, fundador limpio = ENMIENDA 5). Resumen por linaje con juez.resumen_linaje (la misma letra: R0 preregistrado,
           R0 de nacimientos reales, fundadores tras t = 10000, persiste = 0 fundadores tras 10000 y >= 5 nacimientos) + conducta.
  convive  pista v2 con generaciones solapadas y QUIMIOSTATO (generaciones/pista2.py, solapadas=1, reposicion 'fija', r_rep 0.03),
           resumen con corre_convive.resumen_linaje + ERR-118: R0 de FUNDADORES contra R0 de NACIDOS (cohorte t <= T/2).
Brazos: TODO, OFF (== FABRICA), V142 (solo B-5), SIN_<ORGANO>, SOLO_<ORGANO>, y los carros de la carrera O1, FABRICA, APR.
Topes (reglas del equipo): <= 6 corridas (brazos x semillas) por invocacion, T <= 100000, semillas del Frankenstein
17001-17099 (carrera) / 17101-17199 (convive). Banderas desconocidas o abreviadas: abortan con codigo 2 ANTES de tocar disco.
Uso:  python experimentos/frankenstein/corre_frankenstein.py --humo
      python experimentos/frankenstein/corre_frankenstein.py --mundo carrera --brazos TODO,OFF --semillas 17001,17002,17003 --T 30000
"""
import argparse, json, os, statistics as st, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, 'datos')
RANGOS = dict(carrera=(17001, 17099), convive=(17101, 17199))
MAX_CORRIDAS = 6
T_MAX = 100000


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--mundo', default=None)
    ap.add_argument('--brazos', default=None)
    ap.add_argument('--semillas', default=None)
    ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--etiqueta', default='')
    a = ap.parse_args(argv)
    if a.humo:
        if any(x is not None for x in (a.mundo, a.brazos, a.semillas, a.T)): ap.error('--humo no admite otras banderas')
        a.mundo, a.brazos, a.semillas, a.T, a.etiqueta = 'carrera', 'TODO,OFF', '17001', 3000, 'humo'
    if a.mundo not in RANGOS: ap.error(f"--mundo carrera | convive (hay {a.mundo})")
    if not a.brazos or not a.semillas or a.T is None: ap.error('faltan --brazos, --semillas o --T')
    a.brazos = a.brazos.split(','); a.semillas = [int(s) for s in a.semillas.split(',')]
    lo, hi = RANGOS[a.mundo]
    if any(not lo <= s <= hi for s in a.semillas): ap.error(f"semillas fuera de {lo}-{hi} (mundo {a.mundo})")
    if len(a.brazos) * len(a.semillas) > MAX_CORRIDAS: ap.error(f"mas de {MAX_CORRIDAS} corridas por invocacion")
    if not 1000 <= a.T <= T_MAX: ap.error(f"T entre 1000 y {T_MAX}")
    return a


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 3) if xs else None


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


def conducta(ds):
    """lo que hace el bicho (sumado sobre los linajes de la corrida): que muerde, de que muere, organos."""
    mord = {k: 0 for k in 'ABCD'}; cz = {}
    fk = dict(pasos_mapa=0, rodeos_mapa=0, pruebas=0, vetos_peligro=0, lenta_usa=0, repasos=0, des_splits=0, paquetes=0)
    mm = {}; mp = {}
    for d in ds:
        for k, v in d['mord'].items(): mord[k] += sum(v) if isinstance(v, list) else v
        for k, v in d['_carrera']['causas'].items(): cz[k] = cz.get(k, 0) + v
        f = (d.get('carro') or {}).get('frank') or {}
        for k in fk: fk[k] += int(f.get(k, 0) or 0)
        for mo, dd in (f.get('mord_modo') or {}).items():
            for kk, v in dd.items(): mm.setdefault(mo, {}).setdefault(kk, 0); mm[mo][kk] += v
        for mo, v in (f.get('modo_pasos') or {}).items(): mp[mo] = mp.get(mo, 0) + v
    tot = sum(mord.values())
    return dict(mord=mord, frac_malas=(round((mord['B'] + mord['D']) / tot, 4) if tot else None), causas=cz,
                organos=fk, mord_por_modo=mm, pasos_por_modo=mp)


def corre_carrera(seed, brazo, T):
    import comun_frank as C, pista as P, juez as J
    t0 = time.time()
    r = P.run(seed, [C.carro(brazo)] * 9, T=T, fundador_limpio=1)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    lim = sum((x['diag'] or {}).get('limpiezas', 0) for x in L); malas = sum((x['diag'] or {}).get('mordidas_malas', 0) for x in L)
    res = dict(mundo='carrera', seed=seed, brazo=brazo, T=T, seg=round(time.time() - t0, 1),
               R0_med=med([x['R0'] for x in L]), R0_real_med=med([x['R0_real'] for x in L]),
               R0_real_eval_med=med([x['R0_real_eval'] for x in L]),
               cruzan_real=sum(x['cruza_real'] for x in L), persisten=sum(x['persiste'] for x in L),
               sin_fund_post10k=sum(1 for x in L if x['fund_post10k'] == 0),
               muertes_med=med([x['muertes'] for x in L]), nac_reales_med=med([x['nac_reales'] for x in L]),
               fundadores_med=med([x['fundadores'] for x in L]), vida_med=med([x['vida_med'] for x in L]),
               sac_frac_med=med([x['sac_frac'] for x in L]), limpiezas=lim, mordidas_malas_diag=malas,
               comp_mundo=r['pista']['comp_mundo'], frac_sin_bueno_mundo=r['pista']['frac_sin_bueno_mundo'],
               conducta=conducta(r['linajes']),
               linajes=[{k: v for k, v in x.items() if k not in ('telem', 'diag')} for x in L])
    return res


def corre_convive(seed, brazo, T):
    import comun_frank as C, pista2 as P2, corre_convive as JV
    t0 = time.time()
    r = P2.run(seed, [C.carro(brazo)] * 9, T=T, diag=0, solapadas=1, reposicion='fija')
    ps = r['pista']
    L = [JV.resumen_linaje(d, T, ps['muestra']) for d in r['linajes']]
    ind = [x for d in r['linajes'] for x in d['individuos']]   # [k, gen, padre, t_nace, t_muere, hijos, fundador, causa, vol]
    coh = [x for x in ind if x[3] <= T // 2]
    fu = [x[5] for x in coh if x[6]]; na = [x[5] for x in coh if not x[6]]
    fuc = [x[5] for x in coh if x[6] and x[4] >= 0]; nac = [x[5] for x in coh if not x[6] and x[4] >= 0]
    tam = ps.get('tam_total') or []
    i0 = 10000 // ps['muestra']
    res = dict(mundo='convive', seed=seed, brazo=brazo, T=T, seg=round(time.time() - t0, 1),
               persisten=sum(x['persiste'] for x in L), sin_extincion=sum(x['sin_extincion'] for x in L),
               persiste_carro=any(x['sin_extincion'] for x in L),
               R0_coh_med=med([x['R0_coh'] for x in L]), R0_compl_med=med([x['R0_compl'] for x in L]),
               ERR118=dict(R0_fundadores=media(fu), n_fundadores=len(fu), R0_nacidos=media(na), n_nacidos=len(na),
                           R0_fundadores_compl=media(fuc), R0_nacidos_compl=media(nac)),
               cuerpos_media=media(tam[i0:-1] if len(tam) > i0 + 1 else tam), cuerpos_max=(max(tam) if tam else None),
               fundadores=sum(x['fundadores'] for x in L), nacimientos=sum(x['nac'] for x in L),
               gen_max=max(x['gen_max'] for x in L), vida_med=med([x['vida_med'] for x in L]),
               conducta=conducta(r['linajes']), linajes=L)
    return res


def main(argv):
    a = parsea(argv)   # ANTES de importar nada pesado o tocar disco (ERR-115)
    sys.path.insert(0, AQUI)
    import comun_frank as C
    bv = C.brazos_validos()
    malos = [b for b in a.brazos if b not in bv]
    if malos: print(f"brazos desconocidos {malos}; validos {bv}", file=sys.stderr); sys.exit(2)
    shas = C.verifica_shas()
    if not all(ok for *_, ok in shas): print(f"SHAS: {[s for s in shas if not s[3]]}", file=sys.stderr); sys.exit(3)
    os.makedirs(DATOS, exist_ok=True)
    f = corre_carrera if a.mundo == 'carrera' else corre_convive
    R = []; t0 = time.time()
    for b in a.brazos:
        for s in a.semillas:
            x = f(s, b, a.T); R.append(x)
            if a.mundo == 'carrera':
                print(f"{b:16s} s{s} T{a.T}: R0 {x['R0_med']} R0real {x['R0_real_med']} cruzan_real {x['cruzan_real']}/9 persisten {x['persisten']}/9 "
                      f"sinfund>10k {x['sin_fund_post10k']}/9 muertes {x['muertes_med']} vida {x['vida_med']} malas {x['conducta']['frac_malas']} "
                      f"limp {x['limpiezas']} causas {x['conducta']['causas']} ({x['seg']} s)", flush=True)
            else:
                e = x['ERR118']
                print(f"{b:16s} s{s} T{a.T}: persisten {x['persisten']}/9 sin_ext {x['sin_extincion']}/9 R0coh {x['R0_coh_med']} "
                      f"fund {e['R0_fundadores']} (n {e['n_fundadores']}) nacidos {e['R0_nacidos']} (n {e['n_nacidos']}) cuerpos {x['cuerpos_media']} "
                      f"gen {x['gen_max']} malas {x['conducta']['frac_malas']} causas {x['conducta']['causas']} ({x['seg']} s)", flush=True)
    meta = dict(exploratorio='EXPLORATORIO -- no es dato', argv=argv, mundo=a.mundo, brazos=a.brazos, semillas=a.semillas, T=a.T,
                shas={k: h for k, h, _, _ in shas}, frank=C.h16(C.FRANK), corre=C.h16(os.path.abspath(__file__)),
                seg=round(time.time() - t0, 1), fecha=time.strftime('%Y-%m-%d %H:%M:%S'))
    nombre = f"frank_{a.mundo}_{'-'.join(a.brazos)}_s{a.semillas[0]}-{a.semillas[-1]}_T{a.T}{('_' + a.etiqueta) if a.etiqueta else ''}_{time.strftime('%Y%m%d_%H%M%S')}.json"
    p = os.path.join(DATOS, nombre)
    json.dump(dict(meta=meta, corridas=R), open(p, 'w', encoding='utf-8'), default=str)
    print(f"JSON: {p} ({C.h16(p)})")


if __name__ == '__main__':
    main(sys.argv[1:])
