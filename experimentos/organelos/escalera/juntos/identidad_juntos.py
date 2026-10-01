"""identidad_juntos.py — ARNES de "LOS TRES JUNTOS" (O1_TODO: memoria de lugar + senal + PREGUNTA). Un proceso; semillas de practica 738530-738539.
(K) shas (pista, juez, O1, corre_v143; lo importado de escalera/) + carros == construye_juntos + chequeo estatico + identidades cortas.
(C) EN EL MUNDO DE LA SERIE (mueve + c_e), salida ENTERA:
      las tres apagadas  O1_TODO0     == O1_LUGAR         (bit a bit)
      solo senal         O1_TODO_SEN  == O1_LUGAR_SENAL   (bit a bit)
      solo pregunta      O1_TODO_PREG == O1_LUGAR_PREG    (bit a bit)
    y lo mismo en el mundo de cada peldano (P7: c_e sin mueve; P10: mueve sin c_e) y con otra semilla.
    O1_TODO != cada pareja y != O1_LUGAR; O1_TODO_SBAR != O1_TODO (el control actua).
    c_e no toca a quien no emite: preg y lug con c_e 0.01 == con c_e 0 en la fisica de los linajes.
(m) O1_TODO escribe, lee, siembra, explora y olvida (> 0); O1_TODO_SBAR escribe y lee igual que un emisor (mismo canal).
(a) regla 14 (fila campo a campo): corre_juntos.trabajo('lug'/'preg') sin c_e == corre_p10.trabajo('lug'/'preg'); corre_juntos.trabajo('sen')
    sin mueve == corre_p7 fila de 'sen' (campos comunes).
(e) trabajo escribe JSON; --reanuda relee; brazo desconocido aborta dentro. (f) letra sintetica. (g) guardas y semillas.
Uso: python experimentos/organelos/escalera/juntos/identidad_juntos.py [--corto]
"""
import copy, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import corre_juntos as CJR
CR = CJR.CR; R7 = CJR.R7; CO = CJR.CO; ME = CJR.ME; MC = CJR.MC; CJ = CJR.CJ; CV = CJR.CV
import corre_p10 as C10
sys.path.insert(0, CO.PISTA); import revisa_carro as RC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]
CORTO = '--corto' in sys.argv
T = 900 if CORTO else 4500


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def fis(r):
    r = copy.deepcopy(r)
    for d in r['linajes']: d.pop('carro', None)
    return N(r)


def lin(r):
    """fisica de los linajes sin el bloque oasis de la pista ni los cobros (para comparar c_e 0.01 vs 0 en quien no emite)."""
    r = copy.deepcopy(r); out = []
    for d in r['linajes']:
        d.pop('carro', None); (d['_carrera'].get('oasis') or {}).pop('cobros', None); out.append(d)
    return N(out)


