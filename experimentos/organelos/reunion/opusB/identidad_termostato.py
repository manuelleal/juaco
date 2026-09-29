"""identidad_termostato.py — ARNES del confirmatorio del termostato en la pista (Opus B, 28-sep-2026). Un proceso; semillas de practica 5969xx.
(K) shas fijados de todo lo que corre + carros == construye_pas.
(a) regla 14: corre_pas.tarea(V143 / V143_TERMO / O1) == corre_v143.tarea (salvo 'seg').
(b) el brazo ctl (V143_PAS, p 0, sin siembra) == corre_evo.tarea(V143_EVO_BAJO) de termo_banco (linajes, pista, R0_pista; id normalizado).
(c) cadenas de 2 pasajes: pasaje 0 pasg == ctl en el juez; pasaje 1: pasg funda de la siembra (todos), ctl de la inicial (ninguno);
    y la fisica del pasaje 1 difiere (la transferencia actua: control que puede fallar).
(d) trabajo() escribe su JSON y --reanuda lo relee igual; la prueba pasg lee la siembra final de SU cadena.
(e) LA LETRA en casos sinteticos: FUNCIONA, HAY ALGO MODESTO, NO, NO SE LEE (aborto; V2 roto), PC rota -> no FUNCIONA.
(f) guardas: semillas de serie, replica y practica disjuntas y en 596xxx; banderas desconocidas/abreviadas abortan; --humo con --pool aborta;
    el humo cabe (<= 6 corridas, <= 200 000 pasos).
"""
import copy, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_termostato as CT
CPS = CT.CPS; CV = CT.CV; P = CT.P
sys.path.insert(0, os.path.join(CT.RAIZ, 'experimentos', 'organelos', 'termo_banco'))
import corre_evo as CE

N = lambda x: json.loads(json.dumps(x, default=str))
OK = True


