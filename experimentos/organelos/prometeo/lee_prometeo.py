# EXPLORATORIO, no es dato
"""lee_prometeo.py — que hizo PROMETEO (descriptivo; nada decide). Opus, 24-sep-2026. MISION: llegar a la AGI por este camino.
Uso: python lee_prometeo.py [--cintas N]
"""
import glob, json, os, sys
from collections import Counter
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); ORG = os.path.dirname(AQUI)
for d in (os.path.join(ORG, 'codigo'), AQUI): sys.path.insert(0, d)
import codigo_prometeo as CP
import gramatica_def as GD

DATOS = os.path.join(AQUI, 'datos')
SEN = ('sesgo', 'reserva', 'la_otra', 'ventana', 'edad', 'hijos')
DEC = ('boca', 'patas', 'parto')
BRAZOS = ('PROMETEO', 'PROMETEO_SIN_HGT', 'CODIGO_SIN_SOS', 'PERILLAS')
G0 = [1.0] * 18; LO = [1e-9] * 18; HI = [1e9] * 18; EN = [0] * 18   # solo para leer los cables (las perillas no importan aqui)


def organos(c):
    c = tuple(tuple(x) for x in c)
    W, h, gram = CP.organos(c, G0, LO, HI, EN)
    org = [s for s in gram if tuple(s[:4]) != (1, 3, 0, 0)]
    return W, h, org


def humano(c):
    W, h, org = organos(c); out = []
    if W is not None:
        for d in range(3):
            t = ' '.join(f"{W[d][q]:+.0f}·{SEN[q]}" for q in range(6) if W[d][q] != 0)
            if not t: continue
            if d == 2: out.append(f"PARTO: pare solo si {t} >= 0")
            elif d == 0: out.append(f"BOCA: empuja a morder con {t} (x0.5; >0 muerde mas, <0 se niega)")
            else: out.append(f"PATAS: {t} (x0.5; >0 camina aunque quiera quedarse, <0 se queda)")
    if h is not None: out.append(f"HGT: al nacer, con prob {h[0]} toma {h[1]} instrucciones del vecino")
    for s in org: out.append(f"ORGANO de transmision nuevo: {GD.CUANDO[s[0]]}/{GD.QUE[s[1]]}/{GD.QUIEN[s[2]]}/{GD.COMO[s[3]]}")
    return out


def firma_cables(c, solo_func=False):
    """Organos armados por la cinta. INERTE (marcado ~): PARTO con todos los pesos >= 0 (las 6 senales son >= 0: nunca veta) y ORG con
    cuando = nunca (el slot no se expresa). Todo lo demas PUEDE cambiar una decision (FUNCIONAL)."""
    W, h, org = organos(c); f = set()
    if W is not None:
        for d in range(3):
            inerte = d == 2 and all(W[2][q] >= 0 for q in range(6))
            for q in range(6):
                if W[d][q] != 0 and not (solo_func and inerte): f.add(f"{'~' if inerte else ''}{SEN[q]}->{DEC[d]}{'+' if W[d][q] > 0 else '-'}")
    if h is not None: f.add('HGT')
    for s in org:
        if solo_func and s[0] == 0: continue
        f.add(f"{'~' if s[0] == 0 else ''}ORG {GD.CUANDO[s[0]]}/{GD.QUE[s[1]]}/{GD.QUIEN[s[2]]}/{GD.COMO[s[3]]}")
    return f


def medidas(x):
    tl = x['tl']; V = x.get('ventanas_r0') or []; n = {v[0]: v[2] for v in V}; W = 2000
    solo = [n.get(a, 0) for a in range(tl['t_corte'], tl['T'] - tl['r0_margen'], W)]
    return dict(persiste=int(x.get('persiste') or 0), vivos=x.get('vivos_T'), nac_solo=int(sum(solo)), r0=(x.get('r0_final') or 0.0),
                n_nac=x.get('n_nac'), t_ext=x.get('t_ext'))


