"""identidad_v143ex.py -- ARNES DE IDENTIDAD del examen v4 de v14.3 (UN proceso, sin Pool; se corre ANTES de mirar numeros).
Ultima linea: 'RESULTADO: N/N'. Escribe su JSON en datos/humo/ (ERR-42). La salida se guarda en identidad_v143ex_salida.txt.

v14.3 = v14.2 + N (norm_lenta: el paso de la via lenta x 3.0/(P.P)). Memoria nueva CERO; constante nueva M0 = 3.0.

(0) CONSTRUCCION: los cinco archivos en disco == construye_v143.construye() (por anclas, cuerpo == subida_n7 con el defecto
    movido) y todas las anclas reusadas con su sha.
(A) PERILLA APAGADA: organismo_v143(norm_lenta=0) == organismo_v142 (CONGELADO) bit a bit, TODAS las claves, en los 12
    escenarios de organismo/identidad_v142.py (T = 20 000, semilla 43045).
(I) INERCIA con la perilla ENCENDIDA (el candidato tal cual): organismo_v143() == organismo_v142 en los mismos 12 escenarios
    (P.P = 3 -> factor 1.0 exacto). Es lo que el examen asume en T-C (i), T-E y T-F.
(B) MUNDO DE REGLA: organismo_v143g(0) == organismo_v142g y organismo_v143g() == organismo_v142g (px0, xor01, azar), kwargs
    del tronco EXPLICITOS (ERR-38).
(C) MUNDO VIVO: organismo_v143cal(0) == organismo_v3cal y organismo_v143cal() == organismo_v3cal en los montajes EXACTOS del
    examen: T-A VIVO, T-A CUELLO_MIN, T-C (ii) (reversion en T/2), T-D ALIAS 326 y LIMPIA 307 (sal muda); y la cadena:
    organismo_v143cal(vivo=0, n_nec=1) == organismo_v143 en las claves de v14.2.
(D) EL RUNNER: sus tareas dan CAND == tronco en T-A, T-C (ii), T-D, examen E2 (bateria copiada vs congelada, T = 100 000) y
    T-B (bateria_generaliza copiada vs congelada, T = 200 000).
(E) N ENCENDIDO REPRODUCE subida_n7: corre_examen_v143.tarea_tg (= corre_n7.tarea) en la semilla 7701 da, clave por clave, el
    crudo guardado de la serie de subida_n7 (N a k = 1, 5, 8 y T142 a k = 5; T = 100 000).
(R) REGLA 14: kwargs campo a campo, baterias copiadas vs congeladas, letra restada == letra importada, semillas.
(J) EL JUEZ contra los jueces que ya decidieron: T-D y T-B y T-E/T-C (i)/T-F sobre los crudos de dE5 reproducen su veredicto
    registrado (dE5 cayo T-E); T-A/T-C (ii)/T-F sobre V4-CAL reproducen TRONCO_B PASA y PEOR NO; T-G sobre subida_n7 reproduce
    K_max {T142 1, N 8, NC3C 0}.
(X) ENMIENDA ERR-122 (23-sep ~21:10, antes de la serie): la banda de azar G2 que DECIDE T-B es [0.31, 0.60]; la vieja
    [0.42, 0.58] (origen corre_dE5_v2, intacto; y banda interna de las baterias, que no se tocan) se calcula y SOLO se reporta,
    para CAND y TRONCO, en veredicto_TB, en la etapa 8 y en --combina (crudos sinteticos; no simula un paso).
(K) CONTROLES QUE DEBEN FALLAR O DIFERIR: la perilla ACTUA si P.P != 3 (organismo_v143, v143g y v143cal con PAT de masa 4);
    TRONCO_B != OFF; PLACEBO != OFF; N != T142 en 3T-k; el juez dice NO a un candidato sintetico malo y SI al bueno; el PARSER
    del runner rechaza banderas desconocidas, abreviadas, el modo de serie sin --pool y --pool > 6 (ERR-115). Solo se llama al
    parser, en este proceso; nunca a main(): este arnes no puede lanzar ninguna serie.

    python experimentos/tronco_v14_3_examen/identidad_v143ex.py
"""
import contextlib, io, json, os, sys, time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_examen_v143 as R   # pone sys.path (organismo/, mundo vivo, criterio_v3/v4, creacion_B, dE5, subida_n7)
import numpy as np