def chk(nombre, c):
    global OK
    OK &= bool(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def sinid(x): return json.loads(json.dumps(N(x)).replace('V143_EVO_BAJO#', 'C#').replace('V143_PAS#', 'C#'))
def sin_seg(x): return N({k: v for k, v in x.items() if k not in ('seg', 'tel_ps', 'tel_evo')})


t0 = time.time()
print("ARNES identidad_termostato.py")
chk("(K) verifica(): shas fijados y carros == construye_pas", CT.verifica(lambda s: print('   ', s)))
CPS.registra(); CE.registra()
# (a)
for ident in ('V143', 'V143_TERMO', 'O1'):
    x = CPS.tarea(596950, ident, 2000); y = CV.tarea((596950, ident, 2000)); x.pop('tel_ps')
    chk(f"(a) regla 14: tarea({ident}) == corre_v143.tarea (s 596950, T 2000)", sin_seg(x) == sin_seg(y))
# (b)
carro, trans, pm = CT.BRAZOS['ctl']
x = CPS.tarea(596951, carro, 4000, siembra=None, pmut=pm); y = CE.tarea((596951, 'V143_EVO_BAJO', 4000))
chk("(b) ctl (V143_PAS, p 0, sin siembra) == corre_evo.tarea(V143_EVO_BAJO) (s 596951, T 4000)",
    sinid(x['linajes']) == sinid(y['linajes']) and x['R0_pista'] == y['R0_pista'] and sinid(x['pista']) == sinid(y['pista']))
# (c)
base = (596900, 596990)
cg = CT.cadena(0, 'pasg', base, 2, 4000); cc = CT.cadena(0, 'ctl', base, 2, 4000)
k = ('R0_real', 'fund', 'fund_post10k', 'cruza')
chk("(c) pasaje 0: pasg == ctl en el juez", all(cg['pasajes'][0][z] == cc['pasajes'][0][z] for z in k))
a1, c1 = cg['pasajes'][1], cc['pasajes'][1]
chk(f"(c) pasaje 1: pasg funda de la siembra {a1['fund_de_siembra']}/{a1['fund_n']}; ctl {c1['fund_de_siembra']}/{c1['fund_n']}",
    a1['fund_n'] > 0 and a1['fund_de_siembra'] == a1['fund_n'] and c1['fund_de_siembra'] == 0)
chk("(c) control que puede fallar: la fisica del pasaje 1 difiere entre pasg y ctl", any(a1[z] != c1[z] for z in k))
chk("(c) la siembra final de pasg es la del ultimo pasaje (n > 0)", len(cg['siembra_final'] or []) == a1['n_siembra'] > 0)
# (d)
with tempfile.TemporaryDirectory() as td:
    x1 = CT.trabajo(('cadena', 0, 'pasg', base, 2, 3000, 3000, td, False))
    x2 = CT.trabajo(('cadena', 0, 'pasg', base, 2, 3000, 3000, td, True))
    chk("(d) trabajo escribe su JSON y --reanuda lo relee igual", x1['aborto'] is None and N(x1) == N(x2))
    y1 = CT.trabajo(('prueba', 0, 'pasg', base, 2, 3000, 3000, td, False))
    chk(f"(d) la prueba pasg usa la siembra de SU cadena (g {y1.get('g_siembra_usada')}; fund de siembra {y1.get('fund_de_siembra')}/{y1.get('fund_n')})",
        y1['aborto'] is None and y1['g_siembra_usada'] == CT.g_de(x1['siembra_final']) and y1['fund_de_siembra'] == y1['fund_n'] > 0)
    z1 = CT.trabajo(('prueba', 1, 'pasg', base, 2, 3000, 3000, td, False))
    chk("(d) prueba pasg sin cadena -> aborto (nube-9), no se inventa siembra", z1['aborto'] is not None)


# (e) la letra en casos sinteticos
def sint(r0, g_ult, g_ctl, may_o1=20, v143=0.6, rota_v2=False, n=20):
    C = {}; R = {}
    for b in CT.CADENA_BRAZOS:
        C[b] = {}
        for i in range(n):
            p0 = dict(R0_real=[0.1] * 9, fund=[1] * 9, fund_post10k=[0] * 9, cruza=[0] * 9, g_siembra=0.03)
            if rota_v2 and b == 'ctl' and i == 0: p0 = dict(p0, fund=[2] * 9)
            pu = dict(p0, g_siembra=(g_ult if b == 'pasg' else g_ctl))
            C[b][i] = dict(pasajes=[p0, pu])
    for b in CT.PRUEBA_BRAZOS:
        R[b] = {i: dict(coherente=True, R0_med=(v143 if b == 'v143' else r0.get(b, 0.5)) + 0.001 * i, mayoria=int(b == 'o1' and i < may_o1),
                        fund_n=9, fund_de_siembra=(9 if b == 'pasg' else 0), fund=[1] * 9) for i in range(n)}
    return C, R


C, R = sint(dict(pasg=0.85, ctl=0.4, termo=0.9, o1=0.95), 0.2, 0.03)
chk("(e) FUNCIONA: pasg 0.85 > v143 0.6 y > ctl 0.4; g 0.03 -> 0.20; ctl g 0.03", CT.lee_serie(C, R, 20, 0)['veredicto'] == 'FUNCIONA')
C, R = sint(dict(pasg=0.55, ctl=0.4, termo=0.9, o1=0.95), 0.2, 0.03)
chk("(e) HAY ALGO MODESTO: pasg 0.55 < v143 0.6 (PA v143 falla), gana a ctl por 0.15, g en banda", CT.lee_serie(C, R, 20, 0)['veredicto'] == 'HAY ALGO MODESTO')
C, R = sint(dict(pasg=0.45, ctl=0.4, termo=0.9, o1=0.95), 0.05, 0.03)
chk("(e) NO: pasg apenas gana a ctl (+0.05) y g no sube", CT.lee_serie(C, R, 20, 0)['veredicto'] == 'NO')
C, R = sint(dict(pasg=0.85, ctl=0.4, termo=0.9, o1=0.95), 0.2, 0.2)
chk("(e) PC rota (ctl tambien sube g a 0.20) -> no FUNCIONA (MODESTO)", CT.lee_serie(C, R, 20, 0)['veredicto'] == 'HAY ALGO MODESTO')
C, R = sint(dict(pasg=0.85, ctl=0.4, termo=0.9, o1=0.95), 0.2, 0.03)
chk("(e) un aborto -> NO SE LEE", CT.lee_serie(C, R, 20, 1)['veredicto'] == 'NO SE LEE')
C, R = sint(dict(pasg=0.85, ctl=0.4, termo=0.9, o1=0.95), 0.2, 0.03, rota_v2=True)
chk("(e) V2 rota (p0 pasg != ctl) -> NO SE LEE", CT.lee_serie(C, R, 20, 0)['veredicto'] == 'NO SE LEE')
C, R = sint(dict(pasg=0.85, ctl=0.4, termo=0.9, o1=0.95), 0.2, 0.03, may_o1=14)
chk("(e) ancla O1 con 14/20 -> NO SE LEE", CT.lee_serie(C, R, 20, 0)['veredicto'] == 'NO SE LEE')
C, R = sint(dict(pasg=0.85, ctl=0.4, termo=0.9, o1=0.95), 0.2, 0.03, v143=0.35)
chk("(e) ancla V143 0.35 fuera de [0.40, 0.80] -> NO SE LEE", CT.lee_serie(C, R, 20, 0)['veredicto'] == 'NO SE LEE')
C, R = sint(dict(pasg=0.85, ctl=0.4, termo=0.9, o1=0.95), 0.65, 0.03)
chk("(e) g se pasa de la banda (0.65) -> PB falla -> no FUNCIONA", CT.lee_serie(C, R, 20, 0)['veredicto'] != 'FUNCIONA')
chk("(e) bloque: FUNCIONA + MODESTO -> MODESTO; NO SE LEE manda", CT.bloque('FUNCIONA', 'HAY ALGO MODESTO') == 'HAY ALGO MODESTO'
    and CT.bloque('FUNCIONA', 'NO SE LEE') == 'NO SE LEE')
# (f)
S = {}
for m, bb in list(CT.BASES.items()) + [('practica', CT.HUMO['base'])]:
    n = CT.N_IND if m != 'practica' else 10
    S[m] = {CT.sem_pas(bb, i, p) for i in range(n) for p in range(CT.NPAS)} | {CT.sem_pru(bb, i) for i in range(n)}
chk("(f) semillas serie / replica / practica disjuntas y todas en 596000-596999",
    not (S['serie'] & S['replica']) and not (S['serie'] & S['practica']) and not (S['replica'] & S['practica'])
    and all(596000 <= s <= 596999 for v in S.values() for s in v) and len(S['serie']) == 220 and len(S['replica']) == 220)
for bad in (['--seri'], ['--serie', '--pol', '6'], ['--humo', '--pool', '3']):
    try:
        CT.main(bad); r = 'no aborta'
    except SystemExit:
        r = 'aborta'
    chk(f"(f) {bad} aborta", r == 'aborta')
H = CT.HUMO; nh = H['n'] * (2 * H['npas'] + len(H['prueba']))
chk(f"(f) humo: {nh} corridas, {H['n'] * (2 * H['npas'] * H['T_pas'] + len(H['prueba']) * H['T_pru'])} pasos", nh <= 6
    and H['n'] * (2 * H['npas'] * H['T_pas'] + len(H['prueba']) * H['T_pru']) <= 200000)
print(f"{'ARNES PASA' if OK else 'ARNES FALLA'}  ({time.time()-t0:.0f}s)")
sys.exit(0 if OK else 1)
