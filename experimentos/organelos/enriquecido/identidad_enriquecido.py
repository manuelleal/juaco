"""identidad_enriquecido.py — arnes de identidad de MUNDO ENRIQUECIDO (29-sep-2026). Un proceso; T corto (30 000, vivero hasta 10 000);
semillas del arnes 50181-50186. Salida ENTERA en identidad_enriquecido_salida.txt. Mision: llegar a la AGI por este camino.

(K) motor_enriquecido.py == construccion por anclas desde bloques/opusM/motor_bloques.py (sha fijado); shas del runner.
(A) TODO APAGADO (kit 1, nuez 0, social 0): motor_enriquecido == motor_bloques en TODAS las claves de trabajo() y en BQ_OUT
    (BLOQ_V con las tasas de la serie; ING_F1_V sin reglas).
(B) NUEZ PRENDIDA con f = 0 y canal OFF (social 3), kit 1: == motor_bloques (la capa y los rng propios no tocan nada).
(B2) CANAL OFF (social 3) == SIN CANAL (social 0) con nueces (f 0.5) y el kit enriquecido y una regla 'copiar' forzada en los
    fundadores: todas las claves y BQ_OUT iguales; en NZ solo cambian los contadores de disparos/monedas (8, 9).
(C) CONTROLES QUE DEBEN FALLAR: f 0.5 != f 0; SOC != OFF y copia; DESF != SOC y copia; llave imposible -> 0 aperturas.
(S) la mecanica: intentos == abre + falla; con f 1 toda A que llega es nuez; el sentido 'nuez' ACTUA (regla forzada 'foco nuez ->
    boca -' baja los intentos); la llave ACTUA (abre > 0 con llave C).
(D) DETERMINISMO: SOC dos veces == (claves, BQ_OUT, NZ_OUT).
(Q) corte de luz en t = 20 000 + --reanuda == la corrida entera (SOC con copia forzada, vivero permanente para que haya
    checkpoint): claves, BQ_OUT y NZ_OUT.
(R) reanudar con OTRA cfg (de NZ o de BQ) aborta (no sigue en silencio).
(L) la LETRA (corre_enriquecido.veredicto) y medidas() en entradas sinteticas, con extincion del control (H-1 del auditor);
(L3) --reanuda reintenta un JSON abortado (H-3); banderas del runner.
"""
import copy, json, os, shutil, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
sys.path.insert(0, AQUI); sys.path.insert(0, os.path.join(ORG, 'bloques', 'opusM'))
import corre_enriquecido as CE   # noqa: E402
import corre_bloques as CB       # noqa: E402  (solo para enchufar motor_bloques; no se toca)
NS = CE.NS
assert CB.NS is NS
T = 30000; TC = 10000
CAR = os.path.join(AQUI, 'datos', 'arnes')
LOG = []
KIT1 = dict(CB.DEF, on=1, donante='padre')   # las tasas de la serie de BLOQUES, kit 1
COPIA = [[0, 0, 0, 1.01, 4, 3.0]]              # 'hambre < 1.01 -> copiar +3': siempre se cumple (impulso 3 -> moneda 1)


def p(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ok(nombre, cond, info=''):
    p(f"  [{'OK ' if cond else 'MAL'}] {nombre} {info}")
    return bool(cond)


def run_bl(seed, brazo, bq):
    MB = CB.usa_bloques(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(bq)
    r = NS.trabajo((seed, brazo, T, TC, NS.FRIO['T_lect'], os.path.join(CAR, 'bl'), False))
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float)), None


def run_en(seed, brazo, bq, nz, car='en', rean=False, TT=None, tc=TC):
    MB = CE.usa_motor(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(bq); MB.NZ_CFG.clear(); MB.NZ_CFG.update(nz)
    r = NS.trabajo((seed, brazo, TT or T, tc, NS.FRIO['T_lect'], os.path.join(CAR, car), rean))
    Z = json.loads(json.dumps(MB.NZ_OUT, default=float)) if (nz.get('nuez') or nz.get('social')) else None
    return r, json.loads(json.dumps(MB.BQ_OUT, default=float)), Z


def difs(a, b, fuera=('seg', 'brazo')):
    ks = sorted(set(a) | set(b))
    return [k for k in ks if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True)]


def jd(x):
    return json.dumps(x, sort_keys=True)