RAIZ = R.RAIZ
T = 20000
S = 43045            # semilla de IDENTIDAD (umbrales_examen_v143.SEMILLAS['identidad']): no es de ninguna serie
OK = [0]; NO = [0]; DET = []; t0 = time.time()
NUEV_V3CAL = {'desambiguar', 'des_splits', 'des_t', 'invertir_vivo_en', 'placebo'}


def N(x):
    return json.dumps(x, sort_keys=True, default=str)


def anota(bloque, nombre, bien, det=''):
    (OK if bien else NO)[0] += 1
    DET.append(dict(bloque=bloque, nombre=nombre, ok=bool(bien), det=det))
    print(f"  [{time.time() - t0:5.0f}s] ({bloque}) {'OK ' if bien else '***'} {nombre}" + ('' if bien or not det else f'  -> {det}'), flush=True)


def dif(a, b, claves=None, fuera=()):
    ks = claves if claves is not None else sorted((set(a) | set(b)) - set(fuera))
    return [k for k in ks if N(a.get(k, '<falta>')) != N(b.get(k, '<falta>'))]


def igual(bloque, nombre, a, b, claves=None, fuera=()):
    d = dif(a, b, claves, fuera)
    anota(bloque, nombre, not d, f'difieren {d[:6]}')


def distinto(bloque, nombre, a, b, claves):
    d = dif(a, b, claves)
    anota(bloque, nombre + ' (DEBE diferir)', bool(d), 'SALIO IDENTICO')


