"""analiza_serie.py — regimen (1-oct-2026, biotecnologo). Parte 1 del encargo: SIN correr nada, de los JSON de la serie de perillas
(datos/serie_i741201-741220_20261001_074651, SOLO LECTURA): dentro de sel, ¿GV o GW predicen mundo A+C, mordidas, fundadores, cruce?
¿En que pasaje aparece el mundo pelado: al subir GV o despues? Escribe regimen/analiza_serie_salida.json y imprime las tablas.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).
    python experimentos/organelos/escalera/regimen/analiza_serie.py [carpeta_serie]
"""
import glob, json, math, os, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SERIE = os.path.join(os.path.dirname(AQUI), 'perillas', 'datos', 'serie_i741201-741220_20261001_074651')


def rango(x):
    r = sorted(range(len(x)), key=lambda i: x[i]); out = [0.0] * len(x); i = 0
    while i < len(r):
        j = i
        while j + 1 < len(r) and x[r[j + 1]] == x[r[i]]: j += 1
        for k in range(i, j + 1): out[r[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def pearson(x, y):
    n = len(x); mx = sum(x) / n; my = sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float('nan')


def spearman(x, y): return pearson(rango(x), rango(y))


def med(x): return round(float(st.median(x)), 4) if x else None


def medidas(q):
    oz = q['oasis']; lg = q.get('lugar') or {}
    return dict(cruzan=q['cruzan'], R0=q['R0_med'], mundo_AC=q['mundo_AC'], mord_AC=q['mord_AC'], mord_BD=q['mord_BD'], mord_tot=q['mord_AC'] + q['mord_BD'],
                mord_AC_dentro=oz['mord_AC_dentro'], mord_AC_fuera=oz['mord_AC_fuera'], ratio_pasos=oz['ratio_pasos'], viajes=lg.get('viajes'),
                fund=sum(q['fund']), nac=sum(q['nac_reales']), muertes=sum(q['muertes']), vida=q['vida_med'],
                est=sum(int(z == 0) for z in q['fund_post10k']), partos=q.get('partos_tel'), bono_blancos=lg.get('bono_blancos'), max_med=lg.get('max_med'))


def main(carpeta=SERIE):
    R = {}; C = {}
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8')); R.setdefault(d['brazo'], {})[d['i']] = d
    for f in sorted(glob.glob(os.path.join(carpeta, 'cadena_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8')); C.setdefault(d['brazo'], {})[d['i']] = d
    I = sorted(R['sel']); out = {}
    # ---- (A) por brazo: medianas de las pruebas
    K = list(medidas(R['sel'][0]).keys())
    print("\n(A) PRUEBAS por brazo (mediana sobre 20 indices)")
    print(f"{'medida':16s}" + ''.join(f"{b:>10s}" for b in ('sel', 'neu', 'fab', 'o1')))
    out['pruebas_mediana'] = {}
    for k in K:
        fila = {b: med([medidas(R[b][i])[k] for i in I if medidas(R[b][i])[k] is not None]) for b in ('sel', 'neu', 'fab', 'o1')}
        out['pruebas_mediana'][k] = fila
        print(f"{k:16s}" + ''.join(f"{(fila[b] if fila[b] is not None else float('nan')):>10.4g}" for b in ('sel', 'neu', 'fab', 'o1')))
    # ---- (B) dentro de sel: GV y GW de la prueba contra las medidas (Spearman, n = 20)
    print("\n(B) DENTRO DE sel (n = 20 pruebas, genoma fijo mediano de su cadena): Spearman gen -> medida  [GV: rango de la serie]")
    gv = [R['sel'][i]['genoma']['GV'] for i in I]; gw = [R['sel'][i]['genoma']['GW'] for i in I]
    print(f"  GV en sel: min {min(gv):.3f} med {st.median(gv):.3f} max {max(gv):.3f} · GW: min {min(gw):.3f} med {st.median(gw):.3f} max {max(gw):.3f}")
    out['sel_spearman'] = {}
    for k in K:
        y = [medidas(R['sel'][i])[k] for i in I]
        if any(v is None for v in y): continue
        a = spearman(gv, y); b = spearman(gw, y); out['sel_spearman'][k] = dict(GV=round(a, 3), GW=round(b, 3))
        print(f"  {k:16s} rho(GV) {a:+.2f}   rho(GW) {b:+.2f}")
    # ---- (B2) lo mismo con las 4 pruebas de neu que SI viajaron (GV > 0.05): ¿el mundo pelado sigue a GV sin importar el brazo?
    print("\n(B2) TODAS las pruebas con genoma propio (sel + neu, n = 40): Spearman GV -> medida (neu con GV ~0 son O1)")
    gv2 = gv + [R['neu'][i]['genoma']['GV'] for i in I]; gw2 = gw + [R['neu'][i]['genoma']['GW'] for i in I]
    out['selneu_spearman'] = {}
    for k in ('mundo_AC', 'mord_AC', 'mord_BD', 'fund', 'nac', 'cruzan', 'ratio_pasos', 'viajes'):
        y = [medidas(R['sel'][i])[k] for i in I] + [medidas(R['neu'][i])[k] for i in I]
        a = spearman(gv2, y); out['selneu_spearman'][k] = round(a, 3); print(f"  {k:16s} rho(GV) {a:+.2f}")
    # ---- (B3) tabla de las 20 pruebas sel ordenadas por GV
    print("\n(B3) las 20 pruebas sel ordenadas por GV")
    print(f"{'i':>3s}{'GV':>7s}{'GW':>7s}{'cruz':>5s}{'R0':>7s}{'AC':>7s}{'mAC':>6s}{'mBD':>6s}{'mACin':>6s}{'mACout':>7s}{'ratio':>7s}{'viajes':>8s}{'fund':>5s}{'nac':>5s}{'est':>4s}{'maxmed':>7s}")
    for i in sorted(I, key=lambda i: R['sel'][i]['genoma']['GV']):
        m = medidas(R['sel'][i]); g = R['sel'][i]['genoma']
        print(f"{i:3d}{g['GV']:7.3f}{g['GW']:7.3f}{m['cruzan']:5d}{m['R0']:7.3f}{m['mundo_AC']:7.2f}{m['mord_AC']:6d}{m['mord_BD']:6d}{m['mord_AC_dentro']:6d}{m['mord_AC_fuera']:7d}{m['ratio_pasos']:7.2f}{m['viajes']:8d}{m['fund']:5d}{m['nac']:5d}{m['est']:4d}{m['max_med']:7.3f}")
    # ---- (B4) neu con viajes > 0 (los 4-5 genomas neutros que salieron con GV > 0.05)
    print("\n(B4) pruebas neu con GV > 0.05 (deriva que salio con el viaje medio prendido)")
    for i in I:
        g = R['neu'][i]['genoma']
        if g['GV'] > 0.05:
            m = medidas(R['neu'][i]); print(f"  i{i:02d} GV {g['GV']:.3f} GW {g['GW']:.3f} cruzan {m['cruzan']} AC {m['mundo_AC']:.2f} mAC {m['mord_AC']} mBD {m['mord_BD']} ratio {m['ratio_pasos']:.2f} viajes {m['viajes']} fund {m['fund']} nac {m['nac']}")
    # ---- (C) pasajes de sel: ¿cuando aparece el mundo pelado?
    print("\n(C) CADENAS sel por pasaje (mediana de 20): GV de la siembra, mundo AC, mordidas, fundadores, ratio, viajes, cruzan  (y neu al lado)")
    out['pasajes'] = {}
    for b in ('sel', 'neu'):
        out['pasajes'][b] = []
        for p in range(5):
            qs = [C[b][i]['pasajes'][p] for i in I]
            fila = dict(GV=med([(q['genes_siembra'] or {}).get('GV') for q in qs]), GW=med([(q['genes_siembra'] or {}).get('GW') for q in qs]),
                        mundo_AC=med([q['mundo_AC'] for q in qs]), mord_AC=med([q['mord_AC'] for q in qs]), mord_BD=med([q['mord_BD'] for q in qs]),
                        fund=med([sum(q['fund']) for q in qs]), nac=med([sum(q['nac_reales']) for q in qs]), ratio=med([q['oasis']['ratio_pasos'] for q in qs]),
                        viajes=med([(q.get('lugar') or {}).get('viajes') for q in qs]), cruzan=med([q['cruzan'] for q in qs]), est=med([q['moneda']['n_est'] for q in qs]),
                        gen_vivos_GV=med([(q.get('genes_vivos_fin') or {}).get('GV') for q in qs]))
            out['pasajes'][b].append(fila)
            print(f"  {b} p{p}: " + ' '.join(f"{k} {v}" for k, v in fila.items()))
    # ---- (C2) pasaje 0 de sel: GV de la siembra vs mundo AC de ESE pasaje (el gen sube DURANTE el pasaje 0)
    print("\n(C2) sel pasaje 0 (arranca en 0,0; el gen sube dentro del pasaje): GV siembra final vs medidas del pasaje, n = 20")
    q0 = [C['sel'][i]['pasajes'][0] for i in I]; g0 = [(q['genes_siembra'] or {}).get('GV') or 0 for q in q0]
    for k, f in (('mundo_AC', lambda q: q['mundo_AC']), ('mord_AC', lambda q: q['mord_AC']), ('fund', lambda q: sum(q['fund'])), ('viajes', lambda q: q['lugar']['viajes']), ('ratio', lambda q: q['oasis']['ratio_pasos']), ('cruzan', lambda q: q['cruzan'])):
        y = [f(q) for q in q0]; print(f"  {k:10s} rho(GV siembra p0) {spearman(g0, y):+.2f}  · mediana {med(y)}")
    # ---- (C3) la correlacion dentro de cada pasaje de sel (GV siembra -> mundo AC) y entre pasajes
    print("\n(C3) por pasaje de sel: rho(GV siembra, mundo AC), rho(GV siembra, viajes), rho(viajes, mundo AC), rho(ratio, mundo AC)")
    for p in range(5):
        qs = [C['sel'][i]['pasajes'][p] for i in I]; g = [(q['genes_siembra'] or {}).get('GV') or 0 for q in qs]
        ac = [q['mundo_AC'] for q in qs]; vj = [q['lugar']['viajes'] for q in qs]; rt = [q['oasis']['ratio_pasos'] for q in qs]
        print(f"  p{p}: GV-AC {spearman(g, ac):+.2f} · GV-viajes {spearman(g, vj):+.2f} · viajes-AC {spearman(vj, ac):+.2f} · ratio-AC {spearman(rt, ac):+.2f}")
    # ---- (D) pareado sel vs fab en la MISMA semilla de prueba
    print("\n(D) pareado sel - fab por indice (misma semilla de prueba):")
    out['par_sel_fab'] = {}
    for k in ('cruzan', 'R0', 'mundo_AC', 'mord_AC', 'mord_BD', 'mord_AC_dentro', 'mord_AC_fuera', 'ratio_pasos', 'viajes', 'fund', 'nac', 'est', 'vida'):
        d = [medidas(R['sel'][i])[k] - medidas(R['fab'][i])[k] for i in I]
        out['par_sel_fab'][k] = dict(med_dif=med(d), sel_mayor=sum(z > 0 for z in d), fab_mayor=sum(z < 0 for z in d))
        print(f"  {k:16s} mediana(sel - fab) {med(d):>10}  sel> {sum(z > 0 for z in d):2d}  fab> {sum(z < 0 for z in d):2d}")
    json.dump(out, open(os.path.join(AQUI, 'analiza_serie_salida.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
