"""identidad_g50.py — ARNES de 50 GENES (Opus G, 28-sep-2026). UN proceso. Salida: identidad_g50_salida.txt.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

(K) los tres archivos son los construidos por anclas (construye_g50 --verifica).
(A) BASE BIT A BIT: ING_F1, ING_SEL_C e ING_AZA_C en nucleo_g50 (gemelo motor_g50, genoma de 50) == los mismos en nucleo_eco_sel_ing
    (gemelo motor_frio_rapido, genoma de 18) en TODA la fisica y en los 18 genes viejos (las claves con forma de genoma se proyectan
    a sus 18 primeras columnas; tasa_mut se compara por n_mut). Con 15 mutables muta gasta los mismos 2*18 numeros.
(B) PERILLA APAGADA: ING_SEL_50, ING_AZA_50, ING_SEL_25 e ING_SEL_47 con p_mut = 0 == ING_F1 de la base (fisica).
(Z) CONTROL QUE PUEDE FALLAR: ING_SEL_50 con p_mut 0.05 != ING_F1; ING_AZA_50 != ING_SEL_50.
(U) CADA GEN NUEVO SE USA: con p_mut = 0 y el genoma inicial = G0 salvo UN gen nuevo en su piso (o techo si el piso es G0), la fisica
    difiere de G0 (T corto). Un gen que no cambie nada se DECLARA (no se esconde).
(M) muta de motor_eco50: sin genes nuevos mutables == motor_eco.muta en las 18 primeras (mismos numeros); con alguno, gasta 2*50.
(D) determinismo: ING_SEL_50 dos veces == bit a bit.
"""
import importlib.util, json, os, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
SALIDA = os.path.join(AQUI, 'identidad_g50_salida.txt')
TMP = os.path.join(AQUI, 'datos', 'arnes'); os.makedirs(TMP, exist_ok=True)
_out = open(SALIDA if '--sin-U' not in sys.argv else SALIDA.replace('.txt', '_brazos.txt'), 'w', encoding='utf-8')


def P(s):
    print(s, flush=True); _out.write(s + '\n'); _out.flush()