def callado(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return f(*a, **k)


if __name__ == '__main__':
    extra = sys.argv[1:]
    if extra:
        raise SystemExit(f'*** banderas desconocidas {extra}: este arnes no toma argumentos (ERR-115)')
    import organismo_v142 as V142, organismo_v143 as V143, organismo_v142g as V142G, organismo_v143g as V143G
    import organismo_v3cal as CAL, organismo_v143cal as V143C, construye_v143 as CO
    print(f'ARNES identidad_v143ex — T={T}, semilla {S}; python {sys.version.split()[0]}, numpy {np.__version__}')
    for nom, p in [('organismo_v142 (CONGELADO)', V142.__file__), ('organismo_v143', V143.__file__), ('organismo_v142g', V142G.__file__),
                   ('organismo_v143g', V143G.__file__), ('organismo_v3cal', CAL.__file__), ('organismo_v143cal', V143C.__file__),
                   ('corre_examen_v143', R.__file__), ('este arnes', os.path.abspath(__file__))]:
        print(f'  sha {nom:28s} {R.h16(p)}  {os.path.relpath(p, RAIZ)}')

    print('--- (0) construccion por anclas y anclas reusadas')
    C = CO.construye()
    for n_, txt in C.items():
        p = os.path.join(AQUI, n_)
        anota('0', f'{n_} en disco == construccion por anclas', os.path.exists(p) and open(p, 'rb').read().decode('utf-8') == txt)
    malas = [(os.path.relpath(p, RAIZ), R.h16(p), s) for p, s in R.ANCLAS.items() if R.h16(p) != s]
    anota('0', f'las {len(R.ANCLAS)} anclas reusadas tienen su sha', not malas, str(malas))

    ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)),
           ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
           ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
           ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)),
           ('AB sin hija dispersa', dict(mask_rel=0)), ('AB sin puerta por codigo', dict(puerta_pat=0)),
           ('AB las dos perillas v14 off', dict(mask_rel=0, puerta_pat=0)),
           ('AB D comida solap_B=2 (E2K)', dict(nuevo='D', nuevo_val='comida', solap_B=2, nuevo_en=15000))]
    print(f'--- (A) organismo_v143(norm_lenta=0) == organismo_v142 y (I) organismo_v143() == organismo_v142, T={T}')
    for etq, kw in ESC:
        ref = V142.run(S, T=T, **kw)
        igual('A', f'{etq}: N apagada == v14.2', V143.run(S, T=T, norm_lenta=0, **kw), ref)
        igual('I', f'{etq}: N ENCENDIDA (defecto) == v14.2 (inercia, P.P = 3)', V143.run(S, T=T, **kw), ref)

    print(f'--- (B) mundo de regla: organismo_v143g(0) y organismo_v143g() == organismo_v142g, T={T}')
    KWG = R.G142.INSTRUMENTOS['organismo_v142'][1]
    for regla in ('px0', 'xor01', 'azar'):
        ref = V142G.run(S, T=T, mundo='regla', regla=regla, **KWG)
        igual('B', f'regla/{regla}: N apagada == v142g', V143G.run(S, T=T, mundo='regla', regla=regla, norm_lenta=0, **KWG), ref)
        igual('B', f'regla/{regla}: N ENCENDIDA == v142g (20 patrones de masa 3)', V143G.run(S, T=T, mundo='regla', regla=regla, **KWG), ref)

    print(f'--- (C) mundo vivo: organismo_v143cal(0) y organismo_v143cal() == organismo_v3cal en los montajes del examen, T={T}')
    MONT = [('T-A VIVO', S, R.C4.kw_vivo('VIVO', 'OFF')), ('T-A CUELLO_MIN', S, R.C4.kw_vivo('CUELLO_MIN', 'OFF')),
            ('T-C (ii) reversion en T/2', S, R.C4.kw_rev('OFF', T)),
            ('T-D ALIAS 326 (sal muda)', 326, R.kw_sal('OFF')), ('T-D LIMPIA 307 (sal muda)', 307, R.kw_sal('OFF'))]
    for etq, s, kw in MONT:
        ref = CAL.run(s, T=T, **kw)
        igual('C', f'{etq}: N apagada == v3cal (todas las claves)', V143C.run(s, T=T, **dict(kw, norm_lenta=0)), ref)
        igual('C', f'{etq}: N ENCENDIDA == v3cal (inercia: PAT A-D de masa 3)', V143C.run(s, T=T, **dict(kw, norm_lenta=1)), ref)
    a = V143C.run(S, T=T, vivo=0, n_nec=1, placebo=0); b = V143.run(S, T=T)
    igual('C', 'cadena: organismo_v143cal(vivo=0, n_nec=1) == organismo_v143 (claves de v14.2)', a, b, claves=sorted(b))

    print('--- (D) las tareas del runner: CAND == tronco por el camino real del examen')
    o1, o2 = R.tarea_vivo(('VIVO', S, 'CAND', T)), R.tarea_vivo(('VIVO', S, 'OFF', T))
    anota('D', 'tarea_vivo VIVO: CAND (organismo_v143cal) == OFF (tarea calibrada de V4-CAL)', R.iguales(o1, o2), str(dif(o1, o2, fuera=('arm', 'org', 'seg'))[:5]))
    o1, o2 = R.tarea_rev((S, 'CAND', T)), R.tarea_rev((S, 'OFF', T))
    anota('D', 'tarea_rev: CAND == OFF', R.iguales(o1, o2), str(dif(o1, o2, fuera=('arm', 'org', 'seg'))[:5]))
    o1, o2 = R.tarea_sal(('S1-ALIAS', 326, 'CAND', T)), R.tarea_sal(('S1-ALIAS', 326, 'OFF', T))
    anota('D', 'tarea_sal ALIAS 326: CAND == OFF', R.iguales(o1, o2), str(dif(o1, o2, fuera=('arm', 'org', 'seg'))[:5]))
    o1, o2 = R.tarea_ex(('CAND', 'E2', S)), R.tarea_ex(('TRONCO', 'E2', S))
    anota('D', 'tarea_ex E2 (T = 100 000): bateria_v143 (copia) == bateria_v142 (CONGELADA)', R.iguales(o1, o2), str(dif(o1, o2, fuera=('org', 'seg'))[:5]))
    o1, o2 = R.tarea_tb(('CAND', 'px0', S)), R.tarea_tb(('TRONCO', 'px0', S))
    anota('D', 'tarea_tb px0 (T = 200 000): bateria_generaliza_v143 (copia) == bateria_generaliza_v142 (CONGELADA)', R.iguales(o1, o2),
          str(dif(o1, o2, fuera=('org', 'seg', 'modulo'))[:5]))

    print('--- (E) N encendido reproduce el crudo de subida_n7 (serie 7701-7720), T = 100 000')
    j7 = json.load(open(os.path.join(R.N7, 'datos', 'n7_serie_s7701-7720_T100000_20260923_174554.json'), encoding='utf-8'))
    guard = {(r['brazo'], r['k'], r['seed']): r for r in j7['crudos']}
    E = {}
    for b, k in (('N', 1), ('N', 5), ('N', 8), ('T142', 5)):
        E[(b, k)] = o = R.tarea_tg((b, k, 7701, 100000))
        g = guard[(b, k, 7701)]
        igual('E', f'{b} k={k} s7701: == crudo guardado de subida_n7 (sep {g["sep"]}, lift_q4 {g["lift_q4"]}, celdas {g["celdas"]})', o, g, fuera=('seg',))

    print('--- (R) regla 14 (sin simular)')
    for nombre, ok in R.regla14():
        anota('R', nombre, ok)

    print('--- (J) el juez reproduce a los jueces que ya decidieron (datos registrados, sin simular)')
    D = os.path.join(RAIZ, 'datos')
    jd = json.load(open(os.path.join(D, 'dE5_v2_20260921_152224.json'), encoding='utf-8'))['meta']['veredictos']
    td = json.load(open(os.path.join(D, 'dE5_v2_20260921_152224_crudo_TD.json'), encoding='utf-8'))['corridas']
    td = [dict(r, arm=('CAND' if r['arm'] == 'dE5' else r['arm'])) for r in td if r['brazo'] in ('S1-ALIAS', 'S1-LIMPIA')]
    vt = callado(R.veredicto_TD, td)
    anota('J', 'T-D sobre el crudo de dE5: C1/C2/C6 de OFF y dE5 == los registrados',
          all(N({c: vt[a][c] for c in ('C1', 'C2', 'C6')}) == N({c: jd['T-D'][b][c] for c in ('C1', 'C2', 'C6')})
              for a, b in (('OFF', 'OFF'), ('CAND', 'dE5'))))
    jb = json.load(open(os.path.join(D, jd['T-B']['json']), encoding='utf-8'))['corridas']
    tb = [dict(r, org=o) for r in jb for o in ('CAND', 'TRONCO')]
    vb = callado(R.veredicto_TB, tb)
    # ERR-122: el juez de dE5 decidio con la banda VIEJA; se compara lo igual con lo igual (y con la nueva tambien pasa: 0.532)
    anota('J', 'T-B sobre la generalizacion de dE5: G1, azar, G2, azar, K == los registrados; PASA con la banda vieja (la de ese juez) '
               '== lo registrado, y PASA tambien con la de ERR-122 (azar G2 0.532 esta en las dos)',
          all(abs((vb['CAND'][k] or 0) - (jd['T-B'][k] or 0)) < 1e-12 for k in ('G1', 'G1_azar', 'G2', 'G2_azar'))
          and vb['CAND']['K'] == jd['T-B']['K'] and vb['CAND']['pasa_banda_vieja'] == jd['T-B']['pasa']
          and vb['CAND']['pasa'] == jd['T-B']['pasa'])
    jc = json.load(open(os.path.join(D, jd['examen_json']['candidato']), encoding='utf-8'))['corridas']
    jt = json.load(open(os.path.join(D, jd['examen_json']['tronco']), encoding='utf-8'))['corridas']
    ex = [dict(r, org='CAND') for r in jc if r['etapa'] in R.U.SEIS] + [dict(r, org='TRONCO') for r in jt if r['etapa'] in R.U.SEIS]
    ve = callado(R.veredicto_EX, ex)
    anota('J', 'T-E / T-C (i) / T-F sobre el examen de dE5: 13/15/9/5/4/9 (T-E cae), T-C (i) 20/20, T-F pasa == lo registrado',
          all(ve['conducta'][e]['todas'] == jd['T-E']['escenarios'][e]['todas'] for e in R.U.SEIS)
          and ve['T_E']['pasa'] is False and jd['T-E']['pasa'] is False
          and ve['T_C_i']['comeB_Q4'] == jd['T-C_i']['comeB_Q4'] and ve['T_F']['pasa'] == jd['T-F_examen']['pasa'])
    cv = json.load(open(os.path.join(D, 'critv4_20260922_132544.json'), encoding='utf-8'))['veredictos']
    rv = json.load(open(os.path.join(D, 'critv4_20260922_132544_crudo_TA.json'), encoding='utf-8'))['corridas']
    rr = json.load(open(os.path.join(D, 'critv4_20260922_132544_crudo_TCii.json'), encoding='utf-8'))['corridas']
    rel = lambda L: [dict(r, arm='CAND') if r['arm'] == 'PEOR' else r for r in L]
    vv = callado(R.veredicto_vivo, rel(rv), rel(rr))
    anota('J', 'T-A / T-C (ii) / T-F vivo sobre V4-CAL 2841-2920: PEOR (como CAND) NO, TRONCO_B PASA (LI VIVO -4.152), PLACEBO PASA == lo registrado',
          vv['CAND']['v4'] is False and cv['PEOR']['v4'] is False and vv['TRONCO_B']['v4'] is True and vv['PLACEBO']['v4'] is True
          and vv['TRONCO_B']['T-A']['brazos']['VIVO']['det_v4']['NI']['LI'] == cv['TRONCO_B']['T-A']['brazos']['VIVO']['det_v4']['NI']['LI'] == -4.152)
    tg = [r for r in j7['crudos'] if r['brazo'] in R.U.TG['brazos']]
    vg = callado(R.veredicto_TG, tg, 20)
    anota('J', 'T-G sobre la serie de subida_n7: K_max {T142 1, N 8, NC3C 0} == lo registrado; G-1, G-2, G-3 PASAN',
          {b: vg['K_max'][b] for b in R.U.TG['brazos']} == {b: j7['K_max'][b] for b in R.U.TG['brazos']} == {'T142': 1, 'N': 8, 'NC3C': 0}
          and vg['pasa'])

    print('--- (X) ENMIENDA ERR-122: decide azar G2 en [0.31, 0.60]; la banda vieja [0.42, 0.58] SOLO se reporta (crudos sinteticos)')
    import tempfile
    U_ = R.U; ub = R.D5.UMB['T-B']; bt = R.banda_TB()
    anota('X', 'la banda que DECIDE azar G2 es [0.31, 0.60] (NUM == ERR122[banda_nueva] == banda_TB); G1 0.80, G2 0.85, '
               'azar G1 [0.35, 0.65] y cobertura 6 == corre_dE5_v2 / letra, sin cambio',
          tuple(U_.NUM['TB_azar2']) == tuple(U_.ERR122['banda_nueva']) == bt['azar2'] == (0.31, 0.60)
          and (bt['g1'], bt['g2'], bt['azar']) == (ub['g1'], ub['g2'], tuple(ub['azar'])) == (0.80, 0.85, (0.35, 0.65))
          and U_.NUM['TB_cob'] == 6, str(bt))
    interna = '0.42 <= float(np.median(baz)) <= 0.58'
    leer = lambda p: open(p, encoding='utf-8').read()
    anota('X', 'la banda VIEJA [0.42, 0.58] == corre_dE5_v2.UMB[T-B][azar2] (origen intacto) == banda_TB[azar2_vieja]; '
               'bateria_generaliza_v142 (CONGELADA) y v143 conservan su banda interna',
          tuple(ub['azar2']) == tuple(U_.ERR122['banda_vieja']) == bt['azar2_vieja'] == (0.42, 0.58)
          and interna in leer(R.G142.__file__) and interna in leer(R.G143.__file__))
    Ss = R.U.SEMILLAS['serie']
    RV, RR, TB0, EXr, TD, TG = R.sinteticos(80, 20, Ss['ALIAS'], Ss['LIMPIAS'])
    con = lambda x: [dict(r, ba=x) if r['regla'] == 'azar' else dict(r) for r in TB0]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        v36 = R.veredicto_TB(con(0.36))
    anota('X', 'azar G2 0.36 (dentro de la nueva, fuera de la vieja): CAND y TRONCO PASAN con ERR-122 y eso decide (V[pasa]); '
               'la vieja dice NO y SOLO queda como informe',
          v36['pasa'] is True and all(v36[o]['pasa'] and v36[o]['c_azar2'] and not v36[o]['c_azar2_banda_vieja']
                                      and not v36[o]['pasa_banda_vieja'] for o in R.U.ORGS_EX)
          and v36['banda_azar2'] == dict(err='ERR-122', decide=[0.31, 0.6], vieja_solo_informe=[0.42, 0.58]), str(v36.get('banda_azar2')))
    bordes = {x: callado(R.veredicto_TB, con(x))['pasa'] for x in (0.30, 0.31, 0.50, 0.60, 0.61)}
    v50 = callado(R.veredicto_TB, con(0.50))
    anota('X', 'bordes de la banda ERR-122 (cerrada): azar G2 0.30 NO, 0.31 PASA, 0.50 PASA, 0.60 PASA, 0.61 NO; con 0.50 la vieja '
               'tambien PASA (la nueva contiene a la vieja)',
          bordes == {0.30: False, 0.31: True, 0.50: True, 0.60: True, 0.61: False}
          and v50['CAND']['pasa_banda_vieja'] and v50['TRONCO']['pasa_banda_vieja'], str(bordes))
    s = buf.getvalue()
    anota('X', 'el log de T-B imprime la banda que decide ([0.31, 0.6], ERR-122) y la vieja [0.42, 0.58] marcada SOLO INFORME, '
               'NO decide, para CAND y TRONCO',
          '(en [0.31, 0.6], ERR-122)' in s and 'banda VIEJA de azar G2 [0.42, 0.58]' in s and 'SOLO INFORME, NO decide' in s
          and 'CAND azar G2 0.360 FUERA -> T-B NO' in s and 'TRONCO azar G2 0.360 FUERA -> T-B NO' in s
          and s.count('ERR-122) K 20/20 -> PASA') == 2, s[-400:])
    Vs = callado(lambda: dict(TB=R.veredicto_TB(con(0.36)), EX=R.veredicto_EX(EXr), TD=R.veredicto_TD(TD),
                              vivo=R.veredicto_vivo(RV, RR), TG=R.veredicto_TG(TG, 20)))
    buf8 = io.StringIO()
    with contextlib.redirect_stdout(buf8):
        sub8, P8, leg8, fr8 = R.etapa8(Vs, 'arnes-ERR122')
    l8 = [l for l in buf8.getvalue().splitlines() if '   T-B: ' in l]
    anota('X', 'etapa 8: T-B PASA por la banda nueva; su linea lleva al TRONCO (banda ERR-122) PASA y la banda vieja SOLO INFORME '
               '(CAND NO, TRONCO NO); el veredicto de la serie es PASA',
          P8['T-B'] is True and fr8.startswith('PASA') and len(l8) == 1 and 'T-B: PASA' in l8[0]
          and 'TRONCO (mismas semillas, banda ERR-122) PASA' in l8[0]
          and 'banda VIEJA [0.42, 0.58] (SOLO INFORME): CAND NO, TRONCO NO' in l8[0], (l8 or [''])[0][-300:])
    with tempfile.TemporaryDirectory() as td_:
        fs = []
        for modo in ('serie', 'replica'):
            f_ = os.path.join(td_, f'examen_v143_{modo}_arnes.json')
            json.dump(dict(meta=dict(modo=modo), legible=True, sub=sub8, puertas=P8, frase=fr8, veredictos=Vs),
                      open(f_, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
            fs.append(f_)
        frc, lc = R.combina(fs)
    lc_tb = [l for l in lc if 'T-B serie' in l or 'T-B replica' in l]
    anota('X', '--combina: VEREDICTO PASA (decide ERR-122) y por serie imprime la banda vieja SOLO INFORME (CAND NO, TRONCO NO)',
          frc.startswith('VEREDICTO DEL EXAMEN: PASA') and len(lc_tb) == 2
          and all('decide [0.31, 0.6] (ERR-122): CAND PASA TRONCO PASA' in l
                  and 'banda vieja [0.42, 0.58] SOLO INFORME: CAND NO TRONCO NO' in l for l in lc_tb), str(lc_tb)[-300:])

    print('--- (K) controles que DEBEN fallar o diferir')
    P4 = {'A': np.array([1, 1, 0, 1, 1, 0.]), 'B': np.array([1, 0, 1, 0, 1, 1.]), 'C': np.array([0, 1, 1, 1, 0, 1.]), 'D': np.array([1, 0, 1, 1, 0, 1.])}
    for mod, etq, kw in ((V143, 'organismo_v143 (AB)', dict()), (V143G, 'organismo_v143g (AB)', dict(R.G142.INSTRUMENTOS['organismo_v142'][1])),
                         (V143C, 'organismo_v143cal (mundo vivo VIVO)', R.C4.kw_vivo('VIVO', 'OFF'))):
        viejo = {k: v.copy() for k, v in mod.PAT.items()}
        try:
            for k in mod.PAT:
                mod.PAT[k] = P4[k]
            a1 = mod.run(43046, T=T, **dict(kw, norm_lenta=1)); a0 = mod.run(43046, T=T, **dict(kw, norm_lenta=0))
        finally:
            for k in viejo:
                mod.PAT[k] = viejo[k]
        distinto('K', f'{etq} con PAT de MASA 4: N encendida != N apagada (la perilla actua si P.P != 3)', a1, a0,
                 ['W', 'W_lenta', 'Wps', 'Wns', 'deaths', 'mord'])
    oA = R.tarea_vivo(('VIVO', 43046, 'OFF', T))
    distinto('K', 'TRONCO_B (s + 100000) != OFF en la misma semilla-etiqueta', R.tarea_vivo(('VIVO', 43046, 'TRONCO_B', T)), oA,
             ['r', 'deaths', 'descendientes', 'splits'])
    distinto('K', 'PLACEBO (placebo = 1) != OFF', R.tarea_vivo(('VIVO', 43046, 'PLACEBO', T)), oA, ['r', 'deaths', 'descendientes', 'splits'])
    distinto('K', 'N != T142 en 3T-k a k = 5 (s7701): la reparacion SI actua donde P.P = 18', E[('N', 5)], E[('T142', 5)], ['lift_q4', 'sep', 'mordidas'])
    Ss = R.U.SEMILLAS['serie']
    for malo in (False, True):
        RV, RR, TB, EXr, TD, TG = R.sinteticos(80, 20, Ss['ALIAS'], Ss['LIMPIAS'], malo=malo)
        Vs = callado(lambda: dict(TB=R.veredicto_TB(TB), EX=R.veredicto_EX(EXr), TD=R.veredicto_TD(TD), vivo=R.veredicto_vivo(RV, RR),
                                  TG=R.veredicto_TG(TG, 20)))
        P = R.puertas_de(R.subpuertas(Vs))
        if malo:
            anota('K', 'el juez dice NO a un candidato sintetico MALO en T-A, T-B, T-C, T-D y T-G (r y rev -40, azar 0.30, |W[sal]| 1.45, sin componer)',
                  not any(P[k] for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-G')), str(P))
        else:
            anota('K', 'el juez dice SI al candidato sintetico bueno (idem al tronco) y la serie se lee', all(P.values()) and Vs['vivo']['legible'], str(P))
    # Solo se llama al PARSER del runner (R.argumentos), en este proceso: nunca a main(). Aunque alguien cambiara el parser, este
    # control no puede lanzar ninguna serie (ERR-115: los agentes no ejecutan runners con --serie en ninguna forma).
    for args, etq in ((['--humoo'], 'bandera desconocida --humoo'), (['--humo', '--humoo'], 'modo valido + bandera desconocida --humoo'),
                      (['--hum'], 'abreviatura --hum (allow_abbrev=False)'),
                      (['--serie'], 'modo de serie sin --pool'), (['--serie', '--pool', '9'], '--pool 9 (> 6)')):
        viejo, err = sys.argv, io.StringIO()
        sys.argv = ['corre_examen_v143.py'] + args
        try:
            with contextlib.redirect_stderr(err):
                R.argumentos()
            codigo = 0
        except SystemExit as e:
            codigo = e.code
        finally:
            sys.argv = viejo
        anota('K', f'el parser del runner RECHAZA {etq} (argparse, codigo 2; solo se parsea, nunca se corre)',
              codigo == 2 and 'error:' in err.getvalue(), f"codigo {codigo}; {err.getvalue()[-160:]!r}")

    tot = f'RESULTADO: {OK[0]}/{OK[0] + NO[0]}'
    bloques = {}
    for d in DET:
        o, t = bloques.get(d['bloque'], (0, 0)); bloques[d['bloque']] = (o + d['ok'], t + 1)
    print('\n' + '  '.join(f'({b}) {o}/{t}' for b, (o, t) in bloques.items()) + f'   ({time.time() - t0:.0f} s)')
    os.makedirs(R.DATOS_HUMO, exist_ok=True)
    f = os.path.join(R.DATOS_HUMO, f"identidad_v143ex_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(dict(T=T, semilla=S, total=tot, bloques=bloques, detalle=DET, seg=round(time.time() - t0, 1),
                   python=sys.version.split()[0], numpy=np.__version__), open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'datos -> {os.path.relpath(f, RAIZ)}  sha256_16 = {R.h16(f)}')
    print(tot)
    sys.exit(0 if NO[0] == 0 else 1)