def main(n_cintas=3):
    for carpeta in sorted(glob.glob(os.path.join(DATOS, '*_*'))):
        if not os.path.isdir(carpeta): continue
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
        R = [x for x in R if not x.get('abortado')]
        if not R: continue
        print(f"\n==== {os.path.basename(carpeta)}  TL {R[0]['tl']}")
        by = {}
        for x in R: by.setdefault(x['brazo'], {})[x['seed']] = x
        print("| brazo | n | persiste | nac solo (suma) | nac solo por semilla | R0 final med | nac totales med | largo cinta (corte / final, media banco) |")
        for b in BRAZOS:
            d = by.get(b)
            if not d: continue
            ss = sorted(d); M = {s: medidas(d[s]) for s in ss}
            lc = []; lf = []
            for s in ss:
                pr = d[s].get('prometeo') or {}
                cc = (pr.get('cod_corte') or {}).get('banco') or []; bf = pr.get('banco_final') or []
                if cc: lc.append(np.mean([len(c) for c in cc]))
                if bf: lf.append(np.mean([len(c) for c in bf]))
            print(f"| {b} | {len(ss)} | {sum(M[s]['persiste'] for s in ss)}/{len(ss)} | {sum(M[s]['nac_solo'] for s in ss)} | {[M[s]['nac_solo'] for s in ss]} | "
                  f"{np.median([M[s]['r0'] for s in ss]):.2f} | {np.median([M[s]['n_nac'] or 0 for s in ss]):.0f} | "
                  f"{(f'{np.mean(lc):.1f}' if lc else '—')} / {(f'{np.mean(lf):.1f}' if lf else '—')} |")
        for b in ('PROMETEO', 'PROMETEO_SIN_HGT', 'CODIGO_SIN_SOS'):
            d = by.get(b)
            if not d: continue
            print(f"\n  -- {b}: organos del kit en el BANCO (fraccion de las cintas) en el corte y al final, por semilla")
            tot_c = Counter(); tot_f = Counter()
            for s in sorted(d):
                pr = d[s].get('prometeo') or {}
                cc = (pr.get('cod_corte') or {}).get('banco') or []; bf = pr.get('banco_final') or []
                Fc = Counter(); Ff = Counter()
                for c in cc: Fc.update(firma_cables(c))
                for c in bf: Ff.update(firma_cables(c))
                anyc = sum(1 for c in cc if firma_cables(c)) / max(1, len(cc)); anyf = sum(1 for c in bf if firma_cables(c)) / max(1, len(bf))
                func_c = sum(1 for c in cc if firma_cables(c, True)) / max(1, len(cc)); func_f = sum(1 for c in bf if firma_cables(c, True)) / max(1, len(bf))
                topc = {k: round(v / max(1, len(cc)), 2) for k, v in Fc.most_common(5)}
                topf = {k: round(v / max(1, len(bf)), 2) for k, v in Ff.most_common(5)}
                for k, v in Fc.items():
                    if v / max(1, len(cc)) > 0.5: tot_c[k] += 1
                for k, v in Ff.items():
                    if v / max(1, len(bf)) > 0.5: tot_f[k] += 1
                kit = pr.get('kit') or {}
                kv = pr.get('kit_ventanas') or []
                kvs = [(v[0], v[3], v[4], v[5]) for v in kv if v[1] and v[0] % 8000 == 0]
                print(f"   s{s}: con algun organo: corte {anyc:.2f} (funcional {func_c:.2f}) · final {anyf:.2f} (funcional {func_f:.2f}) · persiste {d[s].get('persiste')}")
                print(f"        top corte {topc}")
                print(f"        top final {topf}")
                print(f"        contadores {{boca si/no {kit.get('boca_si')}/{kit.get('boca_no')}, patas mueve/para {kit.get('pata_mueve')}/{kit.get('pata_para')}, "
                      f"vetos {kit.get('veto')}, hgt {kit.get('hgt')} {kit.get('hgt_ops')}}}; eventos HGT {pr.get('n_hgt_ev')}")
                print(f"        nacidos con (cable, hgt, org nuevo) por t: {kvs}")
            print(f"  -> organos en > 50 % del banco (n semillas): corte {dict(tot_c)} · final {dict(tot_f)}")
            # cintas en humano: las del banco final (o del corte) con mas organos, de las semillas que persisten primero
            if n_cintas and b != 'CODIGO_SIN_SOS':
                cand = []
                for s in sorted(d):
                    pr = d[s].get('prometeo') or {}
                    for fuente, L in (('final', pr.get('banco_final') or []), ('corte', (pr.get('cod_corte') or {}).get('banco') or [])):
                        cnt = Counter(tuple(tuple(i) for i in c) for c in L)
                        for c, v in cnt.most_common(3):
                            if firma_cables(c, True): cand.append((v / max(1, len(L)), s, fuente, c))
                cand.sort(key=lambda z: -z[0])
                for fr, s, fuente, c in cand[:n_cintas]:
                    print(f"\n   CINTA s{s} ({fuente}, {fr:.0%} del banco, largo {len(c)}):")
                    print('     ' + CP.texto(c))
                    for l in humano(c): print('     = ' + l)


if __name__ == '__main__':
    n = 3
    if '--cintas' in sys.argv: n = int(sys.argv[sys.argv.index('--cintas') + 1])
    main(n)


def clases(c):
    """(funcional sin HGT, inerte, HGT) de UNA cinta: 0/1 cada una."""
    f = firma_cables(c)
    fun = any(not k.startswith('~') and k != 'HGT' for k in f); ine = any(k.startswith('~') for k in f)
    return int(fun), int(ine), int('HGT' in f)


