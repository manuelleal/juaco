"""identidad_eco_rapido.py — ARNES del GEMELO COMPILADO de JUACO-ECO (motor_eco_rapido.py). Un proceso, sin Pool.

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Un gemelo que no sea BIT A BIT identico SOLO EXPLORA, nunca confirma (regla 9 de registro/EQUIPO.md).

QUE SE COMPARA (gemelo contra motor_eco.run_solapadas, el original, en el mismo proceso):
  (0) ORIGEN: sha de motor_eco / FABRICA_ECO / FABRICA / pista2 == los fijados en el gemelo.
  (P) PRIMITIVAS delegadas: bucle np.exp == np.exp; BLAS de numba == BLAS de NumPy (90.90 denso y 0/1, 6.6, 90x6@6, 2x9@9);
      metodos de Generator (normal, random, integers, uniform, permutation) == NumPy; suma de 6; top-3 con y SIN empate
      (el empate va a np.argsort). Con dos CONTROLES que deben fallar: libm != np.exp y suma ingenua != BLAS en esta maquina.
  (I) E1 eco=None (pista v2, cerebro FABRICA / FABRICA_ECO), varias configuraciones x varias semillas. En CADA corrida:
      salida COMPLETA (todas las claves, json), TRAYECTORIA (cada actua de cada cuerpo en cada paso: t, linaje, pos, E, Ag,
      mov, muerde), PESOS (cerebro ENTERO de cada cuerpo vivo al final, bit a bit: Wl, el, tr, KW, activa, Wp, Wn, Wps, Wns,
      err, mu, mup, mun, zp, zn, contadores, codigos, rechazo vigente, estado de SU Generator) y el MUNDO final en orden.
  (E) E2 eco=dict(...): genoma por cuerpo, mutacion, sombras, banco, vivero, corte, refunda=0, VIDA/CEREBRO/AZAR/MUT0,
      genoma explicito NO entero, ind_cb (filas + genoma). Lo mismo que (I) + las filas de individuos.
  (C) CHECKPOINT: estado COMPLETO del original (su pickle) == estado del gemelo (su pickle) en t = 1000, 2000, 3000 (todos
      los cuerpos, cerebros, genomas, sombras, mundo, rng, banco, contadores); gemelo cortado y reanudado == original seguido;
      firma distinta y formatos cruzados abortan.
  (X) EL MUNDO DE LA SERIE (esc = 90, 90 FABRICA_ECO, tope 3000, muestra 1000): VIDA y AZAR, salida completa.
  (J) corre_eco SIN cambiar su letra (corre_eco_rapido): juez (bateria esc = 9, T_b = 20000) y trabajo() (vivero + corte +
      checkpoint en 10000 + juez) == original; trabajo cortado tras el checkpoint y reanudado == seguido.
  (K) CONTROLES que DEBEN fallar: semilla vecina; gemelo con exp de libm; con suma ingenua; con turno fijo; VIDA vs MUT0;
      AZAR vs VIDA; inmediata vs fija.
  (G) GUARDIAS del original (mismos mensajes) y del gemelo (lo que no compila aborta).
  (D) DETERMINISMO.  (Z) CACHE: un proceso NUEVO carga la cache de numba (0 fallos de cache) y reproduce 3 corridas.
  (V) ACELERACION (pasos/s del original y del gemelo en el MISMO mundo, con el numero medio de cuerpos).
Uso: /root/venv-juaco/bin/python experimentos/juaco_eco/identidad_eco_rapido.py   (escribe identidad_eco_rapido_salida.txt;
     la ultima linea es RESULTADO: N/N)
"""
import json, os, pickle, shutil, subprocess, sys, tempfile, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')]
import motor_eco as ME
import pista2 as P
import motor_eco_rapido as MR
import corre_eco as CR

N = lambda x: json.dumps(x, default=str, sort_keys=True)
OK = [0, 0]
SAL = open(os.path.join(AQUI, 'identidad_eco_rapido_salida.txt'), 'w', encoding='utf-8')
T00 = time.time()


def out(s=''):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def di(et, ok, extra=''):
    OK[1] += 1; OK[0] += int(bool(ok))
    out(f"  [{'OK ' if ok else 'FALLA'}] ({OK[1]}) {et}{(' · ' + extra) if extra else ''}")


def seccion(s):
    out(f"{s}   [{time.strftime('%H:%M:%S')}, {round(time.time() - T00)} s]")


def aborta(f):
    try: f()
    except SystemExit as e: return 'SystemExit: ' + str(e)
    except ValueError as e: return 'ValueError: ' + str(e)
    return None


FAB = P.carga_carro('FABRICA'); FE = ME.carga_eco('FABRICA_ECO')
CF = P.cfg_fabrica(); G0 = ME.genoma0(CF); LO, HI = ME.rangos(G0)
HX = lambda a: np.ascontiguousarray(a).tobytes().hex()
EST = lambda r: r.bit_generator.state


# ================================================================ el carro ESPIA (misma conducta; registra instancias y actua)
class Registro:
    def __init__(self): self.REG = []; self.TRZ = []; self.vista = None


def espia(base, reg):
    class Carro(base.Carro):
        def actua(self, obs):
            if reg.vista is None: reg.vista = obs['objs']
            a = base.Carro.actua(self, obs)
            reg.TRZ.append((obs['t'], self._lin_espia, obs['pos'], obs['E'], obs['Ag'], int(a['mov']), int(bool(a['muerde']))))
            return a

    class Mod:
        __file__ = base.__file__

        @staticmethod
        def crea(ctx):
            c = Carro(ctx); c._lin_espia = ctx['indice']; reg.REG.append((ctx['id'], ctx['indice'], c)); return c
    return Mod


def carros_espia(carros, reg, eco):
    """Las mismas etiquetas (mismos ids) con el carro espia."""
    res = []
    for c in carros:
        e, m = (c, (P.carga_carro(c) if eco is None else ME.carga_eco(c))) if isinstance(c, str) else c
        res.append((e, espia(m, reg)))
    return res


# ================================================================ cerebros y estados canonicos
def cerebro_orig(c, t):
    return dict(Wl=HX(c.Wl), el=HX(c.el), tr=HX(c.tr), KW=HX(c.KW), activa=HX(c.activa), Wp=HX(c.Wp), Wn=HX(c.Wn),
                Wps=HX(c.Wps), Wns=HX(c.Wns), err=HX(c.err), mu=HX(c.mu), mup=HX(c.mup), mun=HX(c.mun), zp=HX(c.zp), zn=HX(c.zn),
                splits=c.splits, split_t=[list(x) for x in c.split_t], err_max=float(c.err_max), t_conflicto=c.t_conflicto,
                t_techo=c.t_techo, n_techo=c.n_techo, gpa=c._gpa, gpn=c._gpn, na=int(c._na), nm=int(c._nm), R=float(c._R),
                Rp=float(c._Rp), hambre=float(c._hambre), sin_objetivo=list(c.sin_objetivo),
                ncod=[[sorted(k), v] for k, v in c.ncod.items()], rech=sorted((x, v) for x, v in c._rech.items() if v >= t),
                rng=EST(c.rng))