def carga(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m; spec.loader.exec_module(m); return m


sys.path.insert(0, AQUI)
import construye_g50 as CG
N0 = carga('nucleo_eco_sel_ing', os.path.join(EXP, 'organelos', 'eco_sel_ing', 'nucleo_eco_sel_ing.py'))
NG = carga('nucleo_g50', os.path.join(AQUI, 'nucleo_g50.py'))
import motor_eco50 as ME50
import motor_eco as ME18
OK = []; t00 = time.time()


def caso(nom, cond, det=''):
    OK.append(bool(cond)); P(f"  [{'OK' if cond else 'FALLA'}] {nom} {det}")


GEN_KEYS = {'sel_corte', 'genes', 'G0', 'vivos_final', 'gen_t', 'sel_100k', 'sel_T', 'corte', 'tasa_mut', 'seg', 'motor', 'genes_vivos_T'}


def proy(r):
    """Fisica + los 18 genes viejos."""
    d = {k: v for k, v in r.items() if k not in GEN_KEYS}
    d['genes'] = list(r['genes'])[:18]; d['G0'] = list(r['G0'])[:18]
    d['vivos_final'] = [list(v)[:4 + 18] for v in r['vivos_final']]
    g = []
    for f in r['gen_t']:
        f = list(f)
        for j in (4, 6):
            if f[j] is not None: f[j] = list(f[j])[:18]
        for j in (5, 7):
            if f[j] is not None: f[j] = [list(x)[:18] for x in f[j]]
        g.append(f)
    d['gen_t'] = g
    d['sel_100k'] = None if r['sel_100k'] is None else list(r['sel_100k'])[:18]
    d['sel_T'] = None if r['sel_T'] is None else list(r['sel_T'])[:18]
    d['sel_corte'] = None if r.get('sel_corte') is None else list(r['sel_corte'])[:18]
    c = r.get('corte')
    if c:
        c = dict(c)
        for k in ('med_vivos', 'med_banco', 'med_sombra_banco'):
            if c.get(k) is not None: c[k] = list(c[k])[:18]
        c['banco'] = [list(e)[:18] for e in c['banco']]
    d['corte'] = c
    d['genes_vivos_T'] = r.get('genes_vivos_T')
    return json.loads(json.dumps(d))


FIS = ('tam_total', 'n_nac', 'n_refund', 'K_nac', 'K_fund', 'fund_2a', 'n_k2', 'max_vivos', 'bloqueados', 'fundadores_rep', 'vivos_T',
       'r0_nac', 'nac_2a', 'causas_2a', 'vida_media_muertos_2a', 'persiste', 't_ext')


def fis(r):
    return json.loads(json.dumps({k: r.get(k) for k in FIS}))


def corre(N, brazo, seed, T, pm=None, genoma=None):
    N._PMUT[0] = pm
    if hasattr(N, '_GENOMA'): N._GENOMA[0] = {} if genoma is None else dict(genoma=genoma)
    try:
        return N.trabajo((seed, brazo, T, N.tc_de(brazo, T), N.FRIO['T_lect'], TMP, False))
    finally:
        N._PMUT[0] = None
        if hasattr(N, '_GENOMA'): N._GENOMA[0] = {}


P(f"[{time.strftime('%H:%M:%S')}] ARNES 50 GENES · construye {CG.h16(os.path.join(AQUI, 'construye_g50.py'))} · motor_eco50 "
  f"{CG.h16(os.path.join(AQUI, 'motor_eco50.py'))} · motor_g50 {CG.h16(os.path.join(AQUI, 'motor_g50.py'))} · nucleo_g50 "
  f"{CG.h16(os.path.join(AQUI, 'nucleo_g50.py'))}")
P("(K) construccion por anclas")
caso('construye_g50 --verifica', CG.main(['--verifica']))
caso('50 genes en motor_eco50', len(ME50.GENES) == 50, f"({len(ME50.GENES)}; nuevos {len(ME50.NOMBRES50)})")

P("(M) muta")
G0 = np.array([float(x) for x in range(1, 51)]) / 10.0; lo = G0 / 4; hi = G0 * 4
pv = np.zeros(50); pv[:18] = 1.0
h50, _ = ME50.muta(G0.copy(), np.random.default_rng(7), pv, 0.15, lo, hi)
h18, _ = ME18.muta(G0[:18].copy(), np.random.default_rng(7), pv[:18], 0.15, lo[:18], hi[:18])
caso('sin nuevos mutables: las 18 == motor_eco.muta', np.array_equal(h50[:18], h18) and np.array_equal(h50[18:], G0[18:]))
r1 = np.random.default_rng(7); pv2 = pv.copy(); pv2[30] = 1.0; ME50.muta(G0.copy(), r1, pv2, 0.15, lo, hi)
r2 = np.random.default_rng(7); r2.random(50); r2.normal(0, 0.15, 50)
caso('con un nuevo mutable gasta 2*50 numeros', r1.random() == r2.random())

T = 30000; S = N0.PRACTICA[0]
P(f"(A) base bit a bit (semilla {S}, T {T})")
N0.usa_gemelo()
B = {b: corre(N0, b, S, T) for b in N0.ING}
NG.usa_gemelo()
G = {b: corre(NG, b, S, T) for b in N0.ING}
for b in N0.ING:
    a, c = proy(B[b]), proy(G[b])
    dif = sorted(k for k in set(a) | set(c) if a.get(k) != c.get(k))
    caso(f'{b}: nucleo_g50 == nucleo_eco_sel_ing', not dif and B[b]['persiste'] is not None,
         f"(claves distintas {dif[:6]}; n_nac {B[b]['n_nac']}; n_mut {B[b].get('n_mut')}; K_nac {B[b].get('K_nac')}; motor {G[b].get('motor')})")
caso('control: ING_SEL_C != ING_F1 en la base (la mutacion hace algo)', fis(B['ING_SEL_C']) != fis(B['ING_F1']))

P("(V) vivero finito (t_corte 20 000 < T 30 000): ING_SEL_C_V de nucleo_g50 == ING_SEL_C de la base con el mismo t_corte; SEL_47_V p0 == SEL_C_V p0")
N0.usa_gemelo()
bv = N0.trabajo((S, 'ING_SEL_C', T, 20000, N0.FRIO['T_lect'], TMP, False))
NG.usa_gemelo()
gv = NG.trabajo((S, 'ING_SEL_C_V', T, 20000, NG.FRIO['T_lect'], TMP, False))
dif = sorted(k for k in set(proy(bv)) | set(proy(gv)) if proy(bv).get(k) != proy(gv).get(k) and k not in ('brazo',))
caso('ING_SEL_C_V == base ING_SEL_C (t_corte 20 000)', not dif, f"(distintas {dif[:6]}; persiste {bv['persiste']}; t_ext {bv['t_ext']})")
NG._PMUT[0] = 0.0
v47 = NG.trabajo((S, 'ING_SEL_47_V', T, 20000, NG.FRIO['T_lect'], TMP, False)); vc = NG.trabajo((S, 'ING_SEL_C_V', T, 20000, NG.FRIO['T_lect'], TMP, False))
NG._PMUT[0] = None
caso('ING_SEL_47_V p_mut 0 == ING_SEL_C_V p_mut 0', fis(v47) == fis(vc))
caso('el vivero finito corta (t_corte 20 000 en la salida)', gv['t_corte'] == 20000)
P("(B) perilla apagada: p_mut 0 == ING_F1 de la base")
for b in ('ING_SEL_50', 'ING_AZA_50', 'ING_SEL_25', 'ING_SEL_47', 'ING_AZA_47'):
    r = corre(NG, b, S, T, pm=0.0)
    caso(f'{b} p_mut 0 == ING_F1', fis(r) == fis(B['ING_F1']), f"(n_nac {r['n_nac']} vs {B['ING_F1']['n_nac']})")

P("(Z) controles que pueden fallar")
s50 = corre(NG, 'ING_SEL_50', S, T); a50 = corre(NG, 'ING_AZA_50', S, T)
caso('ING_SEL_50 (p 0.05) != ING_F1', fis(s50) != fis(B['ING_F1']), f"(mutables {len(s50['mutables'])}; n_mut {s50['n_mut']})")
caso('ING_AZA_50 != ING_SEL_50', fis(a50) != fis(s50))
s47 = corre(NG, 'ING_SEL_47', S, T); a47 = corre(NG, 'ING_AZA_47', S, T)
caso('ING_AZA_47 != ING_SEL_47', fis(a47) != fis(s47), f"(mutables {len(a47['mutables'])}, donante {a47['donante']})")
caso('ING_SEL_47: 47 mutables y 0 fuera (dote, rep_umbral, rep_X quietos)', s47['fuera_mutables'] == 0 and len(s47['mutables']) == 47)
caso('ING_SEL_50: 0 genes fuera de los mutables', s50['fuera_mutables'] == 0)

P("(D) determinismo")
s50b = corre(NG, 'ING_SEL_50', S, T)
caso('ING_SEL_50 dos veces == bit a bit', json.dumps(s50, sort_keys=True, default=str) == json.dumps({**s50b, 'seg': s50['seg']}, sort_keys=True, default=str))

TU = 20000
SIN_U = '--sin-U' in sys.argv   # (U) ya corrio entero con el MISMO motor_g50 (32f9e5dd4ddd20dd); los cambios posteriores son solo brazos del nucleo
if SIN_U: P('(U) OMITIDO en esta corrida (--sin-U): ver la corrida entera anterior, mismo motor_g50 32f9e5dd4ddd20dd: 31/32 cambian, clip_kw mudo')
P(f"(U) cada gen nuevo se usa (p_mut 0; genoma inicial = G0 con UN gen en su piso o techo; T {TU}, semilla {S})")
CF = __import__('pista2').cfg_fabrica()
g0 = ME50.genoma0(CF); LO, HI = ME50.rangos(g0)
ref = None if SIN_U else fis(corre(NG, 'ING_SEL_50', S, TU, pm=0.0))
mudos = []
for nom in ([] if SIN_U else ME50.NOMBRES50):
    j = ME50.NOMBRES.index(nom); gg = g0.copy()
    gg[j] = LO[j] if LO[j] < g0[j] else HI[j]
    r = corre(NG, 'ING_SEL_50', S, TU, pm=0.0, genoma=gg)
    cambia = fis(r) != ref
    if not cambia:   # declarado: un gen de tope (clip) puede no tocarse en 20 000 pasos; se repite a 100 000 antes de llamarlo mudo
        r = corre(NG, 'ING_SEL_50', S, 100000, pm=0.0, genoma=gg)
        cambia = fis(r) != fis(corre(NG, 'ING_SEL_50', S, 100000, pm=0.0))
        P(f'    ({nom}: igual a T {TU}; a T 100 000: {"CAMBIA" if cambia else "IGUAL"})')
    if not cambia: mudos.append(nom)
    P(f"    {nom:14s} G0 {g0[j]:<8g} -> {gg[j]:<8g} fisica {'CAMBIA' if cambia else 'IGUAL'} (n_nac {r['n_nac']} vs {ref['n_nac']}; K_nac {r['K_nac']})")
if not SIN_U: caso('los 32 genes nuevos cambian la fisica', not mudos, f"(mudos: {mudos})")

P(f"RESUMEN: {sum(OK)}/{len(OK)} en {round(time.time() - t00)} s")
_out.close()
