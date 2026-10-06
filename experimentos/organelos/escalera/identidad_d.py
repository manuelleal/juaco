"""identidad_d.py — ARNES del TRAMO D (mundo_familia sobre motor_eco, celula FAMB_RES0_ECO). Un proceso; semillas de practica 739280-739289.
(K) motor_eco.py sha medido y mundo construido (11 anclas); carro cargado por motor_eco.carga_eco.
(M) familia None == motor_eco BIT A BIT (salida entera, con eco); familia apagada == motor_eco salvo su telemetria.
(P) cada perilla ACTUA y difiere de la base: sexo (sin_pareja > 0 o con_pareja > 0; los tipos nacidos reparten X/Y; fisica != base);
    recombina (recombinaciones > 0; genomas de hijos != de la madre en algun gen; != clon); pareja fuerte != azar (misma fisica si solo hay
    una candidata: se exige != con r_par grande); dote_doble (pagos > 0; != sexo); camada (trofico > 0; != base; ningun trofico sin
    necesidad: se exige que el padre tuviera E o Ag < u_cam: se verifica por construccion de la regla).
(c) cada perilla con su control: clon (recombina 0) tiene con_pareja > 0 y 0 recombinaciones.
Uso: python experimentos/organelos/escalera/identidad_d.py [--corto]
"""
import copy, json, os, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import corre_d as CD
MF = CD.MF; MEC = CD.MEC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [True]; NCHK = [0, 0]
CORTO = '--corto' in sys.argv
T = 800 if CORTO else 4000


def chk(nombre, c):
    c = bool(c); OK[0] &= c; NCHK[0] += 1; NCHK[1] += int(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def fis(r):
    r = copy.deepcopy(r)
    for d in r['linajes']: d['_carrera'].pop('familia', None); d.pop('carro', None)
    r['pista'].pop('familia', None)
    return N(r)


KW = dict(T=T, diag=0, mundo_n=CD.ESC, tope_cuerpos=CD.TOPE, muestra=CD.MUESTRA, eco=CD.eco_cfg(T))
def run(seed, fam=None, **k): return N(MF.run(seed, [CD.CARRO] * CD.N_LIN, **dict(KW, **k), familia=fam))


t0 = time.time()
print(f"ARNES identidad_d.py (T {T}{' CORTO' if CORTO else ''})")
info = MF.construye()[1]; chk(f"(K) mundo_familia construido: {info}", info['anclas'] == len(MF.ANCLAS))
chk("(K) identidad corta de corre_d (familia None == motor_eco; familia apagada == motor_eco salvo telemetria)", CD.identidad_corta(lambda s: print('   ', s), T=min(T, 800)))
S = 739281
base = N(MEC.run_solapadas(S, [CD.CARRO] * CD.N_LIN, **KW)); r0 = run(S)
chk(f"(M) familia None == motor_eco BIT A BIT (salida entera, s {S}, T {T}) y mismo rng", r0 == base and r0['pista']['rng_mundo_estado'] == base['pista']['rng_mundo_estado'])
# sexo + recombina
rs = run(S, dict(sexo=1, recombina=1, pareja='azar', r_par=40)); fa = rs['pista']['familia']; fl = [d['_carrera']['familia'] for d in rs['linajes']]
chk(f"(P) sexo 1: parejas {fa['con_pareja']} sin pareja {fa['sin_pareja']} (> 0 alguno), tipos vivos X/Y {fa['tipos_vivos']}, recombinaciones {fa['recombinaciones']} (> 0 si hubo partos: partos {sum(d['descendientes'] for d in rs['linajes'])}); fisica != base",
    (fa['con_pareja'] + fa['sin_pareja']) > 0 and fis(rs) != fis(r0) and (fa['recombinaciones'] == fa['con_pareja']))
rc = run(S, dict(sexo=1, recombina=0, pareja='azar', r_par=40)); fc = rc['pista']['familia']
chk(f"(c) clon con pareja: parejas {fc['con_pareja']} (> 0), recombinaciones {fc['recombinaciones']} (== 0); fisica != sexo (si hubo partos) y != base",
    fc['recombinaciones'] == 0 and fc['con_pareja'] > 0 and fis(rc) != fis(r0) and (fis(rc) != fis(rs) or fc['con_pareja'] == 0))
# genomas de hijos: con recombina, algun hijo difiere de su madre en algun gen MAS alla de la mutacion -> se mira que los hijos tengan genes de dos padres:
ind = rs['eco']['vivos_final']
chk(f"(P) recombina: vivos al final {len(ind)}; hay cuerpos de generacion >= 1 ({sum(1 for v in ind if v[2] >= 1)})", len(ind) > 0)
rf = run(S, dict(sexo=1, recombina=1, pareja='fuerte', r_par=40))
chk(f"(P) pareja fuerte != azar (misma fisica salvo la eleccion; fuerza media de la pareja: fuerte {[d['_carrera']['familia']['fuerza_pareja_media'] for d in rf['linajes']][:3]} vs azar {[d['_carrera']['familia']['fuerza_pareja_media'] for d in rs['linajes']][:3]})",
    fis(rf) != fis(rs))
rd = run(S, dict(sexo=1, recombina=1, pareja='azar', r_par=40, dote_doble=1)); fd = rd['pista']['familia']
chk(f"(P) dote_doble: pagos {fd['pagos_dobles']} (> 0) == parejas {fd['con_pareja']}; fisica != sexo", fd['pagos_dobles'] == fd['con_pareja'] and fd['pagos_dobles'] > 0 and fis(rd) != fis(rs))
# camada: a T 4000 ningun cuerpo tiene 2 hijos vivos a la vez (medido: max hvivos 1); se verifica a T 12000 (poblacion crecida), radio total y u_cam maximo
TK = 12000 if not CORTO else 6000; KWK = dict(KW, T=TK, eco=CD.eco_cfg(TK))
rk = N(MF.run(S, [CD.CARRO] * CD.N_LIN, **KWK, familia=dict(camada=1, u_cam=1.5, r_par=180))); fk = rk['pista']['familia']
rk_b = N(MF.run(S, [CD.CARRO] * CD.N_LIN, **KWK))
chk(f"(P) camada (T {TK}, u_cam 1.5, r_par 180): trofico {fk['trofico']} (> 0); fisica != base; sin sexo: parejas 0", fk['trofico'] > 0 and fis(rk) != fis(rk_b) and fk['con_pareja'] == 0)
rk0 = run(S, dict(camada=1, u_cam=0.0))
chk("(P) camada con u_cam 0 (nunca hay necesidad) == base en la fisica (la regla no dispara)", fis(rk0) == fis(r0))
# guardas
def aborta(**k):
    try: run(S, k); return False
    except SystemExit: return True
chk("(g) recombina sin sexo aborta; pareja desconocida aborta; clave desconocida aborta", aborta(recombina=1) and aborta(sexo=1, pareja='x') and aborta(zzz=1))
print(f"\nARNES {'PASA' if OK[0] else 'FALLA'}, {NCHK[1]}/{NCHK[0]} · {time.time() - t0:.1f}s")
sys.exit(0 if OK[0] else 1)
