"""analiza_potencia_v143.py -- PROBABILIDAD DE PASAR cada puerta del examen v4, calculada ANTES de la serie con datos REALES
ya existentes (no simula ni un paso). Regla 15 de EQUIPO.md / §3 de CRITERIO_TRONCO_v4: toda puerta declara su nulo, su margen
y su n con el calculo. Aqui se calcula, para v14.3, lo que la letra le hara, y se escribe en datos/humo/ (ERR-42).

Por que basta el TRONCO para casi todo: v14.3 == v14.2 bit a bit en todos los mundos de T-A..T-F (P.P = 3; lo verifica
identidad_v143ex.py), asi que P(v14.3 pasa T-B, T-C i, T-D, T-E) = P(el TRONCO pasa esas puertas ABSOLUTAS en 20 semillas
nuevas), y T-A, T-C (ii), T-F son 1 por construccion (d = 0) salvo que TRONCO_B no pase (serie ilegible).

Fuentes (sha fijado; si cambian, se para):
  T-B      regresion_generaliza_organismo_v14_20260918_054926.json (101-120) y _v14_e015c10_20260918_054603.json (121-140):
           v14.1 == v14.2 == v14.3 en el mundo de regla (B-5 T2 40/40 identicas; N inerte con 20 patrones de masa 3)
  T-C i/T-E examen_v142_20260921_153019.json (2001-2020) y examen_v14_20260921_124347.json (121-140) (+101-120 del log)
  legible  critv4_20260922_132544_crudo_{TA,TCii}.json y critv4_rep_20260922_135746_crudo_{TA,TCii}.json (OFF + TRONCO_B)
  T-D      codigo_alias9_20260918_085958.json y codigo_replica_alias9_20260918_091133.json (B-5, 18 ALIAS + 18 LIMPIAS)
  T-G      experimentos/subida_n7/datos/n7_serie_s7701-7720_* y n7_serie_s7721-7740_* (40 semillas, T142 / N / NC3C)

    python experimentos/tronco_v14_3_examen/analiza_potencia_v143.py
"""
import hashlib, json, math, os, sys, time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
D = os.path.join(RAIZ, 'datos')
N7D = os.path.join(RAIZ, 'experimentos', 'subida_n7', 'datos')
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'subida_n7'), os.path.join(RAIZ, 'experimentos', 'criterio_v4'),
                os.path.join(RAIZ, 'experimentos', 'criterio_v3')]