def tabla_organos():
    """Por mundo y brazo: fraccion media del BANCO (corte / final) con >= 1 organo FUNCIONAL (sin HGT), >= 1 INERTE (control neutro interno) y HGT;
    y semillas donde algun organo funcional concreto pasa del 50 % del banco."""
    print("\n| mundo | brazo | n | funcional corte/final | inerte corte/final | HGT corte/final | funcionales > 50 % del banco (semillas) |")
    print("|---|---|---|---|---|---|---|")
    for carpeta in sorted(glob.glob(os.path.join(DATOS, '*_*'))):
        if not os.path.isdir(carpeta): continue
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
        for b in ('PROMETEO', 'PROMETEO_SIN_HGT', 'CODIGO_SIN_SOS'):
            X = [x for x in R if x['brazo'] == b and not x.get('abortado')]
            if not X: continue
            acc = {'c': [], 'f': []}; mayo = Counter()
            for x in X:
                pr = x.get('prometeo') or {}
                for k, L in (('c', (pr.get('cod_corte') or {}).get('banco') or []), ('f', pr.get('banco_final') or [])):
                    if L: acc[k].append(np.mean([clases(c) for c in L], 0))
                    F = Counter()
                    for c in L: F.update(k2 for k2 in firma_cables(c, True) if k2 != 'HGT')
                    for k2, v in F.items():
                        if L and v / len(L) > 0.5: mayo[f"{k2}@{k}"] += 1
            m = {k: (np.mean(v, 0) if v else [np.nan] * 3) for k, v in acc.items()}
            print(f"| {os.path.basename(carpeta)} | {b} | {len(X)} | {m['c'][0]:.2f} / {m['f'][0]:.2f} | {m['c'][1]:.2f} / {m['f'][1]:.2f} | "
                  f"{m['c'][2]:.2f} / {m['f'][2]:.2f} | {dict(mayo) if mayo else '—'} |")


if __name__ == '__main__' and '--organos' in sys.argv:
    tabla_organos()


def tabla_largo(ts=(0, 8000, 16000, 24000, 32000, 40000, 44000, 50000, 54000)):
    """Largo medio de la cinta de los NACIDOS por ventana de 2000 pasos (media de las semillas con nacimientos en esa ventana)."""
    print("\n| mundo | brazo | " + " | ".join(f"t {t // 1000}k" for t in ts) + " |")
    print("|---|---|" + "---|" * len(ts))
    for carpeta in sorted(glob.glob(os.path.join(DATOS, '*_*'))):
        if not os.path.isdir(carpeta): continue
        R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
        for b in ('PROMETEO', 'PROMETEO_SIN_HGT', 'CODIGO_SIN_SOS'):
            X = [x for x in R if x['brazo'] == b and not x.get('abortado')]
            if not X: continue
            cel = []
            for t in ts:
                v = [w[2] for x in X for w in ((x.get('prometeo') or {}).get('kit_ventanas') or []) if w[0] == t and w[2] is not None]
                cel.append(f"{np.mean(v):.1f} ({len(v)})" if v else '—')
            print(f"| {os.path.basename(carpeta)} | {b} | " + " | ".join(cel) + " |")


if __name__ == '__main__' and '--largo' in sys.argv:
    tabla_largo()


def tabla_vivos_gr():
    """Organo de transmision de los VIVOS en T (todos los brazos, tambien PERILLAS, cuya gramatica muta): slots expresados distintos de filtra0
    presentes en > 50 % de los vivos."""
    print("\n| mundo | brazo | semilla | vivos T | slots expresados (no filtra0) en > 50 % de los vivos |")
    print("|---|---|---|---|---|")
    for carpeta in sorted(glob.glob(os.path.join(DATOS, '*_*'))):
        if not os.path.isdir(carpeta): continue
        for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json'))):
            x = json.load(open(p, encoding='utf-8'))
            V = x.get('vivos_gr') or []
            if not V: continue
            F = Counter()
            for v in V: F.update({f"{GD.CUANDO[s[0]]}/{GD.QUE[s[1]]}/{GD.QUIEN[s[2]]}/{GD.COMO[s[3]]}" for s in v[4] if s[0] != 0 and tuple(s[:4]) != (1, 3, 0, 0)})
            may = {k: round(c / len(V), 2) for k, c in F.items() if c / len(V) > 0.5}
            if may: print(f"| {os.path.basename(carpeta)} | {x['brazo']} | {x['seed']} | {len(V)} | {may} |")


if __name__ == '__main__' and '--vivos' in sys.argv:
    tabla_vivos_gr()