def bq_igual(a, b):
    """BQ_OUT igual en todo salvo 'cfg'; en 'cfg', iguales en las claves de BLOQUES (la enriquecida agrega nsen/nacc = 6/4)."""
    a = dict(a); b = dict(b); ca = a.pop('cfg', {}); cb = b.pop('cfg', {})
    comunes = set(ca) & set(cb)
    extra = {k: v for k, v in list(ca.items()) + list(cb.items()) if k not in comunes}
    return jd(a) == jd(b) and all(jd(ca[k]) == jd(cb[k]) for k in comunes) and extra in ({}, dict(nsen=6, nacc=4))


def nz_sin(Z, cols=(8, 9)):
    """NZ_OUT sin los contadores dados (en la serie: columnas 2 + c; en NZC_T: c) y sin la cfg."""
    Z = copy.deepcopy(Z); Z.pop('cfg', None)
    for row in Z['serie']:
        for c in cols: row[2 + c] = None
    for c in cols: Z['NZC_T'][c] = None
    return Z


NZ0 = dict(CE.NZ_DEF, nuez=0, social=0)


def main():
    t0 = time.time(); n = 0; n_ok = 0
    shutil.rmtree(CAR, ignore_errors=True)
    p('identidad_enriquecido.py', time.strftime('%Y-%m-%d %H:%M:%S'), f'T {T}, t_corte {TC}')

    def chk(nombre, cond, info=''):
        nonlocal n, n_ok
        n += 1; n_ok += ok(nombre, cond, info)
    p('(K) construccion por anclas y shas')
    out = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_enriquecido.py'), '--verifica'], capture_output=True, text=True).stdout.strip()
    chk('construye --verifica', out.startswith('IGUAL'), out)
    try:
        CE.verifica(); chk('shas fijados (nucleo, motor_bloques, motor_enriquecido)', True)
    except SystemExit as e:
        chk('shas fijados', False, str(e))

    p('(A) todo apagado == motor_bloques')
    B = {}
    for br, bq in (('BLOQ_V', KIT1), ('ING_F1_V', dict(KIT1, on=0))):
        B[br] = run_bl(50181, br, bq)
        e = run_en(50181, br, dict(bq, nsen=6, nacc=4), NZ0)
        d = difs(B[br][0], e[0])
        chk(f'{br} s50181 claves', not d and e[0]['aborto'] is None, f'distintas {d} · n_nac {e[0].get("n_nac")} · persiste {e[0].get("persiste")}')
        chk(f'{br} s50181 BQ_OUT (cfg: + nsen 6, nacc 4)', bq_igual(B[br][1], e[1]), f"(hijos {e[1].get('n_hijos')}, ins {e[1].get('n_ins')})")

    p('(B) nuez con f = 0 y canal OFF, kit 1 == motor_bloques')
    e = run_en(50181, 'BLOQ_V', dict(KIT1, nsen=6, nacc=4), dict(CE.NZ_DEF, nuez=1, f=0.0, social=3))
    chk('claves', not difs(B['BLOQ_V'][0], e[0]), str(difs(B['BLOQ_V'][0], e[0])))
    chk('BQ_OUT (cfg: + nsen 6, nacc 4)', bq_igual(B['BLOQ_V'][1], e[1]))
    chk('hubo A que llegaron (la rama de nuez corrio) y 0 nueces', e[2]['NZC_T'][6] > 0 and e[2]['NZC_T'][7] == 0, f"NZC_T {e[2]['NZC_T']}")

    p('(B2) canal OFF == sin canal (nueces f 0.5, kit enriquecido, copia forzada en los fundadores)')
    bqF = dict(CE.BQ_DEF, forzada=COPIA)
    off = run_en(50182, 'NUEZ_OFF', bqF, dict(CE.NZ_DEF, social=3))
    sin = run_en(50182, 'NUEZ_OFF', bqF, dict(CE.NZ_DEF, social=0))
    chk('claves', not difs(off[0], sin[0]), str(difs(off[0], sin[0])))
    chk('BQ_OUT', jd(off[1]) == jd(sin[1]))
    chk('NZ igual salvo disparos/monedas', jd(nz_sin(off[2])) == jd(nz_sin(sin[2])))
    chk('OFF: hubo disparos y monedas, 0 copias', off[2]['NZC_T'][8] > 0 and off[2]['NZC_T'][9] > 0 and off[2]['NZC_T'][10] == 0,
        f"NZC_T {off[2]['NZC_T']}")

    p('(C) controles que deben fallar')
    f0 = run_en(50182, 'NUEZ_OFF', bqF, dict(CE.NZ_DEF, social=0, f=0.0))
    chk('f 0.5 != f 0', bool(difs(sin[0], f0[0])), f"{len(difs(sin[0], f0[0]))} claves distintas; nueces {sin[2]['NZC_T'][7]} vs {f0[2]['NZC_T'][7]}")
    soc = run_en(50182, 'NUEZ_SOC', bqF, dict(CE.NZ_DEF, social=1))
    chk('SOC != OFF y copia', bool(difs(off[0], soc[0])) and soc[2]['NZC_T'][10] > 0, f"copias {soc[2]['NZC_T'][10]} · NZC_T {soc[2]['NZC_T']}")
    des = run_en(50182, 'NUEZ_DESF', bqF, dict(CE.NZ_DEF, social=2))
    chk('DESF != SOC y copia', bool(difs(soc[0], des[0])) and des[2]['NZC_T'][10] > 0, f"copias {des[2]['NZC_T'][10]} · NZC_T {des[2]['NZC_T']}")
    chk('SOC y DESF: mismo primer disparo (mismo gatillo): disparos > 0 en ambos', soc[2]['NZC_T'][8] > 0 and des[2]['NZC_T'][8] > 0)
    imp = run_en(50182, 'NUEZ_OFF', bqF, dict(CE.NZ_DEF, social=0, llave=7))
    chk('llave imposible -> 0 aperturas, falla == intentos > 0', imp[2]['NZC_T'][1] == 0 and imp[2]['NZC_T'][2] == imp[2]['NZC_T'][0] > 0,
        f"NZC_T {imp[2]['NZC_T']}")

    p('(S) mecanica')
    for nom, z in (('sin canal', sin), ('SOC', soc), ('DESF', des)):
        c = z[2]['NZC_T']
        chk(f'{nom}: intentos == abre + falla; abre > 0 (la llave C abre)', c[0] == c[1] + c[2] and c[1] > 0, f'{c[:5]}')
    f1 = run_en(50183, 'NUEZ_OFF', bqF, dict(CE.NZ_DEF, social=0, f=1.0))
    chk('f 1: toda A que llega es nuez', f1[2]['NZC_T'][6] == f1[2]['NZC_T'][7] > 0, f"{f1[2]['NZC_T'][6:8]}")
    base = run_en(50183, 'NUEZ_OFF', dict(CE.BQ_DEF, p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0), dict(CE.NZ_DEF, social=0))
    evn = run_en(50183, 'NUEZ_OFF', dict(CE.BQ_DEF, p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0, forzada=[[6, 0, 1, 0.5, 0, -3.0]] * 2),
                 dict(CE.NZ_DEF, social=0))
    ib, ie = base[2]['NZC_T'][0], evn[2]['NZC_T'][0]
    chk("el sentido 'nuez' ACTUA: 'foco nuez -> boca -6' baja los intentos a < 30 %", ib > 0 and ie < 0.3 * ib, f'{ie} vs {ib}')

    p('(D) determinismo')
    s2 = run_en(50182, 'NUEZ_SOC', bqF, dict(CE.NZ_DEF, social=1))
    chk('SOC dos veces ==', not difs(soc[0], s2[0]) and jd(soc[1]) == jd(s2[1]) and jd(soc[2]) == jd(s2[2]))

    p('(Q) corte de luz en t = 20 000 + reanuda == entera')
    ent = run_en(50184, 'NUEZ_SOC', bqF, dict(CE.NZ_DEF, social=1), car='Q_a', tc=T)   # vivero permanente: hay checkpoint en 20 000
    MB = CE.usa_motor()
    orig = NS.CR.ME.run_solapadas

    def corta(*a, _o=orig, **k):
        fn = k['eco']['ckpt_fn']

        def fn2(tt, blob):
            fn(tt, blob)
            if tt == 20000: raise KeyboardInterrupt('corte simulado en t = 20000')
        k['eco'] = dict(k['eco'], ckpt_fn=fn2)
        return _o(*a, **k)
    NS.CR.ME.run_solapadas = corta
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(bqF); MB.NZ_CFG.clear(); MB.NZ_CFG.update(dict(CE.NZ_DEF, social=1))
    try:
        NS.trabajo((50184, 'NUEZ_SOC', T, T, NS.FRIO['T_lect'], os.path.join(CAR, 'Q_b'), False)); cortado = False
    except KeyboardInterrupt:
        cortado = True
    chk('se corto en t = 20 000', cortado)
    shutil.copytree(os.path.join(CAR, 'Q_b'), os.path.join(CAR, 'Q_c'))   # copias del corte para (R)
    shutil.copytree(os.path.join(CAR, 'Q_b'), os.path.join(CAR, 'Q_d'))
    rea = run_en(50184, 'NUEZ_SOC', bqF, dict(CE.NZ_DEF, social=1), car='Q_b', rean=True, tc=T)
    chk('reanuda: claves', not difs(ent[0], rea[0]), str(difs(ent[0], rea[0])))
    chk('reanuda: BQ_OUT', jd(ent[1]) == jd(rea[1]))
    chk('reanuda: NZ_OUT', jd(ent[2]) == jd(rea[2]), f"copias {rea[2]['NZC_T'][10]} abre {rea[2]['NZC_T'][1]}")

    p('(R) reanudar con otra cfg aborta')
    mal = run_en(50184, 'NUEZ_SOC', bqF, dict(CE.NZ_DEF, social=2), car='Q_c', rean=True, tc=T)
    mal2 = run_en(50184, 'NUEZ_SOC', dict(bqF, p_ins=0.03), dict(CE.NZ_DEF, social=1), car='Q_d', rean=True, tc=T)
    chk('social distinto -> aborto con mensaje', (mal[0].get('aborto') or '').find('otra cfg de NZ') >= 0, str(mal[0].get('aborto')))
    chk('BQ distinto (p_ins) -> aborto con mensaje', (mal2[0].get('aborto') or '').find('otra cfg de BQ') >= 0, str(mal2[0].get('aborto')))
    chk('el corte dejo checkpoint (Q y R prueban algo)', cortado and os.path.exists(os.path.join(CAR, 'Q_c', 'ckpt', 'NUEZ_SOC_s50184.pkl')) and os.path.exists(os.path.join(CAR, 'Q_d', 'ckpt', 'NUEZ_SOC_s50184.pkl')))

    p('(L) la letra y las medidas en entradas sinteticas')
    def fake(b, s, fo, si, fc=0.5, pers=1, nue=100, cop=10, inten=500):
        return dict(seed=s, brazo=b, T=CE.T_EXPLORA, t_corte=CE.T_CORTE, aborto=None, bloqueados=0, carro=CE.FAB, persiste=pers,
                    cfg_bq=CE.cfg_de(b)[0], cfg_nz=CE.cfg_de(b)[1],
                    med=dict(frac_ok=fo, SI=si, frac_copia_T=fc, nueces_creadas=(0 if b == 'REF' else nue),
                             intentos=(0 if b == 'REF' else inten), copias=(0 if b in ('REF', 'NUEZ_OFF') else cop)))
    S = CE.SEM_EXPLORA
    D = {b: {s: fake(b, s, {'NUEZ_SOC': 0.8, 'NUEZ_OFF': 0.5, 'NUEZ_DESF': 0.5, 'REF': 0.0}[b], (0.3 if b != 'REF' else None)) for s in S}
         for b in CE.EXPLORA_BR}
    chk('letra: SOC gana a OFF y DESF con SI 0.3 -> FUNCIONA', CE.veredicto(D)[0] == 'FUNCIONA')
    D2 = copy.deepcopy(D)
    for s in S: D2['NUEZ_DESF'][s]['med']['frac_ok'] = 0.8
    chk('letra: DESF iguala a SOC -> HAY ALGO MODESTO (P1 + P3)', CE.veredicto(D2)[0] == 'HAY ALGO MODESTO')
    D3 = copy.deepcopy(D2)
    for s in S: D3['NUEZ_SOC'][s]['med']['SI'] = 0.0; D3['NUEZ_OFF'][s]['med']['frac_ok'] = 0.8
    chk('letra: nada gana y SI 0 -> NO', CE.veredicto(D3)[0] == 'NO')
    D4 = copy.deepcopy(D); del D4['REF'][S[0]]
    chk('letra: falta una corrida -> NO EVALUABLE', CE.veredicto(D4)[0] == 'NO EVALUABLE')
    D5 = copy.deepcopy(D)
    for s in S[:3]: D5['NUEZ_OFF'][s]['persiste'] = 0
    chk('letra: OFF persiste 2/5 -> NO EVALUABLE (mundo invivible)', CE.veredicto(D5)[0] == 'NO EVALUABLE')
    D6 = copy.deepcopy(D); D6['NUEZ_OFF'][S[0]]['med']['copias'] = 3
    chk('letra: OFF con copias -> NO EVALUABLE (sanidad)', CE.veredicto(D6)[0] == 'NO EVALUABLE')
    # H-1 del auditor: extincion del control
    D7 = copy.deepcopy(D)
    for s in S[:3]: D7['NUEZ_DESF'][s]['persiste'] = 0
    chk('letra: DESF persiste 2/5 -> NO EVALUABLE (V2 tambien para DESF)', CE.veredicto(D7)[0] == 'NO EVALUABLE')
    D8 = copy.deepcopy(D)   # DESF extinto en 1 semilla con frac_ok 0 (SOC 'ganaria' por extincion): ese par NO cuenta; quedan 4
    D8['NUEZ_DESF'][S[0]]['persiste'] = 0; D8['NUEZ_DESF'][S[0]]['med']['frac_ok'] = 0.0
    for s in S[1:]: D8['NUEZ_DESF'][s]['med']['frac_ok'] = 0.8   # en los pares validos DESF iguala a SOC
    v8 = CE.veredicto(D8)
    chk('letra: el par con DESF extinto no cuenta (P2 cae: 0/4 validos) -> HAY ALGO MODESTO', v8[0] == 'HAY ALGO MODESTO' and not v8[2]['p2']
        and v8[2]['pares_p2'] == list(S[1:]), str(v8[2].get('pares_p2')))
    D9 = copy.deepcopy(D)   # DESF extinto en 2 semillas: 3 pares validos (< 4 exigidos) aunque SOC gane en los 3
    for s in S[:2]:
        D9['NUEZ_DESF'][s]['persiste'] = 0; D9['NUEZ_DESF'][s]['med']['frac_ok'] = 0.0
    v9 = CE.veredicto(D9)
    chk('letra: 3 pares validos < 4 -> P2 NO SE CUMPLE aunque SOC gane los 3 (-> MODESTO por P1 + P3)', (not v9[2]['p2']) and v9[2]['p1']
        and v9[0] == 'HAY ALGO MODESTO', str(v9[2].get('pares_p2')))
    D10 = copy.deepcopy(D)   # OFF persiste pero con < 20 intentos en una semilla: ese par no cuenta
    D10['NUEZ_OFF'][S[0]]['med']['intentos'] = 5
    v10 = CE.veredicto(D10)
    chk('letra: par con < 20 intentos no cuenta (quedan 4 validos, SOC gana 4/4 -> FUNCIONA)', v10[0] == 'FUNCIONA' and v10[2]['pares_p1'] == list(S[1:]))
    # medidas(): una serie sintetica
    row = lambda t, c: [t, 10] + c + [2, 3, 5]
    c0 = [0] * 16; c1 = [100, 30, 70, 400, 40] + [0] * 11; cT = [300, 180, 120, 800, 90] + [0] * 11
    d = dict(T=100000, tam_total=[10] * 101, nz=dict(serie=[row(20000, c0), row(50000, c1), row(100000, cT)], NZC_T=cT, nueces_T=5))
    m = CE.medidas(d)
    chk('medidas: ventana [T/2, T] (200 intentos, 150 abre -> 0.75; P(llave|A) 50/400 -> SI 0.625)',
        m['intentos'] == 200 and abs(m['frac_ok'] - 0.75) < 1e-9 and abs(m['SI'] - 0.625) < 1e-9, json.dumps(m))
    p('(L3) --reanuda reintenta un M_*.json ABORTADO (H-3 del auditor)')
    car3 = os.path.join(CAR, 'L3'); os.makedirs(car3, exist_ok=True)
    fn3 = os.path.join(car3, 'M_NUEZ_OFF_s50185.json')
    json.dump(dict(seed=50185, brazo='NUEZ_OFF', T=2000, aborto='SystemExit: simulado', K=None), open(fn3, 'w'))
    o3 = CE.corre(50185, 'NUEZ_OFF', 2000, car3, reanuda=True)
    chk('abortado -> se reintenta y queda sin aborto', o3.get('aborto') is None and json.load(open(fn3)).get('aborto') is None and o3.get('med') is not None)
    o4 = CE.corre(50185, 'NUEZ_OFF', 2000, car3, reanuda=True)
    chk('hecho -> se salta (mismo JSON)', json.dumps(o4, sort_keys=True) == json.dumps(o3, sort_keys=True))
    p('(L2) banderas del runner')
    r1 = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_enriquecido.py'), '--explora', '--pool', '3'], capture_output=True, text=True)
    chk('--explora --pool 3 se niega', r1.returncode != 0 and 'pool' in (r1.stdout + r1.stderr))
    r2 = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_enriquecido.py'), '--humo', '--xyz'], capture_output=True, text=True)
    chk('bandera desconocida aborta', r2.returncode != 0 and 'desconocidas' in (r2.stdout + r2.stderr))
    p(f'RESUMEN: {n_ok}/{n} OK en {time.time() - t0:.0f} s')
    with open(os.path.join(AQUI, 'identidad_enriquecido_salida.txt'), 'w', encoding='utf-8') as f: f.write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