def cerebro_gem(st, s, t):
    bi = st['bi'][s]; bf = st['bf'][s]; b = MR.NKMAX + 1
    ncod = [[sorted([int(k) // (b * b) - 1, (int(k) // b) % b - 1, int(k) % b - 1]), int(v)]
            for k, v in zip(st['nck'][s][:bi[MR.I_NCN]], st['ncc'][s][:bi[MR.I_NCN]])]
    return dict(Wl=HX(st['Wl'][s]), el=HX(st['el'][s]), tr=HX(st['tr'][s]), KW=HX(st['KW'][s]), activa=HX(st['act'][s]),
                Wp=HX(st['Wp'][s]), Wn=HX(st['Wn'][s]), Wps=HX(st['Wps'][s]), Wns=HX(st['Wns'][s]), err=HX(st['err'][s]),
                mu=HX(st['mu'][s]), mup=HX(st['mup'][s]), mun=HX(st['mun'][s]), zp=HX(st['zp'][s]), zn=HX(st['zn'][s]),
                splits=int(bi[MR.I_SPL]), split_t=[[int(st['stt'][s][i]), P.TIPOS[int(st['stk'][s][i])]] for i in range(bi[MR.I_NST])],
                err_max=float(bf[MR.F_ERRMAX]), t_conflicto=(None if bi[MR.I_TCON] < 0 else int(bi[MR.I_TCON])),
                t_techo=(None if bi[MR.I_TTEC] < 0 else int(bi[MR.I_TTEC])), n_techo=int(bi[MR.I_NTEC]), gpa=int(bi[MR.I_GPA]),
                gpn=int(bi[MR.I_GPN]), na=int(bi[MR.I_NA]), nm=int(bi[MR.I_NM]), R=float(bf[MR.F_R]), Rp=float(bf[MR.F_RP]),
                hambre=float(bf[MR.F_HAMB]), sin_objetivo=[int(bi[MR.I_SO0 + q]) for q in range(4)], ncod=ncod,
                rech=sorted((int(x), int(v)) for x, v in zip(st['rpos'][s][:bi[MR.I_RN]], st['rexp'][s][:bi[MR.I_RN]]) if v >= t),
                rng=EST(st['GL'][int(s)]))


def mundo_gem(st):
    wi = st['wi']
    return [(int(st['seqpos'][q]), P.TIPOS[int(st['grid'][st['seqpos'][q]])]) for q in range(int(wi[MR.W_NSEQ])) if st['seqpos'][q] >= 0]


def es_canon(ES):
    d = {k: v for k, v in ES.items() if k != 'banco'}
    d['banco'] = [[HX(g), HX(s)] for g, s in ES['banco']]
    return d


def canon_orig(blob):
    st = pickle.loads(blob); t = st['t']
    cs = []
    for b in st['cuerpos']:
        cs.append(dict(lin=b.lin, k=b.k, gen=b.gen, padre=b.padre, tn=b.tn, pos=b.pos, E=float(b.E), Ag=float(b.Ag), gv=b.gv,
                       tB=b.tB, tD=b.tD, vol={None: -1, 'B': 1, 'D': 3}[b.vol_kk], hijos=b.hijos, fund=b.fund,
                       g=HX(b.g), s=HX(b.s), cerebro=cerebro_orig(b.c, t)))
    lin = [dict(mord=l.mord, vis=l.vis, deaths=l.deaths, mnec=l.mnec, causas=l.causas, mvol=l.muertes_vol, fund=l.fund,
                tfund=l.tfund, desc=l.desc, nac=l.nac, bloq=l.bloq, vidas=l.vidas, ind=l.ind, vivos=l.vivos, tam=l.tam, pv=l.pv)
           for l in st['lin']]
    return dict(t=t, cuerpos=cs, mundo=list(st['objs'].items()), rng=EST(st['rng']), pista=EST(st['rng_pista']),
                fund=[EST(r) for r in st['rngs_fund']], muerte=[EST(r) for r in st['rngs_muerte']], quimio=st['banco'][0],
                pisos=st['pisos'][0], llegadas=st['llegadas'][0], perdidas=st['perdidas'][0], olv=st['olv_n'], comp=st['comp'],
                nsuma=st['nobj_suma'], total=st['total'], maxv=st['max_vivos'], ttope=st['t_tope'], tamtot=st['tam_total'],
                lin=lin, ES=es_canon(st['ES']))


def canon_gem(blob, muestra):
    B = pickle.loads(blob); st = B['st']; t = B['t']; wi = st['wi']; li = st['li']
    nsamp = (t - 1) // muestra + 1
    cs = []
    for s in [int(x) for x in st['cuer'][:wi[MR.W_NCUER]]]:
        bi = st['bi'][s]; bf = st['bf'][s]
        cs.append(dict(lin=int(bi[MR.I_LIN]), k=int(bi[MR.I_K]), gen=int(bi[MR.I_GEN]), padre=int(bi[MR.I_PADRE]),
                       tn=int(bi[MR.I_TN]), pos=int(bi[MR.I_POS]), E=float(bf[MR.F_E]), Ag=float(bf[MR.F_AG]), gv=int(bi[MR.I_GV]),
                       tB=int(bi[MR.I_TB]), tD=int(bi[MR.I_TD]), vol=int(bi[MR.I_VOL]), hijos=int(bi[MR.I_HIJ]),
                       fund=int(bi[MR.I_FUND]), g=HX(st['G'][s]), s=HX(st['SH'][s]), cerebro=cerebro_gem(st, s, t)))
    lin = []
    for i in range(li.shape[0]):
        lv = li[i]
        lin.append(dict(mord={x: [int(v) for v in st['mord'][i, j]] for j, x in enumerate(P.TIPOS)},
                        vis={x: [int(v) for v in st['vis'][i, j]] for j, x in enumerate(P.TIPOS)},
                        deaths=int(lv[MR.L_DEATHS]), mnec=[int(lv[MR.L_MN0]), int(lv[MR.L_MN1])],
                        causas={x: int(lv[MR.L_CZ0 + j]) for j, x in enumerate(ME.CAUSAS)}, mvol=int(lv[MR.L_MVOL]),
                        fund=int(lv[MR.L_FUND]), tfund=[int(x) for x in st['tfund'][i, :lv[MR.L_NTF]]], desc=int(lv[MR.L_DESC]),
                        nac=int(lv[MR.L_NAC]), bloq=int(lv[MR.L_BLOQ]), vidas=B['lin_py'][i]['vidas'], ind=B['lin_py'][i]['ind'],
                        vivos=int(lv[MR.L_VIVOS]), tam=[int(x) for x in st['tam'][:nsamp, i]], pv=int(lv[MR.L_PV])))
    return dict(t=t, cuerpos=cs, mundo=mundo_gem(st), rng=EST(st['rng']), pista=EST(st['rng_pista']),
                fund=[EST(r) for r in st['FUND']], muerte=[EST(r) for r in st['MUE']], quimio=float(st['wf'][0]),
                pisos=int(wi[MR.W_PISOS]), llegadas=int(wi[MR.W_LLEG]), perdidas=int(wi[MR.W_PERD]), olv=int(wi[MR.W_OLV]),
                comp={x: int(wi[MR.W_COMP0 + j]) for j, x in enumerate(P.TIPOS)}, nsuma=int(wi[MR.W_NSUMA]),
                total=int(wi[MR.W_TOTAL]), maxv=int(wi[MR.W_MAXV]), ttope=(None if wi[MR.W_TTOPE] < 0 else int(wi[MR.W_TTOPE])),
                tamtot=[int(x) for x in st['tamtot'][:nsamp]], lin=lin, ES=es_canon(B['ES']))


def claves_distintas(a, b):
    d = [k for k in sorted(set(a) | set(b)) if k not in ('linajes', 'pista', 'eco') and N(a.get(k)) != N(b.get(k))]
    d += ['pista.' + k for k in sorted(set(a['pista']) | set(b['pista'])) if N(a['pista'].get(k)) != N(b['pista'].get(k))]
    for i, (la, lb) in enumerate(zip(a['linajes'], b['linajes'])):
        d += [f'lin{i}.{k}' for k in sorted(set(la) | set(lb)) if N(la.get(k)) != N(lb.get(k))]
    if 'eco' in a or 'eco' in b:
        ea, eb = a.get('eco', {}), b.get('eco', {})
        d += ['eco.' + k for k in sorted(set(ea) | set(eb)) if N(ea.get(k)) != N(eb.get(k))]
    return d


def compara(et, seed, carros, kw, eco=None, modo=None, filas=True):
    """UNA corrida: original (con el carro espia) contra gemelo (con el carro real). Salida, filas ind_cb, trayectoria,
    cerebros de los vivos al final y mundo final. Devuelve (dict de igualdades, info, salida original, tiempos)."""
    reg = Registro(); fo, fg = [], []
    eo = eg = None
    if eco is not None:
        eo = dict(eco); eg = dict(eco)
        if filas:
            eo['ind_cb'] = lambda li, row, g: fo.append((li, list(row), HX(g)))
            eg['ind_cb'] = lambda li, row, g: fg.append((li, list(row), HX(g)))
    t0 = time.time(); a = ME.run_solapadas(seed, carros_espia(carros, reg, eco), eco=eo, **kw); ta = time.time() - t0
    trz = []; fin = {}
    t0 = time.time(); b = MR.run_solapadas(seed, carros, eco=eg, _traza=trz, _modo=modo, _estado_final=fin, **kw); tb = time.time() - t0
    st = fin['st']; T = kw['T']; tfin = fin['t']
    dif = claves_distintas(a, b)
    # cerebros de los vivos al final (espia: el ultimo fundador de cada linaje o el hijo '<id>/<k>')
    ids = a['pista']['ids']; porid = {}
    for ident, i, c in reg.REG: porid[(i, ident)] = c
    malos = []; nviv = 0
    for s in fin['vivos']:
        i = int(st['bi'][s, MR.I_LIN]); k = int(st['bi'][s, MR.I_K]); fu = int(st['bi'][s, MR.I_FUND])
        c = porid.get((i, ids[i] if fu else f"{ids[i]}/{k}"))
        nviv += 1
        if c is None or N(cerebro_orig(c, tfin)) != N(cerebro_gem(st, s, tfin)): malos.append((i, k))
    res = dict(salida=not dif, filas=(N(fo) == N(fg)), traza=(N(reg.TRZ) == N(trz)), cerebros=not malos,
               mundo=(N(list(reg.vista.items())) == N(mundo_gem(st))))
    info = dict(dif=dif[:5], malos=malos[:4], nviv=nviv, ntraza=len(trz), ties=int(st['wi'][MR.W_NTIES]),
                mv=a['pista']['max_vivos'], muertes=sum(l['deaths'] for l in a['linajes']),
                nac=sum(l['descendientes'] for l in a['linajes']), pisos=a['pista']['pisos'], bloq=a['pista']['bloqueados'],
                splits=sum(l['carro'].get('splits', 0) for l in a['linajes']), filas=len(fo))
    return res, info, a, (ta, tb)


def reporta(et, res, info, tt, eco=False):
    ok = all(res.values())
    ext = (f"salida {'=' if res['salida'] else '!='} · traza {info['ntraza']} actua {'=' if res['traza'] else '!='} · "
           f"cerebros {info['nviv']} vivos {'=' if res['cerebros'] else '!='} · mundo {'=' if res['mundo'] else '!='}"
           + (f" · filas {info['filas']} {'=' if res['filas'] else '!='}" if eco else '')
           + f" · max_vivos {info['mv']} muertes {info['muertes']} partos {info['nac']} divisiones {info['splits']}"
           + (f" pisos {info['pisos']}" if info['pisos'] else '') + (f" bloqueados {info['bloq']}" if info['bloq'] else '')
           + (f" empates {info['ties']}" if info['ties'] else '')
           + f" · {tt[0]:.1f} s / {tt[1]:.2f} s" + ('' if ok else f" · DIFIERE {info['dif']} {info['malos']}"))
    di(et, ok, ext)


# ================================================================================================ (0)
seccion('(0) ORIGEN (sha fijados en el gemelo)')
for p, h in MR.SHA.items():
    di(f"{os.path.relpath(p, RAIZ)} sha {h}", MR._h16(p) == h)

# ================================================================================================ (P)
seccion('(P) PRIMITIVAS delegadas a NumPy (y dos controles que deben fallar)')
rng = np.random.default_rng(424242)
xs = np.concatenate([rng.uniform(-40, 40, 500000), rng.normal(0, 2, 500000)])
ref = np.exp(xs); B = MR._bufs_exp(); got = np.empty_like(xs)
for i in range(xs.size):
    got[i] = MR._exp1(xs[i], MR.EXP_LOOP, B[0], B[1], B[3], B[5], 0)
di("exp del gemelo (bucle 1-D de np.exp por ctypes) == np.exp, 1 000 000 argumentos", np.array_equal(ref.view(np.int64), got.view(np.int64)))
libm = np.array([MR._exp1(x, MR.EXP_LOOP, B[0], B[1], B[3], B[5], 1) for x in xs[:200000]])
nd = int((libm.view(np.int64) != ref[:200000].view(np.int64)).sum())
di("CONTROL (debe fallar): exp de libm != np.exp en esta maquina", nd > 0, f"distintos {nd}/200000 ({100 * nd / 200000:.2f} %)")
malos = 0; nd_ing = 0
for rep in range(100000):
    a = rng.normal(0, 1, 90); b = rng.normal(0, 1, 90)
    if float(a @ b) != MR._dot(a, b, 90, 0): malos += 1
    if float(a @ b) != MR._dot(a, b, 90, 1): nd_ing += 1
    k3 = np.zeros(90); k3[rng.choice(90, 3, replace=False)] = 1.0
    if float(a @ k3) != MR._dot(a, k3, 90, 0): malos += 1
    c6 = rng.uniform(0, 2, 6); d6 = rng.uniform(0, 1, 6)
    if float(c6 @ d6) != MR._dot(c6, d6, 6, 0): malos += 1
di("BLAS de numba == BLAS de NumPy (ddot 90 denso, ddot 90 con 3 unos, ddot 6), 300 000 casos", malos == 0, f"distintos {malos}")
di("CONTROL (debe fallar): suma de izquierda a derecha != ddot de BLAS (90 denso)", nd_ing > 0, f"distintos {nd_ing}/100000")


def mv(A, x): return A @ x


from numba import njit
mv_nb = njit(mv)
malos = 0
for rep in range(50000):
    A = rng.uniform(0, 1, (90, 6)); x = rng.uniform(0, 1, 6)
    if not np.array_equal(A @ x, mv_nb(A, x)): malos += 1
    A2 = rng.uniform(0, 1.5, (2, 9)); x2 = rng.uniform(0, 1.5, 9)
    if not np.array_equal(A2 @ x2, mv_nb(A2, x2)): malos += 1
di("BLAS de numba == BLAS de NumPy (dgemv 90x6 @ 6 y 2x9 @ 9), 100 000 casos", malos == 0, f"distintos {malos}")


@njit
def _gen_nb(r, n, L, k, sig):
    acc = []
    for i in range(n):
        p = r.permutation(k + (i % 7)); acc.append(float(p.sum()) + p[0] * 1000.0)
        acc.append(float(r.integers(0, L))); acc.append(float(r.integers(0, 4))); acc.append(r.random())
        z = r.normal(0, .3, 2); acc.append(z[0]); acc.append(z[1])
        u = r.uniform(.1, .4, (2, 9)); acc.append(u[1, 8]); v = r.uniform(0, 1, (7, 6)); acc.append(v[6, 5])
        rr = r.random(18); acc.append(rr[17]); zz = r.normal(0.0, sig, 18); acc.append(zz[17])
    return acc


def _gen_py(r, n, L, k, sig):
    acc = []
    for i in range(n):
        p = r.permutation(k + (i % 7)); acc.append(float(p.sum()) + p[0] * 1000.0)
        acc.append(float(int(r.integers(L)))); acc.append(float(int(r.integers(4)))); acc.append(r.random())
        z = r.normal(0, .3, 2); acc.append(z[0]); acc.append(z[1])
        u = r.uniform(.1, .4, (2, 9)); acc.append(u[1, 8]); v = r.uniform(0, 1, (7, 6)); acc.append(v[6, 5])
        rr = r.random(18); acc.append(rr[17]); zz = r.normal(0.0, sig, 18); acc.append(zz[17])
    return acc


malos = 0
for s in range(20):
    for L in (40, 360, 3600, 36000):
        a1 = np.random.default_rng([s, 0, 11, 0]); a2 = np.random.default_rng([s, 0, 11, 0])
        if _gen_nb(a1, 200, L, 2 + s, 0.15) != _gen_py(a2, 200, L, 2 + s, 0.15) or EST(a1) != EST(a2): malos += 1
di("Generator en numba (permutation, integers, random, normal, uniform) == NumPy: flujo y estado final, 80 flujos", malos == 0, f"distintos {malos}")
M6 = rng.uniform(0, 1, (200000, 6)) * rng.uniform(0.001, 1, (200000, 1)); malos = 0
for r6 in M6:
    acc = 0.0
    for v in r6: acc += v
    malos += int(acc != r6.sum())
di("suma de 6 (mu[c].sum()) de izquierda a derecha desde 0.0 == NumPy, 200 000 filas", malos == 0, f"distintos {malos}")
# top-3 del codigo de Kenyon, con y sin empate (el empate lo decide np.argsort por objmode)
PATM = np.array([CF['PAT'][x] for x in P.TIPOS], float)
KWt = np.zeros((1, MR.NKMAX, 6)); act = np.zeros((1, MR.NKMAX), np.bool_); cc = np.zeros((1, 4, 3), np.int64)
cv = np.zeros((1, 4), np.bool_); wb = np.zeros(MR.NKMAX); wit = np.zeros(MR.NWI, np.int64)
malos = 0; nemp = 0
for rep in range(40000):
    nk = int(rng.integers(8, 91)); KWt[:] = 0; act[:] = False
    KWt[0, :nk] = rng.uniform(0, 1, (nk, 6)); act[0, :nk] = True
    if rep % 2:   # EMPATES forzados: filas copiadas (el top-3 queda ambiguo en la frontera)
        src = rng.integers(0, nk, 4); dst = rng.integers(0, nk, 4); KWt[0, dst] = KWt[0, src]
        if rep % 4 == 1: KWt[0, :nk] = np.round(KWt[0, :nk], 1)
    p = int(rng.integers(0, 4)); cv[:] = False; e0 = int(wit[MR.W_NTIES])
    MR._code3(0, p, KWt, act, PATM, cc, cv, wb, 0, wit)
    v = np.where(act[0], KWt[0] @ PATM[p], -1e9)
    if sorted(cc[0, p]) != sorted(int(z) for z in np.argsort(v)[-3:]): malos += 1
    nemp += int(wit[MR.W_NTIES]) - e0
di("codigo de Kenyon: top-3 del gemelo == set(np.argsort(...)[-3:]) del original, 40 000 casos", malos == 0 and nemp > 100,
   f"distintos {malos}; con empate en la frontera (a NumPy por objmode) {nemp}")

# ================================================================================================ (I)
seccion('(I) E1: eco=None (pista v2 + FABRICA / FABRICA_ECO): salida + trayectoria + pesos + mundo')
CASOS_I = [('9 FABRICA fija T=3000', s, ['FABRICA'] * 9, dict(T=3000)) for s in (10001, 10002, 10003, 10004, 10005)]
CASOS_I += [
    ('9 FABRICA_ECO (tupla) T=3000', 10021, [('FABRICA_ECO', FE)] * 9, dict(T=3000)),
    ('9 FABRICA_ECO (tupla) T=3000', 10022, [('FABRICA_ECO', FE)] * 9, dict(T=3000)),
    ('9 FABRICA inmediata T=2000', 10023, ['FABRICA'] * 9, dict(T=2000, reposicion='inmediata')),
    ('9 FABRICA inmediata T=2000', 10024, ['FABRICA'] * 9, dict(T=2000, reposicion='inmediata')),
    ('9 FABRICA mundo_n=5 (esc < n)', 10025, ['FABRICA'] * 9, dict(T=2500, mundo_n=5)),
    ('3 FABRICA mundo_n=9 (esc > n)', 10026, ['FABRICA'] * 3, dict(T=4000, mundo_n=9)),
    ('3 FABRICA mundo_n=9 (esc > n)', 10027, ['FABRICA'] * 3, dict(T=4000, mundo_n=9)),
    ('9 FABRICA rep_acum=1', 10028, ['FABRICA'] * 9, dict(T=3000, rep_acum=1)),
    ('9 FABRICA tope 10 (bloqueados)', 10029, ['FABRICA'] * 9, dict(T=3000, tope_cuerpos=10)),
    ('9 FABRICA muestra 37', 10030, ['FABRICA'] * 9, dict(T=2000, muestra=37)),
    ('9 FABRICA r_rep 0.002 (pisos)', 10031, ['FABRICA'] * 9, dict(T=3000, r_rep=0.002)),
    ('1 FABRICA (n = 1: turno sin permutacion)', 10032, ['FABRICA'], dict(T=8000)),
    ('3 FABRICA escala=0 (L = 40)', 10033, ['FABRICA'] * 3, dict(T=3000, escala=0)),
    ('etiquetas mezcladas FABRICA / FABRICA_ECO', 10034, [('FABRICA', FAB), ('FABRICA_ECO', FE), 'FABRICA'], dict(T=3000)),
    ('9 FABRICA T=15000 (vida larga: divisiones)', 10035, ['FABRICA'] * 9, dict(T=15000)),
]
SALIDAS = {}
for et, s, car, kw in CASOS_I:
    res, info, a, tt = compara(et, s, car, dict(kw, diag=0))
    reporta(f"{et} s{s}", res, info, tt)
    SALIDAS[(et, s)] = a
reg = Registro()
a0 = ME.run_solapadas(10001, ['FABRICA'] * 9, T=3000, diag=0)
a1 = ME.run_solapadas(10001, carros_espia(['FABRICA'] * 9, reg, None), T=3000, diag=0)
di("el carro espia es INERTE (original con espia == original sin espia)", N(a0) == N(a1))

# ================================================================================================ (E)
seccion('(E) E2: eco=dict(...): genoma, mutacion, sombras, banco, vivero, corte, refunda, brazos, ind_cb')
rg = np.random.default_rng(77)
GX = np.array([rg.uniform(LO[j], HI[j]) for j in range(len(G0))])   # genoma explicito NO entero (NK, memoria_rechazo, rep_X con decimales)
KWM = dict(T=6000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500)
CASOS_E = [
    ('eco refunda=1 con G0', (10005, 10041), ['FABRICA_ECO'] * 9, dict(T=3000, diag=0), dict(refunda=1)),
    ('+ 8 sombras, cada_gen 500, banco 50', (10005, 10042), ['FABRICA_ECO'] * 9, dict(T=3000, diag=0), dict(refunda=1, n_sombra=8, cada_gen=500, banco=50)),
    ('(M) p_mut 0.2, 4 sombras, banco 100', (10006, 10043), ['FABRICA_ECO'] * 18, KWM, dict(refunda=1, p_mut=0.2, n_sombra=4, cada_gen=1000, banco=100)),
    ('(M) mutables = alpha, eta_s', (10007, 10044), ['FABRICA_ECO'] * 18, KWM, dict(refunda=1, p_mut=0.2, n_sombra=4, cada_gen=1000, banco=100, mutables=('alpha', 'eta_s'))),
    ('(R) refunda=0: si todo muere, muere', (10008, 10045), ['FABRICA_ECO'] * 9, dict(T=6000, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=100), dict(refunda=0)),
    ('(V) vivero y corte en 3000', (10009, 10046), ['FABRICA_ECO'] * 18, KWM, dict(refunda=1, t_corte=3000, p_mut=0.05, banco=100, n_sombra=4, cada_gen=1000)),
    ('brazo VIDA (corre_eco.eco_cfg), corte 3000', (10047, 10048), ['FABRICA_ECO'] * 18, KWM, CR.eco_cfg('VIDA', 3000)),
    ('brazo CEREBRO, corte 3000', (10016, 10049), ['FABRICA_ECO'] * 18, KWM, CR.eco_cfg('CEREBRO', 3000)),
    ('brazo AZAR (p_mut 0.3), corte 3000', (10015, 10050), ['FABRICA_ECO'] * 18, KWM, dict(CR.eco_cfg('AZAR', 3000), p_mut=0.3)),
    ('brazo MUT0, corte 3000', (10017, 10051), ['FABRICA_ECO'] * 18, KWM, CR.eco_cfg('MUT0', 3000)),
    ('VIDA con banco 5 < n (banco inicial recortado)', (10018, 10052), ['FABRICA_ECO'] * 18, KWM, dict(CR.eco_cfg('VIDA', 3000), banco=5, p_mut=0.3)),
    ('genoma explicito NO entero, sin sombras', (10019, 10053), ['FABRICA_ECO'] * 9, dict(T=4000, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=100),
     dict(refunda=1, genoma=list(GX), p_mut=0.2, n_sombra=0, cada_gen=700, banco=30)),
    ('tope 20 con eco (bloqueados)', (10054, 10055), ['FABRICA_ECO'] * 18, dict(KWM, tope_cuerpos=20), dict(refunda=1, p_mut=0.1, n_sombra=2, banco=40, cada_gen=1500)),
]
for et, seeds, car, kw, eco in CASOS_E:
    for s in seeds:
        res, info, a, tt = compara(et, s, car, kw, eco=eco)
        E_ = a['eco']
        info['mv'] = a['pista']['max_vivos']
        reporta(f"{et} s{s}", res, info, tt, eco=True)
        out(f"        eco: nacidos {E_['n_nac']} · mutaciones {E_['n_mut']} (sombras {E_['n_mut_s']}) · fundadores del banco {E_['n_banco']}"
            f" · refundados {E_['n_refund']} · t_ext {E_['t_ext']} · corte {E_['corte'] and E_['corte']['vivos']} · gen_t {len(E_['gen_t'])}")
fg = []
ind = MR.run_solapadas(10008, ['FABRICA_ECO'] * 9, T=6000, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=100,
                       eco=dict(refunda=1, ind_cb=lambda li, row, g: fg.append((li, row))))
di("(S) flujo de individuos del gemelo: filas == muertes + vivos y l.ind vacio",
   len(fg) == sum(l['deaths'] + l['vivos_final'] for l in ind['linajes']) and all(l['individuos'] == [] for l in ind['linajes']),
   f"filas {len(fg)}")

# ================================================================================================ (C)
seccion('(C) CHECKPOINT: estado completo del original == estado del gemelo; cortado y reanudado; firma')
CKS = {}
for et, s, car, kw, eco in (('vivero + corte, p_mut 0.1', 10010, ['FABRICA_ECO'] * 18, dict(T=4000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500),
                             dict(refunda=1, t_corte=2500, p_mut=0.1, banco=100, n_sombra=4, cada_gen=500)),
                            ('AZAR, tope 3000, muestra 1000', 10060, ['FABRICA_ECO'] * 27, dict(T=4000, diag=0, mundo_n=27, tope_cuerpos=3000, muestra=1000),
                             dict(CR.eco_cfg('AZAR', 2000), p_mut=0.2))):
    cko, ckg = {}, {}
    so = ME.run_solapadas(s, car, eco=dict(eco, ckpt_cada=1000, ckpt_fn=lambda t, b: cko.__setitem__(t, b)), **kw)
    sg = MR.run_solapadas(s, car, eco=dict(eco, ckpt_cada=1000, ckpt_fn=lambda t, b: ckg.__setitem__(t, b)), **kw)
    CKS[s] = (cko, ckg)
    di(f"{et} s{s}: seguida con checkpoints, gemelo == original (toda la salida)", N(so) == N(sg), f"checkpoints {sorted(cko)} / {sorted(ckg)}")
    for tt in sorted(cko):
        co = canon_orig(cko[tt]); cg = canon_gem(ckg[tt], kw['muestra'])
        dk = [k for k in co if N(co[k]) != N(cg.get(k))]
        di(f"{et}: ESTADO COMPLETO en t={tt} (cuerpos, cerebros, genomas, mundo, rng, banco, contadores)", not dk,
           f"{len(co['cuerpos'])} cuerpos, {len(co['mundo'])} objetos, banco {len(co['ES']['banco'])}; pickle {len(cko[tt]) // 1024} KB / {len(ckg[tt]) // 1024} KB"
           + (f" · DIFIERE {dk}" if dk else ''))
    for tt in sorted(ckg):
        blob = pickle.loads(pickle.dumps(ckg[tt]))
        r = MR.run_solapadas(s, car, eco=dict(eco, estado=blob), **kw)
        di(f"{et}: gemelo cortado en t={tt} y reanudado == original seguido (toda la salida)", N(r) == N(so))
ecc = dict(refunda=1, t_corte=2500, p_mut=0.1, banco=100, n_sombra=4, cada_gen=500)
kwc = dict(T=4000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500)
cko, ckg = CKS[10010]
m = aborta(lambda: MR.run_solapadas(10011, ['FABRICA_ECO'] * 18, eco=dict(ecc, estado=ckg[2000]), **kwc))
di("checkpoint del gemelo de OTRA corrida aborta", m is not None and 'firma' in m, str(m))
m = aborta(lambda: MR.run_solapadas(10010, ['FABRICA_ECO'] * 18, eco=dict(ecc, estado=cko[2000]), **kwc))
di("checkpoint del ORIGINAL en el gemelo aborta (formato propio; declarado)", m is not None and 'firma' in m, str(m))
m = aborta(lambda: ME.run_solapadas(10010, ['FABRICA_ECO'] * 18, eco=dict(ecc, estado=ckg[2000]), **kwc))
di("checkpoint del GEMELO en el original aborta", m is not None and 'firma' in m, str(m))

# ================================================================================================ (X)
seccion('(X) EL MUNDO DE LA SERIE (corre_eco.MUNDO: esc 90, 90 FABRICA_ECO, tope 3000, muestra 1000)')
KWX = lambda T: dict(T=T, diag=0, mundo_n=CR.MUNDO['esc'], tope_cuerpos=CR.MUNDO['tope'], muestra=CR.MUNDO['muestra'])
VEL = {}
for et, s, T, eco in (('VIDA, corte 3000', 19001, 4000, CR.eco_cfg('VIDA', 3000)), ('AZAR, corte 1500', 19002, 2000, CR.eco_cfg('AZAR', 1500)),
                      ('MUT0, corte 1500', 19003, 2000, CR.eco_cfg('MUT0', 1500))):
    t0 = time.time(); a = ME.run_solapadas(s, [CR.MUNDO['carro']] * CR.MUNDO['n0'], eco=eco, **KWX(T)); ta = time.time() - t0
    MR.run_solapadas(s, [CR.MUNDO['carro']] * CR.MUNDO['n0'], eco=eco, **KWX(200))   # caliente (la cache ya esta cargada)
    t0 = time.time(); b = MR.run_solapadas(s, [CR.MUNDO['carro']] * CR.MUNDO['n0'], eco=eco, **KWX(T)); tb = time.time() - t0
    cm = float(np.mean(a['pista']['tam_total'])); VEL[et] = (T, ta, tb, cm)
    di(f"{et} s{s} T={T}: toda la salida", N(a) == N(b),
       f"cuerpos medios {cm:.1f}, max {a['pista']['max_vivos']}, nacidos {a['eco']['n_nac']}, refundados {a['eco']['n_refund']}; "
       f"original {ta:.1f} s ({T / ta:.0f} pasos/s), gemelo {tb:.2f} s ({T / tb:.0f} pasos/s), x{ta / tb:.0f}"
       + ('' if N(a) == N(b) else f" · DIFIERE {claves_distintas(a, b)[:5]}"))

# ================================================================================================ (J)
seccion('(J) corre_eco SIN cambiar su letra (corre_eco_rapido cambia CR.ME por el gemelo): juez y trabajo()')
ME_ORIG = CR.ME
import corre_eco_rapido as CRR
ME_GEM = CRR.ME_GEMELO


def con(motor, f, *a):
    viejo = CR.ME; CR.ME = motor
    try: return f(*a)
    finally: CR.ME = viejo


di("corre_eco_rapido: CR.ME es el gemelo y lo demas de motor_eco es el original",
   CR.ME is ME_GEM and ME_GEM.run_solapadas is MR.run_solapadas and ME_GEM.genoma0 is ME.genoma0 and ME_GEM.NOMBRES is ME.NOMBRES
   and 'motor_eco_rapido.py' in CR.ME_SHA())
jo = con(ME_ORIG, CR.juez, list(G0), (19201, 19202, 19203), 20000); jg = con(ME_GEM, CR.juez, list(G0), (19201, 19202, 19203), 20000)
di("juez: bateria de G0 (esc 9, 9 fundadores, sin mutacion ni reposicion, T_b 20000), 3 semillas selladas", N(jo) == N(jg),
   str([(d['vive'], d['nac']) for d in jo]))
Gm = G0.copy(); Gm[ME.NOMBRES.index('rep_umbral')] = 0.6; Gm[ME.NOMBRES.index('dote')] = 0.3
bk = [list(Gm * np.exp(0.02 * k)) for k in range(-4, 5)] + [list(G0)] * 5
jo = con(ME_ORIG, CR.juez, bk, (19011, 19012), 3000); jg = con(ME_GEM, CR.juez, bk, (19011, 19012), 3000)
di("juez: banco mutante (9 entradas al azar por semilla), T_b 3000", N(jo) == N(jg), str([(d['vive'], d['nac']) for d in jo]))
tmp = tempfile.mkdtemp(prefix='eco_rapido_')
try:
    args = lambda d, re: (19001, 'VIDA', 12000, 8000, d, 2, 3000, re)
    da, db, dc = (os.path.join(tmp, x) for x in 'abc')
    for d in (da, db, dc): os.makedirs(d)
    t0 = time.time(); ro = con(ME_ORIG, CR.trabajo, args(da, False)); to = time.time() - t0
    t0 = time.time(); rg_ = con(ME_GEM, CR.trabajo, args(db, False)); tg = time.time() - t0
    sin = lambda r: {k: v for k, v in r.items() if k != 'seg'}
    ja = json.load(open(os.path.join(da, 'VIDA_s19001.json'), encoding='utf-8')); jb = json.load(open(os.path.join(db, 'VIDA_s19001.json'), encoding='utf-8'))
    di("trabajo(19001, VIDA, T 12000, corte 8000, juez 2x3000): resultado y JSON == original (salvo 'seg')",
       N(sin(ro)) == N(sin(rg_)) and N(sin(ja)) == N(sin(jb)),
       f"persiste {ro['persiste']} t_ext {ro['t_ext']} nacidos {ro['n_nac']} juez {[d['vive'] for d in ro['juez']['bateria']] if ro['juez'] else None}; "
       f"original {to:.1f} s, gemelo {tg:.1f} s")

    class Corte(Exception): pass
    real = ME_GEM.run_solapadas

    def corta(*a, **k):
        fn = k['eco']['ckpt_fn']

        def f2(t, blob): fn(t, blob); raise Corte(t)
        k['eco'] = dict(k['eco'], ckpt_fn=f2)
        return real(*a, **k)
    ME_GEM.run_solapadas = corta
    try: con(ME_GEM, CR.trabajo, args(dc, False)); cortado = None
    except Corte as e: cortado = e.args[0]
    finally: ME_GEM.run_solapadas = real
    rr = con(ME_GEM, CR.trabajo, args(dc, True))
    di("trabajo cortado ('corte de luz' tras el checkpoint) y reanudado con --reanuda == original seguido",
       cortado == 10000 and N(sin(rr)) == N(sin(ro)), f"cortado en t={cortado}")
finally:
    shutil.rmtree(tmp)

# ================================================================================================ (K)
seccion('(K) CONTROLES que DEBEN fallar (si nada cambia, nada controla: ERR-38)')
base = SALIDAS[('9 FABRICA fija T=3000', 10001)]
g = MR.run_solapadas(10002, ['FABRICA'] * 9, T=3000, diag=0)
di("gemelo con la semilla vecina != original", N(g) != N(base))
for et, modo in (("gemelo con exp de libm (sin el bucle de NumPy)", dict(exp=1)), ("gemelo con suma ingenua (sin BLAS)", dict(dot=1)),
                 ("gemelo con turno fijo (mismo consumo de azar)", dict(turno=1))):
    res, info, a, tt = compara(et, 10001, ['FABRICA'] * 9, dict(T=3000, diag=0), modo=modo)
    di(f"{et} != original (trayectoria o pesos)", not (res['traza'] and res['cerebros']),
       f"salida {'=' if res['salida'] else '!='} · traza {'=' if res['traza'] else '!='} · cerebros {'=' if res['cerebros'] else '!='}")
e1 = MR.run_solapadas(10047, ['FABRICA_ECO'] * 18, eco=CR.eco_cfg('VIDA', 3000), **KWM)
e2 = MR.run_solapadas(10047, ['FABRICA_ECO'] * 18, eco=CR.eco_cfg('MUT0', 3000), **KWM)
e3 = MR.run_solapadas(10047, ['FABRICA_ECO'] * 18, eco=CR.eco_cfg('AZAR', 3000), **KWM)
di("brazo VIDA != MUT0 (misma semilla)", N(e1) != N(e2), f"mutaciones {e1['eco']['n_mut']} / {e2['eco']['n_mut']}")
di("brazo AZAR != VIDA (misma semilla)", N(e1['eco']['gen_t']) != N(e3['eco']['gen_t']))
di("reposicion inmediata != fija", N(MR.run_solapadas(10023, ['FABRICA'] * 9, T=2000, diag=0)) != N(SALIDAS[('9 FABRICA inmediata T=2000', 10023)]))

# ================================================================================================ (G)
seccion('(G) GUARDIAS: las del original con el mismo mensaje; las del gemelo (lo que no compila aborta)')
for et, kw in (("10 linajes con eco=None", dict(seed=1, carros=['FABRICA'] * 10, T=10, diag=0)),
               ("diag=1", dict(seed=1, carros=['FABRICA'], T=10)),
               ("compat=1", dict(seed=1, carros=['FABRICA'], T=10, diag=0, compat=1)),
               ("rep_acum=2", dict(seed=1, carros=['FABRICA'], T=10, diag=0, rep_acum=2)),
               ("tope_cuerpos < n", dict(seed=1, carros=['FABRICA'] * 3, T=10, diag=0, tope_cuerpos=2)),
               ("reposicion invalida", dict(seed=1, carros=['FABRICA'], T=10, diag=0, reposicion='otra')),
               ("mundo_n fuera de rango", dict(seed=1, carros=['FABRICA'], T=10, diag=0, mundo_n=10)),
               ("carro inexistente", dict(seed=1, carros=['NO_EXISTE'], T=10, diag=0)),
               ("clave eco desconocida", dict(seed=1, carros=['FABRICA_ECO'], T=10, diag=0, eco=dict(refnda=0))),
               ("genoma fuera de rango", dict(seed=1, carros=['FABRICA_ECO'], T=10, diag=0, eco=dict(genoma=list(G0 * 10)))),
               ("t_corte sin vivero", dict(seed=1, carros=['FABRICA_ECO'], T=10, diag=0, eco=dict(refunda=0, t_corte=5)))):
    mo = aborta(lambda: ME.run_solapadas(**kw)); mg = aborta(lambda: MR.run_solapadas(**kw))
    di(f"{et}: aborta igual que el original", mo is not None and mo == mg, str(mg)[:110])
for et, kw in (("carro O2 (no es el cerebro FABRICA)", dict(seed=1, carros=['O2'] * 3, T=10, diag=0)),
               ("carro APR_ECO con eco", dict(seed=1, carros=['APR_ECO'] * 3, T=10, diag=0, eco=dict(refunda=1)))):
    mg = aborta(lambda: MR.run_solapadas(**kw))
    di(f"{et}: el gemelo aborta (fuera de alcance)", mg is not None and mg.startswith('ValueError'), str(mg)[:110])

# ================================================================================================ (D)
seccion('(D) DETERMINISMO')
e1b = MR.run_solapadas(10047, ['FABRICA_ECO'] * 18, eco=CR.eco_cfg('VIDA', 3000), **KWM)
di("dos llamadas iguales del gemelo (eco VIDA con mutacion) dan la misma salida", N(e1) == N(e1b))

# ================================================================================================ (Z)
seccion('(Z) CACHE: un proceso NUEVO carga la cache de numba y reproduce corridas del original')
tmp = tempfile.mkdtemp(prefix='eco_rapido_cache_')
try:
    ref = os.path.join(tmp, 'ref.json')
    casos_z = [[10001, 'I', 3000], [10047, 'E', 6000], [10035, 'L', 15000]]
    refs = {'10001': SALIDAS[('9 FABRICA fija T=3000', 10001)], '10035': SALIDAS[('9 FABRICA T=15000 (vida larga: divisiones)', 10035)],
            '10047': ME.run_solapadas(10047, ['FABRICA_ECO'] * 18, eco=CR.eco_cfg('VIDA', 3000), **KWM)}   # el ORIGINAL
    json.dump(dict(casos=casos_z, refs={k: N(v) for k, v in refs.items()}, eco=CR.eco_cfg('VIDA', 3000), kwm=KWM), open(ref, 'w'))
    hijo = r'''
import json, sys, time, os
t0 = time.time()
sys.path[:0] = [sys.argv[2], os.path.join(os.path.dirname(os.path.dirname(sys.argv[2])), 'experimentos', 'generaciones')]
import motor_eco_rapido as MR
from numba.core.registry import CPUDispatcher
t1 = time.time()
R = json.load(open(sys.argv[1])); N = lambda x: json.dumps(x, default=str, sort_keys=True)
ok = []; tiempos = []
for s, tipo, T in R['casos']:
    t2 = time.time()
    if tipo == 'E': r = MR.run_solapadas(s, ['FABRICA_ECO'] * 18, eco=R['eco'], **R['kwm'])
    else: r = MR.run_solapadas(s, ['FABRICA'] * 9, T=T, diag=0)
    tiempos.append(round(time.time() - t2, 2)); ok.append(N(r) == R['refs'][str(s)])
hits = miss = 0
for nom in dir(MR):
    f = getattr(MR, nom)
    if isinstance(f, CPUDispatcher):
        hits += sum(f.stats.cache_hits.values()); miss += sum(f.stats.cache_misses.values())
print(json.dumps(dict(ok=ok, import_s=round(t1 - t0, 2), tiempos=tiempos, hits=hits, miss=miss)))
'''
    p = subprocess.run([sys.executable, '-c', hijo, ref, AQUI], capture_output=True, text=True, timeout=900)
    try: z = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception: z = dict(ok=[False], hits=0, miss=-1, import_s=None, tiempos=None, err=p.stderr[-400:])
    di("proceso NUEVO: lee la cache (0 compilaciones) y reproduce 3 corridas del original bit a bit",
       all(z['ok']) and len(z['ok']) == 3 and z['miss'] == 0 and z['hits'] > 0,
       f"identicas {z['ok']}; funciones cargadas de la cache {z['hits']}, compiladas {z['miss']}; import {z['import_s']} s; "
       f"corridas {z['tiempos']} s" + (f" · {z.get('err')}" if z.get('err') else ''))
finally:
    shutil.rmtree(tmp)

# ================================================================================================ (V)
seccion('(V) ACELERACION (mismo mundo, mismo proceso; la maquina corre otras series: tiempos con carga)')
for et, (T, ta, tb, cm) in VEL.items():
    out(f"  mundo ECO {et}: T={T}, {cm:.1f} cuerpos de media · original {T / ta:.0f} pasos/s ({ta / T / cm * 1e6:.1f} us por cuerpo y paso)"
        f" · gemelo {T / tb:.0f} pasos/s ({tb / T / cm * 1e6:.2f} us por cuerpo y paso) · x{ta / tb:.0f}")
a = SALIDAS[('9 FABRICA T=15000 (vida larga: divisiones)', 10035)]
t0 = time.time(); ME.run_solapadas(10035, ['FABRICA'] * 9, T=15000, diag=0); ta = time.time() - t0
t0 = time.time(); MR.run_solapadas(10035, ['FABRICA'] * 9, T=15000, diag=0); tb = time.time() - t0
cm = float(np.mean(a['pista']['tam_total']))
out(f"  pista v2, 9 FABRICA, T=15000: {cm:.1f} cuerpos de media · original {15000 / ta:.0f} pasos/s · gemelo {15000 / tb:.0f} pasos/s · x{ta / tb:.0f}")
out(f"tiempo {round(time.time() - T00)} s")
out(f"RESULTADO: {OK[0]}/{OK[1]}")
SAL.close()