FUENTES = {
    os.path.join(D, 'regresion_generaliza_organismo_v14_20260918_054926.json'): '6452fdf50352607e',
    os.path.join(D, 'regresion_generaliza_organismo_v14_e015c10_20260918_054603.json'): None,
    os.path.join(D, 'examen_v142_20260921_153019.json'): None,
    os.path.join(D, 'examen_v14_20260921_124347.json'): None,
    os.path.join(D, 'critv4_20260922_132544_crudo_TA.json'): None,
    os.path.join(D, 'critv4_20260922_132544_crudo_TCii.json'): None,
    os.path.join(D, 'critv4_rep_20260922_135746_crudo_TA.json'): None,
    os.path.join(D, 'critv4_rep_20260922_135746_crudo_TCii.json'): None,
    os.path.join(D, 'codigo_alias9_20260918_085958.json'): None,
    os.path.join(D, 'codigo_replica_alias9_20260918_091133.json'): None,
    os.path.join(N7D, 'n7_serie_s7701-7720_T100000_20260923_174554.json'): '2de815c50f5d10e9',
    os.path.join(N7D, 'n7_serie_s7721-7740_T100000_20260923_180727.json'): '19c9e3d34bb0198f',
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def carga(p):
    s = h16(p)
    if FUENTES.get(p) and s != FUENTES[p]:
        raise SystemExit(f'*** {os.path.basename(p)} sha {s} != {FUENTES[p]}')
    return json.load(open(p, encoding='utf-8'))


def binom_ge(n, k, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def cp_sup(fallos, n, a=0.05):
    """Cota superior (una cola, 95 %) de la tasa de fallo por semilla con `fallos` de `n` (Clopper-Pearson)."""
    if fallos == n:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if sum(math.comb(n, i) * m ** i * (1 - m) ** (n - i) for i in range(0, fallos + 1)) > a:
            lo = m
        else:
            hi = m
    return round(hi, 4)


if __name__ == '__main__':
    t0 = time.time()
    import umbrales_examen_v143 as U
    SH = {os.path.relpath(p, RAIZ).replace(os.sep, '/'): h16(p) for p in FUENTES}
    OUT = dict(fuentes=SH, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'))
    g = np.random.default_rng(20260923)

    # ------------------------------------------------------------ T-B (el tronco en 40 semillas reales)
    filas = []
    for f in list(FUENTES)[:2]:
        j = carga(f); C = j['corridas']; S = j['meta']['semillas']
        px = {r['seed']: r for r in C if r['regla'] == 'px0'}; az = {r['seed']: r for r in C if r['regla'] == 'azar'}
        filas += [(px[s]['acc'], px[s]['ba'], px[s]['cobertura'], az[s]['acc'], az[s]['ba']) for s in S]
    F = np.array([[x if x is not None else np.nan for x in r] for r in filas], float)
    B = 20000; n = 20; cnt = dict(G1=0, G2=0, azar1=0, azar2=0, K=0, todo=0); m2 = []; m1 = []
    BANDA_PROPUESTA = (0.31, 0.60)   # SOLO para el ERR candidato de PREREGISTRO §7 (b); la letra NO se toca aqui
    prop = 0
    for _ in range(B):
        R = F[g.integers(0, len(F), n)]
        c = dict(G1=np.median(R[:, 0]) >= U.NUM['TB_g1'], G2=np.nanmedian(R[:, 1]) >= U.NUM['TB_g2'],
                 azar1=U.NUM['TB_azar'][0] <= np.median(R[:, 3]) <= U.NUM['TB_azar'][1],
                 azar2=U.NUM['TB_azar2'][0] <= np.nanmedian(R[:, 4]) <= U.NUM['TB_azar2'][1],
                 K=(R[:, 2] >= U.NUM['TB_cob']).sum() == n)
        for k, v in c.items():
            cnt[k] += bool(v)
        cnt['todo'] += bool(all(c.values()))
        prop += bool(c['G1'] and c['G2'] and c['azar1'] and c['K'] and BANDA_PROPUESTA[0] <= np.nanmedian(R[:, 4]) <= BANDA_PROPUESTA[1])
        m1.append(np.median(R[:, 3])); m2.append(np.nanmedian(R[:, 4]))
    PTB = {k: round(v / B, 3) for k, v in cnt.items()}
    PTB_prop = round(prop / B, 3)
    q = [0.005, 0.01, 0.025, 0.05, 0.5, 0.95, 0.975, 0.99, 0.995]
    OUT['T-B'] = dict(n_semillas_reales=len(F), P_por_clausula=PTB,
                      mediana_real_azar_G2=round(float(np.nanmedian(F[:, 4])), 4), mediana_real_azar_G1=round(float(np.median(F[:, 3])), 4),
                      series_reales_azar_G2={'101-120': 0.437, '121-140': 0.434},
                      cuantiles_mediana_azar_G2_n20={str(x): round(float(np.quantile(m2, x)), 4) for x in q},
                      cuantiles_mediana_azar_G1_n20={str(x): round(float(np.quantile(m1, x)), 4) for x in q},
                      azar_G2_por_semilla=sorted(round(float(x), 3) for x in F[:, 4]),
                      NO_ES_LA_LETRA_propuesta_ERR=dict(banda_azar_G2=BANDA_PROPUESTA, P_TB_todo=PTB_prop))
    print(f"T-B (tronco == v14.3 en el mundo de regla), bootstrap de {len(F)} semillas reales, n = 20, B = {B}: {PTB}")
    print(f"    (NO es la letra) con la banda de azar G2 propuesta {BANDA_PROPUESTA} para el ERR candidato: T-B entera {PTB_prop}")
    print(f"    mediana real de azar G2 = {OUT['T-B']['mediana_real_azar_G2']} (banda de la letra {list(U.NUM['TB_azar2'])}); "
          f"cuantiles de la mediana a n = 20: {OUT['T-B']['cuantiles_mediana_azar_G2_n20']}")

    # ------------------------------------------------------------ T-C (i) y clausulas absolutas de T-E (el tronco)
    tasa = lambda r, k, i: 100 * r['mord'][k][i] / max(r['vis'][k][i], 1)
    e2, e2i = [], []
    for f in list(FUENTES)[2:4]:
        C = carga(f)['corridas']
        e2 += [r['mord']['B'][3] for r in C if r['etapa'] == 'E2']
        e2i += [tasa(r, 'A', 3) >= .8 * tasa(r, 'A', 1) for r in C if r['etapa'] == 'E2I']
    e2 = np.array(e2); nf = int((e2 < U.NUM['TC_i_come']).sum()) + 0   # + 101-120 del log: 20/20
    nt = len(e2) + 20
    p_up = cp_sup(nf, nt)
    OUT['T-C_i'] = dict(semillas=nt, fallos=nf, minimo=int(e2.min()), p_fallo_cota95=p_up,
                        P_pasa_con_la_cota=round(1 - binom_ge(20, 20 - U.NUM['puerta_E'] + 1, p_up), 3),
                        E2I_tasa=f'{int(np.sum(e2i))}/{len(e2i)} (+20/20 del log 101-120)')
    print(f"T-C (i) / T-E absolutas: E2 come B Q4 >= 50 en {nt - nf}/{nt} semillas del tronco (minimo {int(e2.min())}); "
          f"cota 95 % del fallo por semilla {p_up} -> P(>= 18/20) >= {OUT['T-C_i']['P_pasa_con_la_cota']}; E2I {OUT['T-C_i']['E2I_tasa']}")

    # ------------------------------------------------------------ legibilidad: TRONCO_B pasa T-A, T-C ii y T-F vivo (reparto del nulo)
    a0 = sys.argv
    sys.argv = [a0[0]]
    import corre_criterio_v4 as C4
    import corre_criterio_v3   # noqa: F401  (C4._v3 lo importa perezoso)
    sys.argv = a0
    Pleg = {}
    for etq, fa, fc in (('serie 2841-2920', list(FUENTES)[4], list(FUENTES)[5]), ('replica 2361-2440', list(FUENTES)[6], list(FUENTES)[7])):
        TA = [r for r in carga(fa)['corridas'] if r['arm'] in ('OFF', 'TRONCO_B')]
        TC = [r for r in carga(fc)['corridas'] if r['arm'] in ('OFF', 'TRONCO_B')]
        et = sorted({(r['seed'], r['arm']) for r in TA})
        por = {b: {(r['seed'], r['arm']): r for r in TA if r['brazo'] == b} for b in U.BRAZOS_TA}
        ok = dict(TA=0, TC=0, TF=0, todo=0); BB = 2000
        for _ in range(BB):
            p = g.permutation(len(et)); A = [et[i] for i in p[:80]]; Bm = [et[i] for i in p[80:160]]
            pc = g.permutation(len(TC)); Ac = [TC[i] for i in pc[:80]]; Bc = [TC[i] for i in pc[80:160]]
            ta = all(C4.letra_TA([por[b][k] for k in A], [por[b][k] for k in Bm], C4.U.V4['T-A'])[0] for b in U.BRAZOS_TA)
            tc = C4.letra_TC(Ac, Bc, C4.U.V4['T-C_ii'])[0]
            tf = all(C4.letra_TF([por[b][k] for k in A], [por[b][k] for k in Bm])[0] for b in U.BRAZOS_TA) and C4.letra_TF(Ac, Bc)[0]
            ok['TA'] += ta; ok['TC'] += tc; ok['TF'] += tf; ok['todo'] += (ta and tc and tf)
        Pleg[etq] = {k: round(v / BB, 4) for k, v in ok.items()}
    OUT['legible'] = Pleg
    print(f"legible (TRONCO_B pasa T-A, T-C ii y T-F vivo), reparto del nulo real OFF + TRONCO_B de V4-CAL, B = 2000: {Pleg}")

    # ------------------------------------------------------------ T-D (B-5 en dos series: el tronco en el mundo vivo con sal muda)
    import importlib
    sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'creacion_B'))
    CC = importlib.import_module('corre_codigo')
    u1, u2, u6 = CC.UMBRALES['C1'], CC.UMBRALES['C2'], CC.UMBRALES['C6']
    al, li = [], []
    for f in list(FUENTES)[8:10]:
        P = carga(f)['principal']
        al += [r for r in P if r['brazo'] == 'D1-ALIAS']; li += [r for r in P if r['brazo'] == 'D1-LIMPIA']
    fa = sum(not (r['w_sal'] <= u1['w'] and r['w_veneno'] <= u2['w1']) for r in al)
    fl = sum(not (r['w_sal'] <= u6['w'] and r['w_veneno'] <= u6['wv']) for r in li)
    OUT['T-D'] = dict(alias=len(al), alias_fallan=fa, limpias=len(li), limpias_fallan=fl,
                      valores_alias=sorted({(r['w_sal'], r['w_veneno']) for r in al}), valores_limpias=sorted({(r['w_sal'], r['w_veneno']) for r in li}),
                      p_fallo_cota95=cp_sup(fa + fl, len(al) + len(li)))
    print(f"T-D: el tronco con B-5 cumple C1/C2 en {len(al) - fa}/{len(al)} ALIAS y C6 en {len(li) - fl}/{len(li)} LIMPIAS "
          f"(valores {OUT['T-D']['valores_alias']} / {OUT['T-D']['valores_limpias']}); cota 95 % del fallo por semilla {OUT['T-D']['p_fallo_cota95']}")

    # ------------------------------------------------------------ T-G (subida_n7: 40 semillas reales de T142, N, NC3C)
    C7 = importlib.import_module('corre_n7')
    cr = []
    for f in list(FUENTES)[10:12]:
        cr += [r for r in carga(f)['crudos'] if r['brazo'] in U.TG['brazos']]
    semillas = sorted({r['seed'] for r in cr})
    por = {}
    for r in cr:
        por.setdefault(r['seed'], []).append(r)

    def letra_TG(res, n, como_N='N'):
        rr = []
        for r in res:
            if como_N != 'N':   # el NULO: el tronco presentado como candidato (sus corridas en el lugar de N)
                if r['brazo'] == 'N':
                    continue
                if r['brazo'] == como_N:
                    rr.append(dict(r)); rr.append(dict(r, brazo='N')); continue
            rr.append(r)
        V, kmax = C7.criterios(rr, U.TG['ks'], n)
        g1 = kmax.get('N', 0) >= U.TG['G1_kmax']
        g2 = all((V[k]['N'].get('lift_N>T142') or 0) >= U.TG['G2_n'] for k in U.TG['G2_ks'])
        g3 = all(V[k]['NC3C']['sep'] < U.TG['G3_sep'] and V[k]['NC3C']['lift_q4'] < U.TG['G3_lift'] for k in U.TG['ks'])
        return g1, g2, g3, kmax

    BT = 1000; okN = dict(G1=0, G2=0, G3=0, todo=0); okT = dict(G1=0, todo=0); kms = []
    for _ in range(BT):
        idx = g.integers(0, len(semillas), 20)
        res = [dict(r, seed=i) for i, s in enumerate(idx) for r in por[semillas[s]]]
        g1, g2, g3, km = letra_TG(res, 20)
        okN['G1'] += g1; okN['G2'] += g2; okN['G3'] += g3; okN['todo'] += (g1 and g2 and g3); kms.append(km['N'])
        h1, h2, h3, _ = letra_TG(res, 20, como_N='T142')
        okT['G1'] += h1; okT['todo'] += (h1 and h2 and h3)
    OUT['T-G'] = dict(semillas_reales=len(semillas), P_pasa_N={k: round(v / BT, 3) for k, v in okN.items()},
                      K_max_N_distribucion={str(k): kms.count(k) for k in sorted(set(kms))},
                      P_pasa_bajo_el_nulo_tronco_como_candidato={k: round(v / BT, 3) for k, v in okT.items()},
                      G2_signo_nulo_p05=round(binom_ge(20, 15, 0.5), 4), G2_margen_p085=round(binom_ge(20, 15, 0.85), 3))
    print(f"T-G (3T-k), bootstrap de {len(semillas)} semillas reales de subida_n7, n = 20, B = {BT}: N {OUT['T-G']['P_pasa_N']}, "
          f"K_max(N) {OUT['T-G']['K_max_N_distribucion']}; NULO (el tronco como candidato) {OUT['T-G']['P_pasa_bajo_el_nulo_tronco_como_candidato']}; "
          f"G-2 signo: nulo p = 0.5 -> {OUT['T-G']['G2_signo_nulo_p05']}, margen p = 0.85 -> {OUT['T-G']['G2_margen_p085']}")

    # ------------------------------------------------------------ conjunto (puertas independientes; CAND == tronco en T-A..T-F)
    pl = min(v['todo'] for v in Pleg.values())
    ptd = 0.95   # 36/36 sin fallos y valores exactos (0.0 / -3.0): no hay cota util con n = 36; se DECLARA 0.95
    pser = pl * PTB['todo'] * OUT['T-C_i']['P_pasa_con_la_cota'] * ptd * OUT['T-G']['P_pasa_N']['todo']
    OUT['conjunto'] = dict(P_legible=pl, P_TB=PTB['todo'], P_TCi_TE=OUT['T-C_i']['P_pasa_con_la_cota'], P_TD_declarada=round(ptd, 3),
                           P_TG=OUT['T-G']['P_pasa_N']['todo'], P_serie=round(pser, 3), P_serie_y_replica=round(pser ** 2, 3),
                           P_serie_sin_TB=round(pser / PTB['todo'], 3), P_serie_y_replica_sin_TB=round((pser / PTB['todo']) ** 2, 3))
    print(f"CONJUNTO por serie ~ {OUT['conjunto']['P_serie']} (serie y replica ~ {OUT['conjunto']['P_serie_y_replica']}); "
          f"SIN la banda de azar de T-B: {OUT['conjunto']['P_serie_sin_TB']} ({OUT['conjunto']['P_serie_y_replica_sin_TB']})")

    # ------------------------------------------------------------ coste por corrida (datos reales)
    segs = {}
    for f in list(FUENTES)[4:6]:
        C = carga(f)['corridas']; segs[os.path.basename(f)] = round(float(np.mean([r['seg'] for r in C])), 2)
    segs['n7 (T142/N/NC3C)'] = round(float(np.mean([r['seg'] for r in cr])), 2)
    OUT['seg_por_corrida_PC_bajo_Pool'] = segs
    OUT['seg'] = round(time.time() - t0, 1)
    os.makedirs(os.path.join(D, 'humo'), exist_ok=True)
    dj = os.path.join(D, 'humo', f"potencia_examen_v143_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(OUT, open(dj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    print(f"seg por corrida (PC, bajo Pool): {segs}")
    print(f"datos -> {os.path.relpath(dj, RAIZ)}  sha256_16 = {h16(dj)}  ({OUT['seg']} s)")