KW = dict(pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
def run(m, seed, **k): return N(MC.run(seed, [('X', m)] * 9, T=T, **dict(KW, **k)))


t0 = time.time()
print(f"ARNES identidad_juntos.py (T {T}{' CORTO' if CORTO else ''})")
chk("(K) verifica(): shas, carros == construye_juntos, mundo_tramo_c", CJR.verifica(lambda s: print('   ', s)))
for n, b in CJ.todas().items():
    v = RC.revisa_fuente(b.decode('utf-8'), n); chk(f"(K) chequeo estatico {n}: {'PASA' if not v else v[:2]}", not v)
chk("(K) identidad corta corre_p1", CO.identidad_corta(lambda s: print('   ', s), T=min(T, 1500)))
chk("(K) identidad corta corre_c", CR.identidad_corta_c(lambda s: print('   ', s), T=min(T, 1200)))
chk("(K) identidad corta corre_juntos", CJR.identidad_corta(lambda s: print('   ', s), T=min(T, 1500)))
lug, _ = CR.modulo('O1_LUGAR'); pg, _ = CR.modulo('O1_LUGAR_PREG'); R7.fija('sen'); sn = CV._MODS['O1_LUGAR_SENAL']
t0m, _ = CJR.modulo('O1_TODO0'); ts, _ = CJR.modulo('O1_TODO_SEN'); tp, _ = CJR.modulo('O1_TODO_PREG'); tt, _ = CJR.modulo('O1_TODO'); tb, _ = CJR.modulo('O1_TODO_SBAR')
MV = T // 3; CE = CJR.C_E
MUNDOS = {'serie (mueve + c_e)': dict(mueve=MV, c_e=CE), 'P7 (c_e, sin mueve)': dict(c_e=CE), 'P10 (mueve, sin c_e)': dict(mueve=MV)}
G = {}
for S in (738531, 738532):
    for nm, mk in MUNDOS.items():
        if S == 738532 and not nm.startswith('serie'): continue
        rl = run(lug, S, **mk); rs = run(sn, S, **mk); rp = run(pg, S, **mk)
        a0 = run(t0m, S, **mk); a_s = run(ts, S, **mk); a_p = run(tp, S, **mk)
        chk(f"(C) s {S} mundo {nm}: las tres apagadas O1_TODO0 == O1_LUGAR (salida ENTERA)", a0 == rl)
        chk(f"(C) s {S} mundo {nm}: solo senal O1_TODO_SEN == O1_LUGAR_SENAL (salida ENTERA)", a_s == rs)
        chk(f"(C) s {S} mundo {nm}: solo pregunta O1_TODO_PREG == O1_LUGAR_PREG (salida ENTERA)", a_p == rp)
        if nm.startswith('serie'): G[S] = (rl, rs, rp)
S = 738531; rl, rs, rp = G[S]; mk = MUNDOS['serie (mueve + c_e)']
rt = run(tt, S, **mk); rb = run(tb, S, **mk)
chk("(C) O1_TODO != O1_LUGAR, != pareja senal, != pareja pregunta (las piezas actuan juntas)", fis(rt) != fis(rl) and fis(rt) != fis(rs) and fis(rt) != fis(rp))
chk("(C) O1_TODO_SBAR != O1_TODO (el control de contenido actua) y != pareja pregunta", fis(rb) != fis(rt) and fis(rb) != fis(rp))
chk("(C) c_e no toca a quien no emite: lug y preg con c_e 0.01 == con c_e 0 (fisica de los linajes)",
    lin(rl) == lin(run(lug, S, mueve=MV)) and lin(rp) == lin(run(pg, S, mueve=MV)))
# (m)
tot = lambda r, k: sum(d['carro'].get(k, 0) for d in r['linajes'])
cob = lambda r: sum((d['_carrera'].get('oasis') or {}).get('cobros', 0) for d in r['linajes'])
chk(f"(m) O1_TODO escribe {tot(rt, 'sn_escribe')} (cobros {cob(rt)}), lee {tot(rt, 'sn_lee')}, siembra {tot(rt, 'sn_siembra')}, explora {tot(rt, 'pg_exc')}, olvida {tot(rt, 'pg_olv')} (todo > 0)",
    all(tot(rt, k) > 0 for k in ('sn_escribe', 'sn_lee', 'sn_siembra', 'pg_exc', 'pg_olv')) and cob(rt) > 0)
chk(f"(m) O1_TODO_SBAR escribe {tot(rb, 'sn_escribe')} y lee {tot(rb, 'sn_lee')} (> 0: mismo canal, mismo costo {cob(rb)}); explora {tot(rb, 'pg_exc')}",
    tot(rb, 'sn_escribe') > 0 and tot(rb, 'sn_lee') > 0 and cob(rb) > 0 and tot(rb, 'pg_exc') > 0)
chk("(m) lug no escribe ni explora; pareja senal no explora; pareja pregunta no escribe",
    cob(rl) == 0 and all('pg_exc' not in d['carro'] and 'sn_escribe' not in d['carro'] for d in rl['linajes'])
    and all('pg_exc' not in d['carro'] for d in rs['linajes']) and cob(rp) == 0 and all('sn_escribe' not in d['carro'] for d in rp['linajes']))
# (a) regla 14 a nivel de FILA
with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as td2:
    def q(x, quita): return N({k: v for k, v in x.items() if k not in quita})
    quita = ('seg', 'estado', 'i', 'tipo', 'brazo', 'aborto', 'pizarra', 'senal', 'latencia_vida', 'latencia', 'oasis_info')
    m10 = dict(CO.MUNDO_OASIS, mueve=600)
    for b in ('lug', 'preg'):
        xj = CJR.trabajo((0, b, 738533, 2000, td, False, m10)); x10 = C10.trabajo((0, b, 738533, 2000, td2, False, m10))
        chk(f"(a) regla 14 (fila): corre_juntos.trabajo('{b}') sin c_e == corre_p10.trabajo('{b}') campo a campo (s 738533, T 2000, mueve 600; salvo lo agregado)",
            xj['aborto'] is None and x10['aborto'] is None and q(xj, quita) == q(x10, quita) and q(xj, quita).get('preg') is not None)
    m7 = dict(R7.MUNDO_P7)
    xj = CJR.trabajo((1, 'sen', 738533, 2000, td, False, m7)); f7 = dict(R7.fila(R7.tarea(738534, 'sen', 2000), 2000))
    comunes = [k for k in f7 if k not in ('seg', 'estado', 'latencia')]
    chk(f"(a) regla 14 (fila): corre_juntos.trabajo('sen') sin mueve == corre_p7 fila de 'sen' en {len(comunes)} campos comunes (pizarra, senal y latencia por vida incluidas; s 738534, T 2000)",
        xj['aborto'] is None and all(N(xj[k]) == N(f7[k]) for k in comunes) and N(xj['latencia_vida']) == N(f7['latencia']) and xj['pizarra']['escrituras_total'] >= 0)
    mj = dict(CJR.MUNDO_J, mueve=600)
    x2 = CJR.trabajo((0, 'todo', 738535, 2000, td, False, mj))
    chk(f"(e) trabajo todo: JSON escrito; fila con preg (mudanzas {x2.get('preg', {}).get('mudanzas')}), pizarra (c_e {x2.get('pizarra', {}).get('c_e')}), estado SENAL 1 PREGUNTA 1 SN_BARAJA 0",
        x2['aborto'] is None and os.path.exists(os.path.join(td, 'prueba_i00_todo.json')) and x2['preg']['mudanzas'] == 3 and x2['pizarra']['c_e'] == CE
        and (x2['estado']['SENAL'], x2['estado']['SN_BARAJA'], x2['estado']['PREGUNTA']) == (1, 0, 1) and x2['oasis_info']['c_e'] == CE)
    x3 = CJR.trabajo((0, 'todo', 738535, 2000, td, True, mj))
    chk("(e) --reanuda relee igual", N({k: v for k, v in x2.items() if k != 'seg'}) == N({k: v for k, v in x3.items() if k != 'seg'}))
    x4 = CJR.trabajo((0, 'zzz', 738535, 2000, td, False, mj))
    chk("(e) brazo desconocido -> aborto escrito (nube-9)", x4['aborto'] is not None and os.path.exists(os.path.join(td, 'prueba_i00_zzz.json')))


# (f) letra sintetica
def sint(cz, n=20, aborto=0, quita=None, fund=None, lat=None, mud=4):
    R = {}
    dflt = {'todo': 6, 'sen': 5, 'preg': 8, 'lug': 4, 'todobar': 5}
    for b in CJR.ORDEN:
        R[b] = {}; s, sb, p = CJR.PERILLAS[b]
        for i in range(n):
            c = cz.get(b, [dflt[b]] * n)[i]; fm = (fund or {}).get(b, [10] * n)[i]; lt = (lat or {}).get(b, [1000] * n)[i]
            est = dict(carro=CJR.BRAZOS[b], mundo=dict(CJR.MUNDO_J), LUGAR=1, LUGAR_BARAJA=0, SENAL=s, SN_BARAJA=sb, PREGUNTA=p, PG_BARAJA=0)
            R[b][i] = dict(cruzan=c, mayoria=int(c * 2 > 9), R0_med=0.9, coherente=True, fund=[fm] * 9, fund_media=float(fm), fund_post10k=[0] * 9,
                           oasis=dict(mord_AC_dentro=5, extra=ME.EXTRA, pobre=ME.POBRE, ratio_pasos=3.0, ratio_mord=1.0), estado=est, vida_med=1000,
                           mundo_AC=2.0, mord_AC=100, mord_BD=10, T=100000, oasis_info=dict(mueve=CJR.MUEVE, c_e=CJR.C_E),
                           preg=dict(latencia_med=float(lt), latencias_n=36, nunca=0, mudanzas=mud, pg_exc=(100 if p else 0), pg_olv=(100 if p else 0)), lat_med=float(lt),
                           pizarra=dict(escrituras_total=(50 if s else 0), cobros_total=(50 if s else 0), c_e=CJR.C_E), senal=(dict(sn_escribe=50, sn_lee=40, sn_siembra=5) if s else None))
    if quita: quita(R)
    return CJR.lee_serie(R, n, aborto)


V = lambda L: L['veredicto']
L = sint({'todo': [9] * 20, 'preg': [8] * 14 + [7] * 6})
chk(f"(f) SUMAN: todo 9 gana a sen (5) y a preg (8/7) 20/20 con +26 y gana al control: {V(L)}", V(L) == 'SUMAN')
L = sint({'todo': [9] * 20, 'preg': [8] * 20, 'todobar': [9] * 20})
chk(f"(f) NO SUMAN: gana a las parejas pero NO al control de contenido: {V(L)} ({L['matiz']})", V(L) == 'NO SUMAN' and 'control' in (L['matiz'] or ''))
L = sint({})
chk(f"(f) SE ESTORBAN: todo 6 < la mejor pareja (preg 8) 20/20: {V(L)} mejor {L['mejor_pareja']}", V(L) == 'SE ESTORBAN' and L['mejor_pareja'] == 'preg')
L = sint({'todo': [8] * 20})
chk(f"(f) NO SUMAN: todo == la mejor pareja: {V(L)}", V(L) == 'NO SUMAN')
L = sint({'todo': [9] * 12 + [8] * 8, 'preg': [8] * 20})
chk(f"(f) NO SUMAN en el umbral: gana 12/20 (+12): {V(L)} umbral {L['en_umbral']}", V(L) == 'NO SUMAN' and L['en_umbral'])
L = sint({'todo': [9] * 20, 'preg': [9] * 10 + [7] * 10})
chk(f"(f) NO SUMAN por TECHO: preg en 9/9 en 10 semillas (ganables 10 < 13): {V(L)} ({L['matiz']}) alcanzable {L['techo']['SUMAN_alcanzable']}",
    V(L) == 'NO SUMAN' and 'TECHO' in (L['matiz'] or '') and not L['techo']['SUMAN_alcanzable'])
L = sint({'todo': [8] * 20}, fund={'todo': [1] * 20}, lat={'todo': [300] * 20})
chk(f"(f) sombra: todo == preg en cruzan, pero menos fundadores y menor latencia que las dos parejas: {V(L)} · SUMAN_en_sombra {L['sombra']['SUMAN_en_sombra']}",
    V(L) == 'NO SUMAN' and L['sombra']['SUMAN_en_sombra'])
chk("(f) NO SE LEE: un aborto", V(sint({'todo': [9] * 20, 'preg': [8] * 20}, aborto=1)) == 'NO SE LEE')
chk("(f) NO SE LEE: el mundo no se mudo 4 veces", V(sint({'todo': [9] * 20, 'preg': [8] * 20}, mud=3)) == 'NO SE LEE')
chk("(f) NO SE LEE: banda (lug en 9 = 180 > 115)", V(sint({'todo': [9] * 20, 'preg': [8] * 20, 'lug': [9] * 20})) == 'NO SE LEE')
chk("(f) NO SE LEE: banda (preg en 6 = 120 < 140)", V(sint({'preg': [6] * 20})) == 'NO SE LEE')


def _muda(R): R['todo'][3]['pizarra']['escrituras_total'] = 0
def _est(R): R['sen'][2]['estado']['PREGUNTA'] = 1
chk("(f) NO SE LEE: la senal no actua en una corrida de todo (0 escrituras)", V(sint({'todo': [9] * 20, 'preg': [8] * 20}, quita=_muda)) == 'NO SE LEE')
chk("(f) NO SE LEE: estado equivocado (pareja senal con PREGUNTA 1)", V(sint({'todo': [9] * 20, 'preg': [8] * 20}, quita=_est)) == 'NO SE LEE')
L = sint({'todo': [9] * 10, 'preg': [8] * 10}, n=10)
chk(f"(f) la letra escala a n 10 (gana >= {L['umbrales']['gana_par']}, suma >= {L['umbrales']['dif_suma']}; bandas a la mitad): {V(L)}", V(L) == 'SUMAN' and L['umbrales'] == dict(gana_par=7, dif_suma=5))
# (g)
ser = set(range(CJR.SEM['serie'], CJR.SEM['serie'] + 20)); rep = set(range(CJR.SEM['replica'], CJR.SEM['replica'] + 20))
exp = set(range(CJR.SEM['explora'], CJR.SEM['explora'] + 6)); hum = set(range(CJR.SEM['humo'], CJR.SEM['humo'] + 6)); pra = set(range(738530, 738540))
todo = [ser, rep, exp, hum, pra]
chk("(g) semillas: serie, replica, explora, humo y arnes disjuntas entre si y todas en 7385xx (fuera de 739xxx, la escalera previa)",
    all(not (a & b) for i, a in enumerate(todo) for b in todo[i + 1:]) and all(738500 <= s < 738600 for s in set.union(*todo)))


def aborta(argv):
    try: CJR.main(argv); return False
    except SystemExit: return True


chk("(g) banderas desconocidas o abreviadas abortan (--hum, --humo --x)", aborta(['--hum']) and aborta(['--humo', '--x']))
chk("(g) --humo con --pool aborta; --pool 3 aborta; --serie --T aborta; --serie --mueve aborta; --humo --n 3 aborta (9 corridas); --explora --T 250000 aborta",
    aborta(['--humo', '--pool', '2']) and aborta(['--serie', '--pool', '3']) and aborta(['--serie', '--T', '1000']) and aborta(['--serie', '--mueve', '10000'])
    and aborta(['--humo', '--n', '3']) and aborta(['--explora', '--T', '250000']))
g = CJR.guarda('serie', 'juntos_serie_x', False)
chk(f"(g) candado de --serie activo sin commit: {str(g)[:90]!r}", g is not None)
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
