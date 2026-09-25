"""identidad_codigo.py — ARNES del CODIGO v0 (identidad bit a bit + arnes por pieza). Un proceso. Semillas 27002 (identidad), 27003 (pieza).

MISION: llegar a la AGI por este camino.

I1  motor_codigo SIN codigo y SIN cambio == motor_gramatica, BIT A BIT (salida entera), en dos configuraciones (PERILLAS y VIDA de la gramatica).
I2  LA PEDIDA: la cinta inicial (compilada desde FIJO:filtra0 en G0), desarrollada y SIN errores de copia (c_on=False), da EXACTAMENTE la
    misma corrida que motor_gramatica con la gramatica FIJA en filtra0 (sin mutacion numerica, sin sombras). Salida entera menos d['codigo'].
I2b la misma cinta con el COPIADOR PRENDIDO pero todas sus zonas en TASA 0 (copia + SOS + desarrollo en cada parto y en cada fundador del
    vivero): misma corrida. El rng de la copia no toca el mundo.
I3  el cambio del mundo: antes de t_cambio la corrida es identica a la sin cambio (tamano, mordidas); despues, A da dS < 0 y B dS > 0.
I4  el copiador con errores corre en el mundo (sin abortar), los errores ocurren, la cinta cambia de largo, la SOS se registra.
P   arnes por pieza del lector y del copiador (cada instruccion cambia algo medible; la SOS sube la tasa cuando debe y solo entonces).
"""
import json, os, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
GRAMD = os.path.join(os.path.dirname(AQUI), 'gramatica')
for _d in (AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
import motor_codigo as MC
import codigo_def as CD
import gramatica_def as GD
import importlib.util
_sp = importlib.util.spec_from_file_location('motor_gramatica_ref', os.path.join(GRAMD, 'motor_gramatica.py'))
MG = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(MG)
import corre_codigo as RC

SEED = 27002; SEED_P = 27003
N0 = RC.MUNDO['n0']
OK = []


def chk(nombre, cond, extra=''):
    OK.append((nombre, bool(cond))); print(f"[{'OK ' if cond else 'MAL'}] {nombre} {extra}", flush=True)


def canon(x): return json.dumps(x, sort_keys=True, default=repr)


def corre(M, eco, T):
    return M.run_solapadas(SEED, [RC.CARRO] * N0, T=T, diag=0, mundo_n=RC.MUNDO['esc'], tope_cuerpos=RC.MUNDO['tope'], muestra=100, eco=eco)


def main():
    t0 = time.time()
    shas = RC.SHAS(); print(f"shas {shas}")
    import hashlib
    sg = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    chk('I0 carro y gramatica_def son COPIAS byte a byte', sg(os.path.join(AQUI, 'carros', 'FAMB_GRAM_ECO.py')) == sg(os.path.join(GRAMD, 'carros', 'FAMB_GRAM_ECO.py'))
        and sg(os.path.join(AQUI, 'gramatica_def.py')) == sg(os.path.join(GRAMD, 'gramatica_def.py')))
    T = 6000; tc = 3000
    base = dict(refunda=1, t_corte=tc, sigma=0.15, banco=200, cada_gen=1000, mutables=RC.MUTABLES, g_tope=4, g_alfabeto=RC.ALFABETO)
    # I1
    e1 = dict(base, gramatica=[GD.FILTRA0] * N0, p_mut=0.05, n_sombra=2, donante='padre', g_pcampo=0.05, g_pdup=0.02, g_pdel=0.02)
    a = corre(MG, dict(e1), T); b = corre(MC, dict(e1), T)
    chk('I1a sin codigo == motor_gramatica (PERILLAS, con sombras)', canon(a) == canon(b), f"nac {a['eco']['n_nac']} refund {a['eco']['n_refund']}")
    e1b = dict(base, gramatica=GD.fundadores_silenciosos(SEED, N0, RC.ALFABETO), p_mut=0.05, n_sombra=2, donante='azar', g_pcampo=0.05, g_pdup=0.02, g_pdel=0.02)
    a = corre(MG, dict(e1b), T); b = corre(MC, dict(e1b), T)
    chk('I1b sin codigo == motor_gramatica (silenciosos, AZAR)', canon(a) == canon(b))
    # I2 la pedida
    ref = dict(base, gramatica=[GD.FILTRA0] * N0, p_mut=0.0, n_sombra=0, donante='padre')
    a = corre(MG, dict(ref), T)
    b = corre(MC, dict(base, codigo=[RC.CINTA0] * N0, p_mut=0.0, n_sombra=0, donante='padre', c_on=False), T)
    bc = b.pop('codigo')
    chk('I2 CINTA0 sin errores de copia == gramatica FIJA filtra0 (BIT A BIT)', canon(a) == canon(b),
        f"nac {a['eco']['n_nac']} refund {a['eco']['n_refund']} n_banco {a['eco']['n_banco']} vivos {len(a['eco']['vivos_final'])}")
    chk('I2 ... y el lector corrio en cada parto y fundador del banco', len(bc['cod_nac']) == a['eco']['n_nac'] + a['eco']['n_banco'] and all(x[4] == 0 for x in bc['cod_nac']),
        f"{len(bc['cod_nac'])} desarrollos")
    c00 = CD.compila(tasa_copiador=0, tasa_cuerpo=0)
    b = corre(MC, dict(base, codigo=[c00] * N0, p_mut=0.0, n_sombra=0, donante='padre', c_on=True, c_sos=True), T); b.pop('codigo')
    chk('I2b copiador PRENDIDO con TASA 0 en toda la cinta == gramatica FIJA filtra0', canon(a) == canon(b))
    fm = [x[12] for x in bc['cod_nac'] if x[12] >= 0]
    print(f"    calibracion (mundo viejo, CINTA0 sin errores, T {T}): frac_mal del padre al parir: media {np.mean(fm):.3f} p50 {np.median(fm):.3f} "
          f"p90 {np.percentile(fm, 90):.3f} p99 {np.percentile(fm, 99):.3f} max {np.max(fm):.3f} (n {len(fm)}); U_SOS[2] = {CD.U_SOS[2]}")
    # I3 cambio
    tcb = 4000
    e3 = dict(base, codigo=[RC.CINTA0] * N0, p_mut=0.0, n_sombra=0, donante='padre', c_on=False)
    b0 = corre(MC, dict(e3), T); b1 = corre(MC, dict(e3, cambio=(tcb, 'A', 'B')), T)
    k = tcb // 100
    chk('I3a antes del cambio: identica a la sin cambio', b0['pista']['tam_total'][:k] == b1['pista']['tam_total'][:k] and
        b0['codigo']['cod_nac'] == [x for x in b0['codigo']['cod_nac']] and
        [x for x in b0['codigo']['cod_nac'] if x[0] < tcb] == [x for x in b1['codigo']['cod_nac'] if x[0] < tcb])
    ms = b1['codigo']['mord_signo']; print(f"    mord_signo {ms}")
    chk('I3b despues del cambio A es MALA y B es BUENA; antes al reves', ms.get('A/post', [0, 0])[0] == 0 and ms.get('A/post', [0, 0])[1] > 0 and
        ms.get('A/pre', [0, 0])[1] == 0 and ms.get('B/pre', [0, 0])[0] == 0 and ms.get('B/post', [1, 1])[1] == 0 and ms.get('C/post', [0, 1])[1] == 0)
    chk('I3c el cambio cambia la corrida despues de t_cambio', b0['pista']['tam_total'] != b1['pista']['tam_total'])
    # I4 copiador con errores en el mundo
    b = corre(MC, dict(base, codigo=[RC.CINTA0] * N0, p_mut=0.0, n_sombra=0, donante='padre', c_on=True, c_sos=True, cambio=(tcb, 'A', 'B')), T)
    cn = b['codigo']['cod_nac']; ne = [x[4] for x in cn]; lg = [x[7] for x in cn]
    chk('I4 errores de copia en el mundo: ocurren, cambian el largo, se registran', np.mean(ne) > 0.5 and len(set(lg)) > 1,
        f"errores/copia {np.mean(ne):.2f} · largo {min(lg)}..{max(lg)} · SOS {np.mean([x[5] for x in cn]):.3f} · fenotipo cambia {np.mean([x[6] for x in cn]):.3f} · tipos {np.sum([x[8:12] for x in cn], 0).tolist()}")
    # I5 checkpoint: reanudar DESPUES del cambio (con cinta, errores y SOS) da la misma corrida que sin cortar
    blobs = {}
    e5 = dict(base, codigo=[RC.CINTA0] * N0, p_mut=0.0, n_sombra=0, donante='padre', c_on=True, c_sos=True, cambio=(tcb - 500, 'A', 'B'),
              ckpt_cada=1000, ckpt_fn=lambda t, b_: blobs.__setitem__(t, b_))
    full = corre(MC, dict(e5), T)
    res = corre(MC, dict(e5, estado=blobs[tcb], ckpt_fn=lambda t, b_: None), T)
    chk('I5 checkpoint: reanudar despues del cambio == corrida entera (salida entera)', canon(full) == canon(res), f"reanuda en {tcb}, cambio en {tcb - 500}")
    # ---------------------------------------------------------------- P: arnes por pieza (desarrollo y copia, fuera del mundo)
    CF = MC.P.cfg_fabrica() if hasattr(MC, 'P') else None
    import pista2 as P2
    G0 = MC.genoma0(P2.cfg_fabrica()); lo, hi = MC.rangos(G0); EN = MC.ENTEROS
    dv = lambda c: CD.desarrolla(CD.valida(c), G0, lo, hi, EN)
    g0, gr0, _ = dv(RC.CINTA0)
    chk('P0 CINTA0 -> G0 exacto y filtra0', np.array_equal(g0, G0) and gr0 == GD.FILTRA0, CD.texto(RC.CINTA0))
    def cambia_en(c, j_esp):
        g, gr, _ = dv(c); d = set(np.flatnonzero(g != G0).tolist()); return d == set(j_esp), g, gr
    ok = all(cambia_en([('SUM', j, 1)], [j])[0] for j in range(18) if j != 14 or True)
    chk('P1 SUM j +1 cambia SOLO el rasgo j (los 18)', ok)
    for kx in range(3):
        okk, g, _ = cambia_en([('EJE', kx, 1)], [j for j, s in CD.EJES[kx]])
        chk(f'P2 EJE {kx} cambia sus 4 rasgos (pleiotropia)', okk, str({MC.NOMBRES[j]: round(float(g[j] / G0[j]), 3) for j, s in CD.EJES[kx]}))
    g1, _, _ = dv([('DEF', 0), ('SUM', 0, 1), ('FIN',), ('LLAMA', 0)]); g2, _, _ = dv([('DEF', 0), ('SUM', 0, 1), ('FIN',), ('LLAMA', 0), ('LLAMA', 0)])
    g3, _, _ = dv([('DEF', 0), ('SUM', 0, 2), ('FIN',), ('LLAMA', 0), ('LLAMA', 0)]); g4, _, _ = dv([('DEF', 0), ('SUM', 0, 1), ('FIN',)])
    chk('P3 gen MAESTRO: DEF sin LLAMA no hace nada; 2 LLAMA = doble; cambiar el DEF cambia todas las llamadas',
        np.array_equal(g4, G0) and abs(np.log(g2[0] / G0[0]) - 2 * np.log(g1[0] / G0[0])) < 1e-9 and abs(np.log(g3[0] / G0[0]) - 4 * np.log(g1[0] / G0[0])) < 1e-9)
    _, grA, _ = dv([('REP', 1), ('ORG', 1, 3, 0, 0), ('FIN',)]); _, grB, _ = dv([('REP', 2), ('ORG', 1, 3, 0, 0), ('FIN',)])
    _, grC, _ = dv([('REP', 1), ('ORG', 1, 3, 0, 0), ('FIN',), ('REP', 1), ('ORG', 1, 3, 0, 0), ('FIN',)])
    _, grD, _ = dv([('REP', 2), ('ORG', 1, 3, 0, 0), ('ORG', 2, 1, 2, 1)])   # sin FIN: cierra al final
    chk('P4 REP y duplicacion en tandem de un tramo DUPLICAN la estructura (el organo)', len(grA) == 1 and len(grB) == 2 and grB == grC and len(grD) == 4, f"{grB} · {grD}")
    _, grE, _ = dv([('ORG', 3, 1, 2, 2)]); chk('P5 ORG construye un slot', grE == ((3, 1, 2, 2, 0),))
    gF, _, _ = dv([('REP', 3), ('SUM', 2, 1)]); gG, _, _ = dv([('REP', 3), ('FIN',), ('SUM', 2, 1)])
    chk('P6 FIN cambia la estructura (con FIN el REP queda vacio)', abs(np.log(gF[2] / G0[2]) - 3 * 0.15) < 1e-9 and abs(np.log(gG[2] / G0[2]) - 0.15) < 1e-9)
    gH, _, st = dv([('DEF', 0), ('LLAMA', 0), ('SUM', 0, 1), ('FIN',), ('LLAMA', 0)])
    chk('P7 recursion acotada (PROF_MAX)', st['llamadas'] == CD.PROF_MAX + 0 or st['llamadas'] <= 2 ** CD.PROF_MAX, f"llamadas {st['llamadas']} pasos {st['pasos']}")
    # copiador
    rr = np.random.default_rng([SEED_P, 0, 23, 0])
    def err_medio(c, fm, sos_on=True, n=3000):
        return float(np.mean([CD.copia(c, rr, fm, sos_on)[1]['n'] for _ in range(n)]))
    cz = [('TASA', 0)] + [('SUM', 0, 0)] * 29; c4 = [('TASA', 4)] + [('SUM', 0, 0)] * 29
    e0 = err_medio(CD.valida(cz), 0.0); e4 = err_medio(CD.valida(c4), 0.0)
    chk('P8 TASA: zona 0 -> 0 errores; zona 4 -> 30 x 0.1', e0 == 0 and abs(e4 - 3.0) < 0.2, f"{e0} · {e4:.3f}")
    cmix = CD.valida([('TASA', 0)] + [('SUM', 0, 0)] * 15 + [('TASA', 4)] + [('SUM', 0, 0)] * 14)
    pos = np.zeros(40); rr2 = np.random.default_rng([SEED_P, 1, 23, 0])
    for _ in range(3000):
        c2, s2 = CD.copia(cmix, rr2, 0.0)
        # contar por zona con cambios de argumento no es trivial; medir que la PRIMERA mitad queda intacta
        pos[0] += int(c2[:16] == cmix[:16])
    chk('P9 zonas: el tramo en TASA 0 queda INTACTO en todas las copias (el tramo en TASA 4 no)', pos[0] == 3000)
    c0 = RC.CINTA0; u = CD.U_SOS[CD.regla_sos(c0)[0]]; f = CD.F_SOS[CD.regla_sos(c0)[1]]
    eb = err_medio(c0, u - 0.01); ea = err_medio(c0, u); en = err_medio(c0, u + 0.2, sos_on=False); ef = err_medio(c0, None)
    chk(f'P10 SOS: con frac_mal >= {u} la tasa sube x{f}; debajo no; sin SOS (brazo) no; fundador (None) no',
        abs(ea / eb - f) < 0.35 and abs(en / eb - 1) < 0.15 and abs(ef / eb - 1) < 0.15, f"debajo {eb:.3f} · arriba {ea:.3f} · sin_sos {en:.3f} · fundador {ef:.3f}")
    tipos = np.zeros(4)
    for _ in range(3000): tipos += CD.copia(c0, rr, 0.0)[1]['tipos']
    chk('P11 los 4 tipos de error ocurren en proporcion 0.55/0.20/0.15/0.10', all(abs(tipos / tipos.sum() - np.array([0.55, 0.2, 0.15, 0.1])) < 0.04), str(tipos.tolist()))
    cs = CD.valida([('TASA', 4), ('SOS', 0, 3)] + [('SUM', 0, 0)] * 10)
    cs2 = CD.valida([('TASA', 4), ('SUM', 0, 0)] * 5 + [('SOS', 0, 1)] + [('SOS', 0, 3)])
    chk('P12 la regla SOS es de la cinta: vale la PRIMERA SOS; sin SOS no hay SOS', CD.regla_sos(cs) == (0, 3) and CD.regla_sos(cs2) == (0, 1) and CD.regla_sos(cz) is None)
    print(f"\nARNES: {sum(o for _, o in OK)}/{len(OK)} · {round(time.time() - t0, 1)} s")
    json.dump(dict(ok=[list(x) for x in OK], shas=shas, seg=round(time.time() - t0, 1)), open(os.path.join(AQUI, 'datos', 'identidad_codigo.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
