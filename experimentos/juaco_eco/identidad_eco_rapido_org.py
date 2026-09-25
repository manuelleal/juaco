"""identidad_eco_rapido_org.py — ARNES del GEMELO COMPILADO motor_eco_rapido_org.py (ECO v2, ORGANOS COMO GENES: motor_eco2 +
FAMB_ORG_ECO; y FAMB_RES0_ECO / FABRICA_ECO / FABRICA con 20 genes). Un proceso, sin Pool. Nube, 24-sep-2026 (compilador de gemelos).

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Un gemelo que no sea BIT A BIT identico SOLO EXPLORA, nunca confirma (regla 9 de registro/EQUIPO.md).

SEMILLAS: SOLO de practica, 19901-19909, 20091-20099 y 10001-10011.

QUE SE COMPARA (gemelo contra motor_eco2.run_solapadas, el original en Python, en el mismo proceso):
  (0) ORIGEN: sha fijados; motor_eco2 y FAMB_ORG_ECO en disco == los que construye construye_eco_org.py; genoma de 20 genes.
  (P) PRIMITIVAS (las del gemelo de la familia, re-verificadas): exp, BLAS, Generator, sumas de 6, fila de la sorpresa, top-3.
  (N) NACIMIENTO AISLADO de FAMB_ORG_ECO con genomas de 20 genes al azar (organos prendidos o no, y en el umbral EXACTO 1.0) y memoria
      None o tabla al azar: crea + nace del carro == _consts + _crea + _nace (+ _nace_fam con el 'filtra0' que el gemelo saca del genoma).
      al_parir: con 'ensena' la tabla == _tabla_padre; sin el, None y el parto no se cuenta.
  (I) E1 eco=None con FAMB_ORG_ECO (los organos se toman apagados: = FABRICA_ECO en la fisica) y mezclas.
  (E) E2 eco=dict: brazos VIDA, AZAR y MUT0 de corre_eco (20 genes) en esc 30, 90 y 270 (corto); genomas con los organos prendidos,
      apagados, mezclados por linaje y en el umbral; mutacion que los prende y apaga; refunda=0; tope. En CADA corrida: salida completa,
      trayectoria (cada actua), CADA NACIMIENTO tras nace(), cerebro + familia + ORGANOS de cada vivo, mundo, filas de ind_cb.
  (C) CHECKPOINT: estado completo (con organos) == el del original; cortado y reanudado == seguido; firmas ajenas abortan.
  (X) EL MUNDO DE LA SERIE de v2 con FAMB_ORG_ECO: esc 90 (VIDA, AZAR, MUT0) y esc 270 corto.
  (J) JUEZ (corre_eco.juez con CR.ME = motor_eco2 o el gemelo, MUNDO['carro'] = FAMB_ORG_ECO, refunda=0, genoma=): G0 y un banco
      real de 20 genes con organos. corre_eco_v2.trabajo (su runner) con el gemelo (usa_gemelo) == con Python; cortado y reanudado.
  (L) LARGO: eco VIDA esc 9 con mutacion fuerte (los organos se prenden y apagan), T 30 000.
  (R) REGRESION con 20 genes: FABRICA_ECO y FAMB_RES0_ECO contra motor_eco2; eco=None: gemelo de organos == gemelo de la familia.
  (K) CONTROLES que DEBEN fallar, barridos sobre TODAS las corridas guardadas con su prediccion exacta: organos siempre expresados
      (difiere en toda corrida con un parto de un padre sin 'ensena' o un hijo sin 'filtra0' que recibio neutras); 'filtra0' del PADRE
      (difiere en toda corrida con un parto con neutras donde el organo del padre y el del hijo no coinciden); sin leer el nodo; empate
      al primero (tablas de una entrada). Y: semilla vecina, exp de libm, suma ingenua, turno fijo, VIDA contra MUT0.
  (G) GUARDIAS.  (D) DETERMINISMO.  (Z) CACHE en un proceso NUEVO.  (V) ACELERACION.
Uso: /root/venv-juaco/bin/python experimentos/juaco_eco/identidad_eco_rapido_org.py   (escribe identidad_eco_rapido_org_salida.txt
     desde el arranque; la ultima linea es RESULTADO: N/N)
"""
import copy, importlib.util, json, os, pickle, shutil, subprocess, sys, tempfile, time, types
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')]
import motor_eco2 as ME2
import pista2 as P
import motor_eco_rapido_org as MO
import corre_eco as CR
import construye_eco_org as CORG

N = lambda x: json.dumps(x, default=str, sort_keys=True)
OK = [0, 0]
SAL = open(os.path.join(AQUI, 'identidad_eco_rapido_org_salida.txt'), 'w', encoding='utf-8')
T00 = time.time()
PRACTICA = set(range(19901, 19910)) | set(range(20091, 20100)) | set(range(10001, 10012))


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


def sem(s):
    assert s in PRACTICA, f"semilla {s} fuera de la practica"
    return s


FAB = P.carga_carro('FABRICA'); FE = ME2.carga_eco('FABRICA_ECO'); FM = ME2.carga_eco('FAMB_RES0_ECO'); FO = ME2.carga_eco('FAMB_ORG_ECO')
CF = P.cfg_fabrica(); G0 = ME2.genoma0(CF); LO, HI = ME2.rangos(G0); NLEE = int(CF['kw']['nodo_lee'])
IE, IF = ME2.NOMBRES.index('ensena'), ME2.NOMBRES.index('filtra0')
HX = lambda a: np.ascontiguousarray(a).tobytes().hex()
EST = lambda r: r.bit_generator.state
LET = 'ABCD'
out(f"IDENTIDAD motor_eco_rapido_org · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {np.__version__} · "
    f"numba {__import__('numba').__version__} · gemelo {MO._h16(MO.__file__)} · arnes {MO._h16(os.path.abspath(__file__))}")


# ================================================================ el carro ESPIA (misma conducta; registra instancias, actua y partos)
class Registro:
    def __init__(self): self.REG = []; self.TRZ = []; self.NAC = []; self.MEM = []; self.PORID = {}; self.vista = None


def espia(base, reg):
    class Carro(base.Carro):
        def actua(self, obs):
            if reg.vista is None: reg.vista = obs['objs']
            a = base.Carro.actua(self, obs)
            reg.TRZ.append((obs['t'], self._lin_espia, obs['pos'], obs['E'], obs['Ag'], int(a['mov']), int(bool(a['muerde']))))
            return a

        def nace(self, info):
            base.Carro.nace(self, info)
            n10 = getattr(self, '_n10', None); mem = info.get('memoria'); par = reg.PORID.get(info.get('padre'))
            reg.NAC.append((info['t'], self._lin_espia, info['k'], (n10['recibido'] if n10 is not None else -1), int(self._nlec),
                            int(self._ldiv), HX(self.Wps), HX(self.Wns)))
            if hasattr(self, 'ENSENA'):   # FAMB_ORG_ECO: lo que decide cada control de los organos
                reg.MEM.append(dict(org=1, mem_none=mem is None, nneu=sum(1 for e in (mem or []) if float(e[1]) == 0.0),
                                    fil_hijo=bool(self.FILTRA0), fil_padre=(bool(par.FILTRA0) if par is not None else None),
                                    una=(n10 is not None and n10['recibido'] == NLEE)))
            else:
                reg.MEM.append(dict(org=0, mem_none=mem is None, nneu=0, fil_hijo=None, fil_padre=None,
                                    una=(n10 is not None and n10['recibido'] == NLEE)))

    class Mod:
        __file__ = base.__file__

        @staticmethod
        def crea(ctx):
            c = Carro(ctx); c._lin_espia = ctx['indice']; reg.REG.append((ctx['id'], ctx['indice'], c)); reg.PORID[ctx['id']] = c
            return c
    return Mod


def carros_espia(carros, reg, eco):
    res = []
    for c in carros:
        e, m = (c, (P.carga_carro(c) if eco is None else ME2.carga_eco(c))) if isinstance(c, str) else c
        res.append((e, espia(m, reg)))
    return res


# ================================================================ cerebros y estados canonicos (con familia y ORGANOS)
def fam_orig(c):
    md = {}
    for _t, k9, n9, R9 in c._mordh: md[(int(n9), LET.index(k9))] = float(R9)
    d = dict(md=[[n, k, R] for (n, k), R in sorted(md.items())], nodo=c._nodo, nlec=int(c._nlec), ldiv=int(c._ldiv))
    if hasattr(c, '_n10'):
        c2 = copy.copy(c); c2._n10 = copy.deepcopy(c._n10)
        d.update(n10=dict(recibido=c._n10['recibido'], partos=c._n10['partos'], dado=c._n10['dado'][:50]),
                 tabla=c2.al_parir(dict(t=-1, k=-1)))
    if hasattr(c, 'ENSENA'): d.update(organos=[int(c.ENSENA), int(c.FILTRA0)])
    return d


def fam_gem(st, s):
    bi = st['bi'][s]; tf = int(st['LFAM'][int(bi[MO.I_LIN])])
    d = dict(md=[[n, k, R] for n, k, R in MO._tabla_py(st, s, 'md')], nodo=MO._nodo_py(st, s, NLEE),
             nlec=int(bi[MO.I_NLEC]), ldiv=int(bi[MO.I_LDIV]))
    if tf:
        npa = int(bi[MO.I_NPART])
        ens = tf == 1 or bool(bi[MO.I_ENS])   # lo que haria al_parir: la tabla si el organo 'ensena' esta expresado
        d.update(n10=dict(recibido=int(bi[MO.I_RECIB]), partos=npa, dado=[int(x) for x in st['dado'][s, :min(npa, MO.DADO)]]),
                 tabla=(MO._tabla_padre_py(st, s) if ens else None))
    if tf == 2: d.update(organos=[int(bi[MO.I_ENS]), int(bi[MO.I_FIL])])
    return d


def cerebro_orig(c, t):
    return dict(Wl=HX(c.Wl), el=HX(c.el), tr=HX(c.tr), KW=HX(c.KW), activa=HX(c.activa), Wp=HX(c.Wp), Wn=HX(c.Wn),
                Wps=HX(c.Wps), Wns=HX(c.Wns), err=HX(c.err), mu=HX(c.mu), mup=HX(c.mup), mun=HX(c.mun), zp=HX(c.zp), zn=HX(c.zn),
                splits=c.splits, split_t=[list(x) for x in c.split_t], err_max=float(c.err_max), t_conflicto=c.t_conflicto,
                t_techo=c.t_techo, n_techo=c.n_techo, gpa=c._gpa, gpn=c._gpn, na=int(c._na), nm=int(c._nm), R=float(c._R),
                Rp=float(c._Rp), hambre=float(c._hambre), sin_objetivo=list(c.sin_objetivo),
                ncod=[[sorted(k), v] for k, v in c.ncod.items()], rech=sorted((x, v) for x, v in c._rech.items() if v >= t),
                rng=EST(c.rng), familia=fam_orig(c))


def cerebro_gem(st, s, t):
    bi = st['bi'][s]; bf = st['bf'][s]; b = MO.NKMAX + 1
    ncod = [[sorted([int(k) // (b * b) - 1, (int(k) // b) % b - 1, int(k) % b - 1]), int(v)]
            for k, v in zip(st['nck'][s][:bi[MO.I_NCN]], st['ncc'][s][:bi[MO.I_NCN]])]
    return dict(Wl=HX(st['Wl'][s]), el=HX(st['el'][s]), tr=HX(st['tr'][s]), KW=HX(st['KW'][s]), activa=HX(st['act'][s]),
                Wp=HX(st['Wp'][s]), Wn=HX(st['Wn'][s]), Wps=HX(st['Wps'][s]), Wns=HX(st['Wns'][s]), err=HX(st['err'][s]),
                mu=HX(st['mu'][s]), mup=HX(st['mup'][s]), mun=HX(st['mun'][s]), zp=HX(st['zp'][s]), zn=HX(st['zn'][s]),
                splits=int(bi[MO.I_SPL]), split_t=[[int(st['stt'][s][i]), P.TIPOS[int(st['stk'][s][i])]] for i in range(bi[MO.I_NST])],
                err_max=float(bf[MO.F_ERRMAX]), t_conflicto=(None if bi[MO.I_TCON] < 0 else int(bi[MO.I_TCON])),
                t_techo=(None if bi[MO.I_TTEC] < 0 else int(bi[MO.I_TTEC])), n_techo=int(bi[MO.I_NTEC]), gpa=int(bi[MO.I_GPA]),
                gpn=int(bi[MO.I_GPN]), na=int(bi[MO.I_NA]), nm=int(bi[MO.I_NM]), R=float(bf[MO.F_R]), Rp=float(bf[MO.F_RP]),
                hambre=float(bf[MO.F_HAMB]), sin_objetivo=[int(bi[MO.I_SO0 + q]) for q in range(4)], ncod=ncod,
                rech=sorted((int(x), int(v)) for x, v in zip(st['rpos'][s][:bi[MO.I_RN]], st['rexp'][s][:bi[MO.I_RN]]) if v >= t),
                rng=EST(st['GL'][int(s)]), familia=fam_gem(st, s))


def mundo_gem(st):
    wi = st['wi']
    return [(int(st['seqpos'][q]), P.TIPOS[int(st['grid'][st['seqpos'][q]])]) for q in range(int(wi[MO.W_NSEQ])) if st['seqpos'][q] >= 0]


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
    for s in [int(x) for x in st['cuer'][:wi[MO.W_NCUER]]]:
        bi = st['bi'][s]; bf = st['bf'][s]
        cs.append(dict(lin=int(bi[MO.I_LIN]), k=int(bi[MO.I_K]), gen=int(bi[MO.I_GEN]), padre=int(bi[MO.I_PADRE]),
                       tn=int(bi[MO.I_TN]), pos=int(bi[MO.I_POS]), E=float(bf[MO.F_E]), Ag=float(bf[MO.F_AG]), gv=int(bi[MO.I_GV]),
                       tB=int(bi[MO.I_TB]), tD=int(bi[MO.I_TD]), vol=int(bi[MO.I_VOL]), hijos=int(bi[MO.I_HIJ]),
                       fund=int(bi[MO.I_FUND]), g=HX(st['G'][s]), s=HX(st['SH'][s]), cerebro=cerebro_gem(st, s, t)))
    lin = []
    for i in range(li.shape[0]):
        lv = li[i]
        lin.append(dict(mord={x: [int(v) for v in st['mord'][i, j]] for j, x in enumerate(P.TIPOS)},
                        vis={x: [int(v) for v in st['vis'][i, j]] for j, x in enumerate(P.TIPOS)},
                        deaths=int(lv[MO.L_DEATHS]), mnec=[int(lv[MO.L_MN0]), int(lv[MO.L_MN1])],
                        causas={x: int(lv[MO.L_CZ0 + j]) for j, x in enumerate(ME2.CAUSAS)}, mvol=int(lv[MO.L_MVOL]),
                        fund=int(lv[MO.L_FUND]), tfund=[int(x) for x in st['tfund'][i, :lv[MO.L_NTF]]], desc=int(lv[MO.L_DESC]),
                        nac=int(lv[MO.L_NAC]), bloq=int(lv[MO.L_BLOQ]), vidas=B['lin_py'][i]['vidas'], ind=B['lin_py'][i]['ind'],
                        vivos=int(lv[MO.L_VIVOS]), tam=[int(x) for x in st['tam'][:nsamp, i]], pv=int(lv[MO.L_PV])))
    return dict(t=t, cuerpos=cs, mundo=mundo_gem(st), rng=EST(st['rng']), pista=EST(st['rng_pista']),
                fund=[EST(r) for r in st['FUND']], muerte=[EST(r) for r in st['MUE']], quimio=float(st['wf'][0]),
                pisos=int(wi[MO.W_PISOS]), llegadas=int(wi[MO.W_LLEG]), perdidas=int(wi[MO.W_PERD]), olv=int(wi[MO.W_OLV]),
                comp={x: int(wi[MO.W_COMP0 + j]) for j, x in enumerate(P.TIPOS)}, nsuma=int(wi[MO.W_NSUMA]),
                total=int(wi[MO.W_TOTAL]), maxv=int(wi[MO.W_MAXV]), ttope=(None if wi[MO.W_TTOPE] < 0 else int(wi[MO.W_TTOPE])),
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


GUARDA = []   # corridas del original (salida, filas, nacimientos, lo que decide cada control) para barrer los controles en (K)


def compara(seed, carros, kw, eco=None, modo=None, filas=True):
    reg = Registro(); fo, fg = [], []
    eo = eg = None
    if eco is not None:
        eo = dict(eco); eg = dict(eco)
        if filas:
            eo['ind_cb'] = lambda li, row, g: fo.append((li, list(row), HX(g)))
            eg['ind_cb'] = lambda li, row, g: fg.append((li, list(row), HX(g)))
    t0 = time.time(); a = ME2.run_solapadas(sem(seed), carros_espia(carros, reg, eco), eco=eo, **kw); ta = time.time() - t0
    trz = []; fin = {}; trn = []
    t0 = time.time(); b = MO.run_solapadas(seed, carros, eco=eg, _traza=trz, _modo=modo, _estado_final=fin, _traza_nac=trn, **kw); tb = time.time() - t0
    st = fin['st']; tfin = fin['t']
    dif = claves_distintas(a, b)
    ids = a['pista']['ids']; porid = {}
    for ident, i, c in reg.REG: porid[(i, ident)] = c
    malos = []; nviv = 0; org_on = [0, 0]
    for s in fin['vivos']:
        i = int(st['bi'][s, MO.I_LIN]); k = int(st['bi'][s, MO.I_K]); fu = int(st['bi'][s, MO.I_FUND])
        c = porid.get((i, ids[i] if fu else f"{ids[i]}/{k}"))
        nviv += 1
        if hasattr(c, 'ENSENA'): org_on[0] += int(c.ENSENA); org_on[1] += int(c.FILTRA0)
        if c is None or N(cerebro_orig(c, tfin)) != N(cerebro_gem(st, s, tfin)): malos.append((i, k))
    res = dict(salida=not dif, filas=(N(fo) == N(fg)), traza=(N(reg.TRZ) == N(trz)), cerebros=not malos,
               mundo=(N(list(reg.vista.items())) == N(mundo_gem(st))), nacimientos=(N(reg.NAC) == N(trn)))
    M_ = reg.MEM; morg = [m for m in M_ if m['org']]
    info = dict(dif=dif[:5], malos=malos[:4], nviv=nviv, ntraza=len(trz), ties=int(st['wi'][MO.W_NTIES]),
                mv=a['pista']['max_vivos'], muertes=sum(l['deaths'] for l in a['linajes']),
                nac=sum(l['descendientes'] for l in a['linajes']), pisos=a['pista']['pisos'], bloq=a['pista']['bloqueados'],
                splits=sum(c.splits for _, _, c in reg.REG), filas=len(fo), nnac=len(trn),
                ens=sum(1 for m in morg if not m['mem_none']), no_ens=sum(1 for m in morg if m['mem_none']),
                fil_si=sum(1 for m in morg if not m['mem_none'] and m['fil_hijo']), org_on=org_on,
                gmax=max([int(r[1]) for l in a['linajes'] for r in l['individuos']] + [int(r[1][1]) for r in fo], default=0))
    if modo is None:
        GUARDA.append(dict(seed=seed, carros=carros, kw=kw, eco=eco, filas=(eco is not None and filas), a=N(a), fo=N(fo), nac=N(reg.NAC),
                           p_on=sum(1 for m in morg if m['mem_none'] or (not m['fil_hijo'] and m['nneu'] > 0)),
                           p_padre=sum(1 for m in morg if not m['mem_none'] and m['nneu'] > 0 and m['fil_padre'] is not None
                                       and m['fil_padre'] != m['fil_hijo']),
                           p_lee=sum(1 for n_ in reg.NAC if n_[3] > 0), p_una=sum(1 for m in M_ if m['una'])))
    return res, info, a, (ta, tb)


def reporta(et, res, info, tt, eco=False):
    ok = all(res.values())
    ext = (f"salida {'=' if res['salida'] else '!='} · traza {info['ntraza']} {'=' if res['traza'] else '!='} · "
           f"nacimientos {info['nnac']} {'=' if res['nacimientos'] else '!='} · "
           f"cerebros+familia+organos {info['nviv']} vivos {'=' if res['cerebros'] else '!='} · mundo {'=' if res['mundo'] else '!='}"
           + (f" · filas {info['filas']} {'=' if res['filas'] else '!='}" if eco else '')
           + f" · max_vivos {info['mv']} muertes {info['muertes']} partos {info['nac']} gen_max {info['gmax']} divisiones {info['splits']}"
           + f" · partos ORG con tabla {info['ens']} (el hijo filtra {info['fil_si']}) / sin tabla {info['no_ens']}"
           + f" · vivos con ensena/filtra0 {info['org_on'][0]}/{info['org_on'][1]}"
           + (f" pisos {info['pisos']}" if info['pisos'] else '') + (f" bloqueados {info['bloq']}" if info['bloq'] else '')
           + (f" empates_top3 {info['ties']}" if info['ties'] else '')
           + f" · {tt[0]:.1f} s / {tt[1]:.2f} s" + ('' if ok else f" · DIFIERE {res} {info['dif']} {info['malos']}"))
    di(et, ok, ext)


def GEN(**kw):
    g = G0.copy()
    for k, v in kw.items(): g[ME2.NOMBRES.index(k)] = v
    assert ((g >= LO - 1e-12) & (g <= HI + 1e-12)).all(), kw
    return list(g)


# ================================================================================================ (0)
seccion('(0) ORIGEN (sha fijados en el gemelo; el instrumento Python de ECO v2 en disco es el construido)')
for p, h in MO.SHA.items():
    di(f"{os.path.relpath(p, RAIZ)} sha {h}", MO._h16(p) == h)
arts = CORG.textos()
di("motor_eco2.py y carros/FAMB_ORG_ECO.py en disco == los que construye construye_eco_org.py",
   all(open(p_, encoding='utf-8').read() == s_ for p_, s_ in arts.items()))
di("genoma de motor_eco2: los 18 de motor_eco en su sitio + ensena, filtra0 (G0 0.9, rango [0.225, 3.6]); UMBRAL_ORG 1.0",
   len(ME2.GENES) == 20 and tuple(ME2.NOMBRES[18:]) == ('ensena', 'filtra0') and list(G0[18:]) == [0.9, 0.9]
   and abs(LO[18] - 0.225) < 1e-15 and abs(HI[19] - 3.6) < 1e-15 and ME2.UMBRAL_ORG == 1.0,
   f"G0 organos {list(G0[18:])}, rango [{LO[18]}, {HI[18]}]")

# ================================================================================================ (P)
seccion('(P) PRIMITIVAS (las del gemelo de la familia, re-verificadas en este modulo)')
rng = np.random.default_rng([20091, 1])
xs = np.concatenate([rng.uniform(-40, 40, 100000), rng.normal(0, 2, 100000)])
ref = np.exp(xs); B = MO._bufs_exp(); got = np.array([MO._exp1(x, MO.EXP_LOOP, B[0], B[1], B[3], B[5], 0) for x in xs])
di("exp del gemelo (bucle 1-D de np.exp por ctypes) == np.exp, 200 000 argumentos", np.array_equal(ref.view(np.int64), got.view(np.int64)))
libm = np.array([MO._exp1(x, MO.EXP_LOOP, B[0], B[1], B[3], B[5], 1) for x in xs[:100000]])
nd = int((libm.view(np.int64) != ref[:100000].view(np.int64)).sum())
di("CONTROL (debe fallar): exp de libm != np.exp en esta maquina", nd > 0, f"distintos {nd}/100000")
PATM = np.array([CF['PAT'][x] for x in P.TIPOS], float)
malos = 0; nd_ing = 0
for rep in range(50000):
    a = rng.normal(0, 1, 90); b = rng.normal(0, 1, 90)
    if float(a @ b) != MO._dot(a, b, 90, 0): malos += 1
    if float(a @ b) != MO._dot(a, b, 90, 1): nd_ing += 1
    c6 = rng.uniform(-10, 10, 6)
    if float(c6 @ PATM[rep % 4]) != MO._dot(c6, PATM[rep % 4], 6, 0): malos += 1
di("BLAS de numba == BLAS de NumPy (ddot 90 y ddot 6 con un patron), 100 000 casos", malos == 0, f"distintos {malos}")
di("CONTROL (debe fallar): suma de izquierda a derecha != ddot de BLAS (90 denso)", nd_ing > 0, f"distintos {nd_ing}/50000")


from numba import njit


@njit
def _fila_l2r(W, n, P6):
    acc = 0.0
    for q in range(6): acc += (W[0, n, q] - W[1, n, q]) * P6[q]
    return acc


malos = 0; tot = 0
for rep in range(3000):
    Wps = rng.uniform(0, 10, (2, 6)) * (rng.random((2, 6)) < .7); Wns = rng.uniform(0, 10, (2, 6)) * (rng.random((2, 6)) < .7)
    m = int(rng.integers(1, 401)); Nn = rng.integers(0, 2, m); Kk = rng.integers(0, 4, m)
    sref = ((Wps[Nn] - Wns[Nn]) * PATM[Kk]).sum(1); W2 = np.stack([Wps, Wns])
    for i in range(0, m, max(1, m // 25)):
        tot += 1; malos += int(_fila_l2r(W2, Nn[i], PATM[Kk[i]]) != sref[i])
di(f"fila de la sorpresa del nodo: .sum(1) de NumPy en (m, 6), m = 1..400 == de izquierda a derecha desde 0.0, {tot} filas", malos == 0,
   f"distintos {malos}")
KWt = np.zeros((1, MO.NKMAX, 6)); act = np.zeros((1, MO.NKMAX), np.bool_); cc = np.zeros((1, 4, 3), np.int64)
cv = np.zeros((1, 4), np.bool_); wb = np.zeros(MO.NKMAX); wit = np.zeros(MO.NWI, np.int64)
malos = 0; nemp = 0
for rep in range(10000):
    nk = int(rng.integers(8, 91)); KWt[:] = 0; act[:] = False
    KWt[0, :nk] = rng.uniform(0, 1, (nk, 6)); act[0, :nk] = True
    if rep % 2:
        src = rng.integers(0, nk, 4); dst = rng.integers(0, nk, 4); KWt[0, dst] = KWt[0, src]
        if rep % 4 == 1: KWt[0, :nk] = np.round(KWt[0, :nk], 1)
    p = int(rng.integers(0, 4)); cv[:] = False; e0 = int(wit[MO.W_NTIES])
    MO._code3(0, p, KWt, act, PATM, cc, cv, wb, 0, wit)
    v = np.where(act[0], KWt[0] @ PATM[p], -1e9)
    if sorted(cc[0, p]) != sorted(int(z) for z in np.argsort(v)[-3:]): malos += 1
    nemp += int(wit[MO.W_NTIES]) - e0
di("codigo de Kenyon: top-3 del gemelo == set(np.argsort(...)[-3:]), 10 000 casos", malos == 0 and nemp > 50,
   f"distintos {malos}; con empate en la frontera (a NumPy por objmode) {nemp}")

# ================================================================================================ (N)
seccion('(N) NACIMIENTO AISLADO de FAMB_ORG_ECO (20 genes; organos al azar y en el umbral) y al_parir con y sin ensena')
RVd = {(n, k): (1.0 if v > 0 else (-3.0 if v < 0 else 0.0)) for k in range(4) for n, v in enumerate(CF['EFECTO'][CF['VAL_VIVO'][LET[k]]])}
rgn = np.random.default_rng([20092, 1])


def ctx_n(g, r):
    d = dict(id='x', indice=0, n_linajes=1, T=1000, L=40, PAT={k: v.copy() for k, v in CF['PAT'].items()}, rng=r, dote=0.6,
             rep_umbral=1.0, costo=0.001, costo_a=0.001, rep_X=500, cupo=P.CUPO, ancho=P.ANCHO, fabrica=P.cfg_fabrica())
    return ME2.ctx_genoma(d, g)


ORG_VAL = (0.225, 0.9, 0.9999999999999999, 1.0, 1.0000000000000002, 1.3, 3.6)   # extremos y el umbral EXACTO


def genoma_org(rep):
    g = np.array([rgn.uniform(LO[j], HI[j]) for j in range(len(G0))]) if rep % 4 else G0.copy()
    for j, gg in enumerate(ME2.GENES):
        if gg[2] and rep % 2: g[j] = float(round(g[j]))
    for j in (IE, IF):
        u = rgn.random()
        g[j] = float(rgn.choice(ORG_VAL)) if u < 0.5 else float(rgn.uniform(LO[j], HI[j]))
    return g


def nace_org(rep, nodo=0):
    g = genoma_org(rep)
    if rgn.random() < 0.2: tabla = None; mem = None
    else:
        sub = [(n, k) for n in range(2) for k in range(4) if rgn.random() < 0.6]
        tabla = [(n, k, (RVd[(n, k)] if rep % 2 else float(rgn.choice([1.0, 0.0, -3.0])))) for n, k in sub]
        mem = [[[float(z) for z in CF['PAT'][LET[k]]], R, n] for n, k, R in tabla]
    s1, s2 = [20092, rep, 1], [20092, rep, 2]
    c = FO.crea(ctx_n(g, np.random.default_rng(s1))); rh = np.random.default_rng(s2)
    c.nace(dict(t=0, k=1, fundador=False, memoria=mem, rng_hijo=rh, padre='x'))
    r1 = np.random.default_rng(s1); r2 = np.random.default_rng(s2)
    st = MO._nace_aislado(g, r1, r2, tabla, sin0=None, nodo=nodo)
    a = dict(Wl=HX(c.Wl), KW=HX(c.KW), act=HX(c.activa), Wps=HX(c.Wps), Wns=HX(c.Wns), nlec=c._nlec, ldiv=c._ldiv,
             rec=c._n10['recibido'], nodo=N(c._nodo), r1=EST(c.rng), r2=EST(rh), org=[int(c.ENSENA), int(c.FILTRA0)])
    b = dict(Wl=HX(st['Wl'][0]), KW=HX(st['KW'][0]), act=HX(st['act'][0]), Wps=HX(st['Wps'][0]), Wns=HX(st['Wns'][0]),
             nlec=int(st['bi'][0, MO.I_NLEC]), ldiv=int(st['bi'][0, MO.I_LDIV]), rec=int(st['bi'][0, MO.I_RECIB]),
             nodo=N(MO._nodo_py(st, 0, NLEE)), r1=EST(r1), r2=EST(r2), org=[int(st['bi'][0, MO.I_ENS]), int(st['bi'][0, MO.I_FIL])])
    return [k for k in a if a[k] != b[k]], (mem is None), bool(c.FILTRA0), float(g[IF]) == 1.0 or float(g[IE]) == 1.0


malos = 0; nnone = 0; nfil = 0; numb = 0
for rep in range(2500):
    d, mn, fi, um = nace_org(rep); malos += int(bool(d)); nnone += int(mn); nfil += int(fi); numb += int(um)
di("nace de FAMB_ORG_ECO (genoma de 20 al azar, memoria None o tabla) == gemelo (Wl, KW, Wps, Wns, nodo, lecturas, lect_div, recibido,"
   " organos expresados y los dos Generators), 2500 casos", malos == 0,
   f"distintos {malos}; memoria None {nnone}; hijo con filtra0 {nfil}; organo en el umbral EXACTO 1.0 {numb}")
for nodo, et in ((1, 'sin leer el nodo'), (2, 'empate al PRIMER indice')):
    malos = 0
    for rep in range(400): malos += int(bool(nace_org(20000 + rep, nodo=nodo)[0]))
    di(f"CONTROL (debe fallar): gemelo {et} != carro", malos > 0, f"distintos {malos}/400")
malos = 0; nnone = 0
for rep in range(2000):
    g = genoma_org(rep); c = FO.crea(ctx_n(g, np.random.default_rng([20093, rep])))
    st = MO._cuerpos_vacios(1, len(ME2.GENES), 0); st['PATM'] = PATM
    tb = [(n, k, float(rgn.choice([1.0, -3.0, 0.0]))) for n in range(2) for k in range(4) if rgn.random() < 0.4]
    c._nodo = [[[float(z) for z in CF['PAT'][LET[k]]], R, n] for n, k, R in tb] * NLEE
    for n, k, R in tb: st['tbH'][0, n, k] = True; st['tbR'][0, n, k] = R
    c._mordh = []
    for q in range(int(rgn.integers(0, 12))):
        n = int(rgn.integers(0, 2)); k = int(rgn.integers(0, 4)); R = RVd[(n, k)]
        c._mordh.append([q, LET[k], n, R]); st['mdH'][0, n, k] = True; st['mdR'][0, n, k] = R
    p0 = c._n10['partos']; ta = c.al_parir(dict(t=0, k=1)); ens = float(g[IE]) >= 1.0
    tg = MO._tabla_padre_py(st, 0) if ens else None
    nnone += int(ta is None)
    malos += int(N(ta) != N(tg) or c._n10['partos'] != p0 + int(ens))
di("al_parir de FAMB_ORG_ECO == gemelo: con 'ensena' la tabla (_tabla_padre) y el parto contado; sin el, None y el parto NO se cuenta; 2000 casos",
   malos == 0, f"distintos {malos}; sin ensena {nnone}")

# ================================================================================================ (I)
seccion('(I) E1: eco=None con FAMB_ORG_ECO (organos apagados: el ctx no trae los genes) y mezclas')
FOT = ('FAMB_ORG_ECO', FO)
CASOS_I = [('9 ORG fija T=5000', s, [FOT] * 9, dict(T=5000)) for s in (20091, 20092, 10001)]
CASOS_I += [('9 ORG inmediata T=3000', 20093, [FOT] * 9, dict(T=3000, reposicion='inmediata')),
            ('mezcla 3 ORG + 3 FAMB_RES0 + 3 FABRICA_ECO', 20094, [FOT] * 3 + [('FAMB_RES0_ECO', FM)] * 3 + [('FABRICA_ECO', FE)] * 3, dict(T=5000)),
            ('1 ORG (n = 1)', 20095, [FOT], dict(T=8000))]
SALIDAS = {}
for et, s, car, kw in CASOS_I:
    res, info, a, tt = compara(s, car, dict(kw, diag=0))
    reporta(f"{et} s{s}", res, info, tt)
    SALIDAS[(et, s)] = a
g_org = MO.run_solapadas(20091, [('FAMB_ORG_ECO', FO)] * 9, T=5000, diag=0)
g_fe = MO.run_solapadas(20091, [('FAMB_ORG_ECO', FE)] * 9, T=5000, diag=0)
fis = lambda r: N([{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']]) + N(r['pista'])
di("eco=None: FAMB_ORG_ECO (organos apagados) == FABRICA_ECO en toda la fisica, en el gemelo (la identidad Python del constructor)",
   fis(g_org) == fis(g_fe))

# ================================================================================================ (E)
seccion('(E) E2: eco=dict con FAMB_ORG_ECO: brazos, organos prendidos/apagados/mezclados/en el umbral, mutacion, esc 30/90/270')
K30 = dict(T=6000, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=500)
K9 = lambda T: dict(T=T, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=500)
K18 = dict(T=6000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500)
K90 = dict(T=3000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000)
K270 = dict(T=1200, diag=0, mundo_n=270, tope_cuerpos=9000, muestra=1000)
G_ON = GEN(ensena=1.2, filtra0=1.2); G_ENS = GEN(ensena=1.2, filtra0=0.9); G_FIL = GEN(ensena=0.9, filtra0=1.2)
G_UMB = GEN(ensena=1.0, filtra0=1.0); G_BAJO = GEN(ensena=0.9999999999999999, filtra0=0.9999999999999999)
MIX9 = [G_ON, G_ENS, G_FIL, list(G0), G_UMB, G_BAJO, GEN(ensena=3.6, filtra0=0.225), GEN(ensena=1.05, filtra0=0.97), G_ON]
MIX18 = MIX9 + MIX9
CASOS_E = [
    ('brazo VIDA esc 30, corte 3000', (20091, 19901), ['FAMB_ORG_ECO'] * 30, K30, CR.eco_cfg('VIDA', 3000)),
    ('brazo AZAR esc 30 (p_mut 0.3), corte 3000', (20092,), ['FAMB_ORG_ECO'] * 30, K30, dict(CR.eco_cfg('AZAR', 3000), p_mut=0.3)),
    ('brazo MUT0 esc 30, corte 3000', (20093,), ['FAMB_ORG_ECO'] * 30, K30, CR.eco_cfg('MUT0', 3000)),
    ('VIDA esc 30 con p_mut 0.3 (los organos se prenden por mutacion)', (20094,), ['FAMB_ORG_ECO'] * 30, K30, dict(CR.eco_cfg('VIDA', 3000), p_mut=0.3)),
    ('organos PRENDIDOS (ensena y filtra0 1.2), sin mutacion', (20095,), ['FAMB_ORG_ECO'] * 9, K9(6000), dict(refunda=1, genoma=G_ON)),
    ('ensena SI y filtra0 NO (la tabla con las neutras)', (20096,), ['FAMB_ORG_ECO'] * 9, K9(6000), dict(refunda=1, genoma=G_ENS)),
    ('ensena NO y filtra0 SI (nadie ensena)', (20097,), ['FAMB_ORG_ECO'] * 9, K9(5000), dict(refunda=1, genoma=G_FIL)),
    ('organos en el umbral EXACTO 1.0 (expresados)', (20098,), ['FAMB_ORG_ECO'] * 9, K9(6000), dict(refunda=1, genoma=G_UMB)),
    ('organos un ulp POR DEBAJO del umbral (apagados)', (20099,), ['FAMB_ORG_ECO'] * 9, K9(5000), dict(refunda=1, genoma=G_BAJO)),
    ('organos MEZCLADOS por linaje, p_mut 0.3, 2 sombras, banco 40', (10002,), ['FAMB_ORG_ECO'] * 9, K9(6000),
     dict(refunda=1, genoma=MIX9, p_mut=0.3, n_sombra=2, banco=40, cada_gen=1000)),
    ('MEZCLADOS esc 18, AZAR (donante azar), p_mut 0.3', (10003,), ['FAMB_ORG_ECO'] * 18, K18,
     dict(CR.eco_cfg('AZAR', 3000), genoma=MIX18, p_mut=0.3)),
    ('(R) refunda=0 con los organos prendidos: si todo muere, muere', (10004,), ['FAMB_ORG_ECO'] * 9, dict(K9(8000), muestra=100),
     dict(refunda=0, genoma=G_ON)),
    ('tope 25 con organos mezclados (bloqueados)', (10005,), ['FAMB_ORG_ECO'] * 18, dict(K18, tope_cuerpos=25),
     dict(refunda=1, genoma=MIX18, p_mut=0.1, n_sombra=2, banco=40, cada_gen=1500)),
    ('DIVIDE con organos prendidos: eta x4, NK 12', (10006,), ['FAMB_ORG_ECO'] * 9, K9(6000), dict(refunda=1, genoma=GEN(eta=0.12, NK=12, ensena=1.2, filtra0=1.2))),
    ('mezcla de cerebros con eco: 6 ORG + 6 FAMB_RES0 + 6 FABRICA_ECO (organos mezclados)', (10007,),
     ['FAMB_ORG_ECO'] * 6 + ['FAMB_RES0_ECO'] * 6 + ['FABRICA_ECO'] * 6, K18, dict(refunda=1, genoma=MIX18, p_mut=0.2, banco=40)),
    ('brazo VIDA esc 90, corte 2000', (19902,), ['FAMB_ORG_ECO'] * 90, K90, CR.eco_cfg('VIDA', 2000)),
    ('brazo AZAR esc 90, corte 2000', (19903,), ['FAMB_ORG_ECO'] * 90, K90, CR.eco_cfg('AZAR', 2000)),
    ('brazo MUT0 esc 90 con organos PRENDIDOS, corte 2000', (19904,), ['FAMB_ORG_ECO'] * 90, K90, dict(CR.eco_cfg('MUT0', 2000), genoma=G_ON)),
    ('brazo VIDA esc 270 (corto), corte 800', (19905,), ['FAMB_ORG_ECO'] * 270, K270, CR.eco_cfg('VIDA', 800)),
]
SAL_E = {}
for et, seeds, car, kw, eco in CASOS_E:
    for s in seeds:
        res, info, a, tt = compara(s, car, kw, eco=eco)
        E_ = a['eco']; SAL_E[(et, s)] = a
        reporta(f"{et} s{s}", res, info, tt, eco=True)
        out(f"        eco: nacidos {E_['n_nac']} · mutaciones {E_['n_mut']} (sombras {E_['n_mut_s']}) · fundadores del banco {E_['n_banco']}"
            f" · refundados {E_['n_refund']} · t_ext {E_['t_ext']} · corte {E_['corte'] and E_['corte']['vivos']} · gen_t {len(E_['gen_t'])}")

# ================================================================================================ (C)
seccion('(C) CHECKPOINT: estado completo (con organos) del original == del gemelo; cortado y reanudado; firmas')
CKS = {}
for et, s, car, kw, eco in (('organos mezclados esc 18, p_mut 0.2, corte 2500, 4 sombras', 19906, ['FAMB_ORG_ECO'] * 18,
                             dict(T=4000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500),
                             dict(refunda=1, t_corte=2500, genoma=MIX18, p_mut=0.2, banco=100, n_sombra=4, cada_gen=500)),
                            ('VIDA esc 90, muestra 1000', 19907, ['FAMB_ORG_ECO'] * 90, dict(T=3000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000),
                             dict(CR.eco_cfg('VIDA', 2000), p_mut=0.2))):
    cko, ckg = {}, {}
    so = ME2.run_solapadas(sem(s), car, eco=dict(eco, ckpt_cada=1000, ckpt_fn=lambda t, b: cko.__setitem__(t, b)), **kw)
    sg = MO.run_solapadas(s, car, eco=dict(eco, ckpt_cada=1000, ckpt_fn=lambda t, b: ckg.__setitem__(t, b)), **kw)
    CKS[s] = (cko, ckg, so)
    di(f"{et} s{s}: seguida con checkpoints, gemelo == original (toda la salida)", N(so) == N(sg), f"checkpoints {sorted(cko)} / {sorted(ckg)}")
    for tt in sorted(cko):
        co = canon_orig(cko[tt]); cg = canon_gem(ckg[tt], kw['muestra'])
        dk = [k for k in co if N(co[k]) != N(cg.get(k))]
        nt = sum(1 for c in co['cuerpos'] if c['cerebro']['familia'].get('n10', {}).get('recibido', -1) > 0)
        ne = sum(1 for c in co['cuerpos'] if c['cerebro']['familia'].get('organos', [0, 0])[0])
        di(f"{et}: ESTADO COMPLETO en t={tt} (cuerpos, cerebros, familia, organos, genomas, mundo, rng, banco, contadores)", not dk,
           f"{len(co['cuerpos'])} cuerpos ({nt} con tabla, {ne} con ensena), {len(co['mundo'])} objetos, banco {len(co['ES']['banco'])}"
           + (f" · DIFIERE {dk}" if dk else ''))
    for tt in sorted(ckg):
        r = MO.run_solapadas(s, car, eco=dict(eco, estado=pickle.loads(pickle.dumps(ckg[tt]))), **kw)
        di(f"{et}: gemelo cortado en t={tt} y reanudado == original seguido (toda la salida)", N(r) == N(so))
cko, ckg, _so = CKS[19906]
ecc = dict(refunda=1, t_corte=2500, genoma=MIX18, p_mut=0.2, banco=100, n_sombra=4, cada_gen=500)
kwc = dict(T=4000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500)
m = aborta(lambda: MO.run_solapadas(19908, ['FAMB_ORG_ECO'] * 18, eco=dict(ecc, estado=ckg[2000]), **kwc))
di("checkpoint del gemelo de OTRA corrida aborta", m is not None and 'firma' in m, str(m))
m = aborta(lambda: MO.run_solapadas(19906, ['FAMB_ORG_ECO'] * 18, eco=dict(ecc, estado=cko[2000]), **kwc))
di("checkpoint del ORIGINAL en el gemelo aborta (formato propio; declarado)", m is not None and 'firma' in m, str(m))
m = aborta(lambda: ME2.run_solapadas(19906, ['FAMB_ORG_ECO'] * 18, eco=dict(ecc, estado=ckg[2000]), **kwc))
di("checkpoint del GEMELO en el original aborta", m is not None and 'firma' in m, str(m))
m = aborta(lambda: MO.run_solapadas(19906, [('FAMB_ORG_ECO', FM)] * 18, eco=dict(ecc, estado=ckg[2000]), **kwc))
di("checkpoint de ORG reanudado con las MISMAS etiquetas y el cerebro FAMB_RES0_ECO aborta", m is not None and 'cerebros distintos' in m, str(m))

# ================================================================================================ (X)
seccion('(X) EL MUNDO DE LA SERIE de v2 con FAMB_ORG_ECO (esc 90: VIDA, AZAR, MUT0; esc 270 corto)')
VEL = {}; SAL_X = {}
for et, s, car, kw, eco in (('esc 90 VIDA, corte 3000', 19908, ['FAMB_ORG_ECO'] * 90, dict(T=4000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000), CR.eco_cfg('VIDA', 3000)),
                            ('esc 90 AZAR, corte 3000', 19909, ['FAMB_ORG_ECO'] * 90, dict(T=4000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000), CR.eco_cfg('AZAR', 3000)),
                            ('esc 90 MUT0, corte 3000', 10008, ['FAMB_ORG_ECO'] * 90, dict(T=4000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000), CR.eco_cfg('MUT0', 3000)),
                            ('esc 270 VIDA, corte 1000', 10009, ['FAMB_ORG_ECO'] * 270, dict(T=1500, diag=0, mundo_n=270, tope_cuerpos=9000, muestra=1000), CR.eco_cfg('VIDA', 1000))):
    t0 = time.time(); a = ME2.run_solapadas(sem(s), car, eco=eco, **kw); ta = time.time() - t0
    MO.run_solapadas(s, car, eco=eco, **dict(kw, T=200))   # caliente
    t0 = time.time(); b = MO.run_solapadas(s, car, eco=eco, **kw); tb = time.time() - t0
    cm = float(np.mean(a['pista']['tam_total'])); VEL[et] = (kw['T'], ta, tb, cm); SAL_X[et] = a
    di(f"{et} s{s} T={kw['T']}: toda la salida", N(a) == N(b),
       f"cuerpos medios {cm:.1f}, max {a['pista']['max_vivos']}, nacidos {a['eco']['n_nac']}, refundados {a['eco']['n_refund']}, vivos en T "
       f"{len(a['eco']['vivos_final'])}; original {ta:.1f} s ({kw['T'] / ta:.0f} pasos/s), gemelo {tb:.2f} s ({kw['T'] / tb:.0f} pasos/s), x{ta / tb:.0f}"
       + ('' if N(a) == N(b) else f" · DIFIERE {claves_distintas(a, b)[:5]}"))

# ================================================================================================ (J)
seccion("(J) JUEZ (refunda=0, genoma=) con motor_eco2 / el gemelo y corre_eco_v2.trabajo con el gemelo (usa_gemelo)")
ME_GEM = types.ModuleType('motor_eco2_gemelo')
ME_GEM.__dict__.update({k: v for k, v in ME2.__dict__.items() if not k.startswith('__')})
ME_GEM.run_solapadas = MO.run_solapadas
JUEZ_PRACTICA = dict(CR.JUEZ, semillas=(20098, 20099))


def con(motor, carro, f, *a):
    viejo = CR.ME; vc = CR.MUNDO['carro']; vj = CR.JUEZ; CR.ME = motor; CR.MUNDO['carro'] = carro; CR.JUEZ = JUEZ_PRACTICA
    try: return f(*a)
    finally: CR.ME = viejo; CR.MUNDO['carro'] = vc; CR.JUEZ = vj


jo = con(ME2, 'FAMB_ORG_ECO', CR.juez, list(G0), (20098, 20099), 10000)
jg = con(ME_GEM, 'FAMB_ORG_ECO', CR.juez, list(G0), (20098, 20099), 10000)
di("juez con FAMB_ORG_ECO: G0 de 20 genes (organos apagados), T_b 10000, 2 semillas de practica", N(jo) == N(jg), str([(d['vive'], d['nac']) for d in jo]))
jo = con(ME2, 'FAMB_ORG_ECO', CR.juez, G_ON, (20098,), 10000)
jg = con(ME_GEM, 'FAMB_ORG_ECO', CR.juez, G_ON, (20098,), 10000)
di("juez con FAMB_ORG_ECO: los organos PRENDIDOS, T_b 10000", N(jo) == N(jg), str([(d['vive'], d['nac']) for d in jo]))
banco = CKS[19906][2]['eco']['corte']['banco']
nb_on = sum(1 for g in banco if g[IE] >= 1.0)
jo = con(ME2, 'FAMB_ORG_ECO', CR.juez, banco, (20098, 20099), 6000)
jg = con(ME_GEM, 'FAMB_ORG_ECO', CR.juez, banco, (20098, 20099), 6000)
di(f"juez con FAMB_ORG_ECO: banco REAL del corte ({len(banco)} genomas de 20, {nb_on} con ensena), 9 al azar por semilla, T_b 6000",
   N(jo) == N(jg), str([(d['vive'], d['nac']) for d in jo]))
import corre_eco_v2 as V2
tmp = tempfile.mkdtemp(prefix='eco_rapido_org_')
try:
    args = lambda d, re: (20097, 'w30', 'VIDA', 12000, 8000, d, re)
    da, db, dc = (os.path.join(tmp, x) for x in 'abc')
    for d in (da, db, dc): os.makedirs(d)
    V2.MOTOR[0] = ME2
    t0 = time.time(); ro = V2.trabajo(args(da, False)); to = time.time() - t0
    MRr = V2.usa_gemelo()
    t0 = time.time(); rg_ = V2.trabajo(args(db, False)); tg = time.time() - t0
    fuera = lambda r: {k: v for k, v in r.items() if k not in ('seg', 'motor')}
    di("corre_eco_v2.trabajo(20097, w30, VIDA, T 12000, corte 8000) con el gemelo (usa_gemelo) == con Python (salvo 'seg' y 'motor')",
       MRr is MO and N(fuera(ro)) == N(fuera(rg_)) and rg_['motor'].startswith('GEMELO'),
       f"persiste {ro['persiste']} vivos_T {ro['vivos_T']} nacidos {ro['n_nac']} banco con ensena {ro['banco_on']}; original {to:.1f} s, gemelo {tg:.1f} s")

    class Corte(Exception): pass

    def corta(*a, **k):
        fn = k['eco']['ckpt_fn']

        def f2(t, blob): fn(t, blob); raise Corte(t)
        k['eco'] = dict(k['eco'], ckpt_fn=f2)
        return MO.run_solapadas(*a, **k)
    V2.MOTOR[0].run_solapadas = corta
    try: V2.trabajo(args(dc, False)); cortado = None
    except Corte as e: cortado = e.args[0]
    finally: V2.MOTOR[0].run_solapadas = MO.run_solapadas
    rr = V2.trabajo(args(dc, True))
    di("corre_eco_v2.trabajo con el gemelo cortado ('corte de luz' tras el checkpoint) y reanudado == Python seguido",
       cortado == 10000 and N(fuera(rr)) == N(fuera(ro)), f"cortado en t={cortado}")
finally:
    V2.MOTOR[0] = ME2
    shutil.rmtree(tmp)
di("el MUNDO y el JUEZ de corre_eco quedan como estaban y el motor de corre_eco_v2 vuelve a Python",
   CR.MUNDO['carro'] == 'FABRICA_ECO' and CR.JUEZ['semillas'] == tuple(range(19201, 19221)) and V2.MOTOR[0] is ME2)

# ================================================================================================ (L)
seccion('(L) LARGO: eco VIDA esc 9 con mutacion fuerte (los organos se prenden y apagan), T 30 000')
res, info, a, tt = compara(19909, ['FAMB_ORG_ECO'] * 9, dict(T=30000, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=1000),
                           eco=dict(CR.eco_cfg('VIDA', 20000), p_mut=0.4, genoma=MIX9))
reporta("eco VIDA esc 9 p_mut 0.4, organos mezclados, T=30000, corte 20000 s19909", res, info, tt, eco=True)

# ================================================================================================ (R)
seccion('(R) REGRESION con 20 genes (FABRICA_ECO, FAMB_RES0_ECO contra motor_eco2) y eco=None: gemelo de organos == gemelo de la familia')
for et, s, car, kw, eco in (('eco VIDA esc 18 FABRICA_ECO, corte 3000', 10010, ['FABRICA_ECO'] * 18, K18, CR.eco_cfg('VIDA', 3000)),
                            ('eco VIDA esc 18 FAMB_RES0_ECO, corte 3000', 10011, ['FAMB_RES0_ECO'] * 18, K18, CR.eco_cfg('VIDA', 3000)),
                            ('9 FABRICA eco=None T=3000', 10001, ['FABRICA'] * 9, dict(T=3000, diag=0), None)):
    res, info, a, tt = compara(s, car, kw, eco=eco)
    reporta(f"{et} s{s}", res, info, tt, eco=eco is not None)
import motor_eco_rapido_fam as MF
for et, s, car, T in (('9 FAMB_RES0_ECO eco=None T=40000', 10002, [('FAMB_RES0_ECO', FM)] * 9, 40000),
                      ('9 FABRICA_ECO eco=None T=40000', 10003, [('FABRICA_ECO', FE)] * 9, 40000)):
    v = MF.run_solapadas(sem(s), car, T=T, diag=0); w = MO.run_solapadas(s, car, T=T, diag=0)
    di(f"{et} s{s}: gemelo de organos == gemelo de la familia (132/132) en toda la salida", N(v) == N(w),
       f"partos {sum(l['descendientes'] for l in v['linajes'])}")

# ================================================================================================ (K)
seccion('(K) CONTROLES que DEBEN fallar (si nada cambia, nada controla: ERR-38)')
base = SAL_E[('organos MEZCLADOS por linaje, p_mut 0.3, 2 sombras, banco 40', 10002)]
g = MO.run_solapadas(10003, ['FAMB_ORG_ECO'] * 9, eco=dict(refunda=1, genoma=MIX9, p_mut=0.3, n_sombra=2, banco=40, cada_gen=1000), **K9(6000))
di("gemelo con la semilla vecina != original", N(g) != N(base))


def gemelo_como(G, modo):
    fg = []; trn = []
    eg = None if G['eco'] is None else dict(G['eco'])
    if G['filas']: eg['ind_cb'] = lambda li, row, g: fg.append((li, list(row), HX(g)))
    b = MO.run_solapadas(G['seed'], G['carros'], eco=eg, _modo=modo, _traza_nac=trn, **G['kw'])
    return N(b) != G['a'], N(fg) != G['fo'], N(trn) != G['nac']


out(f"  barrido de los controles sobre {len(GUARDA)} corridas guardadas del original ((I), (E), (L), (R))")
for et, modo, clave, qu in (("con los organos SIEMPRE expresados", dict(org=1), 'p_on',
                             "con un parto de un padre SIN 'ensena' o un hijo SIN 'filtra0' que recibio neutras"),
                            ("con 'filtra0' leido del PADRE (no del hijo)", dict(org=2), 'p_padre',
                             "con un parto con neutras donde el 'filtra0' del padre y el del hijo no coinciden"),
                            ("que NO lee el nodo", dict(nodo=1), 'p_lee', 'con alguna tabla no vacia'),
                            ("con el empate de la lectura al PRIMER indice", dict(nodo=2), 'p_una', 'con alguna tabla de UNA entrada')):
    pred = [G for G in GUARDA if G[clave] > 0]; resto = [G for G in GUARDA if G[clave] == 0]
    dp = [gemelo_como(G, modo) for G in pred]; dr = [gemelo_como(G, modo) for G in resto]
    npf = sum(1 for x in dp if any(x)); nrf = sum(1 for x in dr if any(x)); nfis = sum(1 for x in dp + dr if x[0] or x[1])
    di(f"CONTROL (debe fallar): gemelo {et} != original en TODA corrida {qu}", len(pred) > 0 and npf == len(pred),
       f"distintas {npf}/{len(pred)} (en nacimientos {sum(1 for x in dp if x[2])}); en las otras {len(resto)}: distintas {nrf}; "
       f"con la FISICA (salida o filas) distinta: {nfis}/{len(GUARDA)}")
for et, modo in (("gemelo con exp de libm (sin el bucle de NumPy)", dict(exp=1)), ("gemelo con suma ingenua (sin BLAS)", dict(dot=1)),
                 ("gemelo con turno fijo (mismo consumo de azar)", dict(turno=1))):
    res, info, a, tt = compara(10002, ['FAMB_ORG_ECO'] * 9, K9(6000), eco=dict(refunda=1, genoma=MIX9, p_mut=0.3, n_sombra=2, banco=40, cada_gen=1000), modo=modo)
    di(f"{et} != original (trayectoria o pesos)", not (res['traza'] and res['cerebros']),
       f"salida {'=' if res['salida'] else '!='} · traza {'=' if res['traza'] else '!='} · cerebros {'=' if res['cerebros'] else '!='}")
e1 = MO.run_solapadas(20091, ['FAMB_ORG_ECO'] * 30, eco=CR.eco_cfg('VIDA', 3000), **K30)
e2 = MO.run_solapadas(20091, ['FAMB_ORG_ECO'] * 30, eco=CR.eco_cfg('MUT0', 3000), **K30)
di("brazo VIDA != MUT0 (misma semilla, ORG)", N(e1) != N(e2), f"mutaciones {e1['eco']['n_mut']} / {e2['eco']['n_mut']}")
on = MO.run_solapadas(20095, ['FAMB_ORG_ECO'] * 9, eco=dict(refunda=1, genoma=G_ON), **K9(6000))
off = MO.run_solapadas(20095, ['FAMB_ORG_ECO'] * 9, eco=dict(refunda=1), **K9(6000))
di("organos prendidos != apagados (misma semilla): el organo cambia la fisica", fis(on) != fis(off),
   f"partos {sum(l['descendientes'] for l in on['linajes'])} / {sum(l['descendientes'] for l in off['linajes'])}")

# ================================================================================================ (G)
seccion('(G) GUARDIAS: las del original con el mismo mensaje; las del gemelo (lo que no compila aborta)')
for et, kw in (("genoma de 18 genes (el de motor_eco) con motor_eco2", dict(seed=1, carros=['FAMB_ORG_ECO'] * 3, T=10, diag=0, eco=dict(genoma=list(G0[:18])))),
               ("organo fuera de rango (ensena 3.7 > 3.6)", dict(seed=1, carros=['FAMB_ORG_ECO'] * 3, T=10, diag=0, eco=dict(genoma=list(G0[:18]) + [3.7, 0.9]))),
               ("'FAMB_ORG_ECO' como texto con eco=None (no es carro de la carrera)", dict(seed=1, carros=['FAMB_ORG_ECO'], T=10, diag=0)),
               ("clave eco desconocida", dict(seed=1, carros=['FAMB_ORG_ECO'], T=10, diag=0, eco=dict(refnda=0))),
               ("t_corte sin vivero", dict(seed=1, carros=['FAMB_ORG_ECO'], T=10, diag=0, eco=dict(refunda=0, t_corte=5))),
               ("401 linajes con eco", dict(seed=1, carros=['FAMB_ORG_ECO'] * 401, T=10, diag=0, eco=dict(refunda=1))),
               ("mundo_n fuera de rango con eco", dict(seed=1, carros=['FAMB_ORG_ECO'], T=10, diag=0, mundo_n=2001, eco=dict(refunda=1))),
               ("diag=1", dict(seed=1, carros=[FOT], T=10))):
    mo = aborta(lambda: ME2.run_solapadas(**kw)); mg = aborta(lambda: MO.run_solapadas(**kw))
    di(f"{et}: aborta igual que el original", mo is not None and mo == mg, str(mg)[:110])
for et, kw in (("carro APR_ECO con eco", dict(seed=1, carros=['APR_ECO'] * 3, T=10, diag=0, eco=dict(refunda=1))),
               ("T = 3", dict(seed=1, carros=[FOT] * 3, T=3, diag=0))):
    mg = aborta(lambda: MO.run_solapadas(**kw))
    di(f"{et}: el gemelo aborta (fuera de alcance)", mg is not None and mg.startswith('ValueError'), str(mg)[:120])

# ================================================================================================ (D)
seccion('(D) DETERMINISMO')
e1b = MO.run_solapadas(20091, ['FAMB_ORG_ECO'] * 30, eco=CR.eco_cfg('VIDA', 3000), **K30)
di("dos llamadas iguales del gemelo (ORG, eco VIDA con mutacion) dan la misma salida", N(e1) == N(e1b))

# ================================================================================================ (Z)
seccion('(Z) CACHE: un proceso NUEVO carga la cache de numba y reproduce corridas del original')
tmp = tempfile.mkdtemp(prefix='eco_rapido_org_cache_')
try:
    ref = os.path.join(tmp, 'ref.json')
    refs = {'I': SALIDAS[('9 ORG fija T=5000', 20091)], 'X90': SAL_X['esc 90 VIDA, corte 3000'], 'X270': SAL_X['esc 270 VIDA, corte 1000']}
    json.dump(dict(refs={k: N(v) for k, v in refs.items()}, e90=CR.eco_cfg('VIDA', 3000), e270=CR.eco_cfg('VIDA', 1000)), open(ref, 'w'))
    hijo = r'''
import json, sys, time, os
t0 = time.time()
sys.path[:0] = [sys.argv[2], os.path.join(os.path.dirname(os.path.dirname(sys.argv[2])), 'experimentos', 'generaciones')]
import motor_eco_rapido_org as MO
import motor_eco2 as ME2
from numba.core.registry import CPUDispatcher
t1 = time.time()
R = json.load(open(sys.argv[1])); N = lambda x: json.dumps(x, default=str, sort_keys=True)
FO = ME2.carga_eco('FAMB_ORG_ECO')
ok = []; tiempos = []
for tipo in ('I', 'X90', 'X270'):
    t2 = time.time()
    if tipo == 'I': r = MO.run_solapadas(20091, [('FAMB_ORG_ECO', FO)] * 9, T=5000, diag=0)
    elif tipo == 'X90': r = MO.run_solapadas(19908, ['FAMB_ORG_ECO'] * 90, T=4000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000, eco=R['e90'])
    else: r = MO.run_solapadas(10009, ['FAMB_ORG_ECO'] * 270, T=1500, diag=0, mundo_n=270, tope_cuerpos=9000, muestra=1000, eco=R['e270'])
    tiempos.append(round(time.time() - t2, 2)); ok.append(N(r) == R['refs'][tipo])
hits = miss = 0
for nom in dir(MO):
    f = getattr(MO, nom)
    if isinstance(f, CPUDispatcher):
        hits += sum(f.stats.cache_hits.values()); miss += sum(f.stats.cache_misses.values())
print(json.dumps(dict(ok=ok, import_s=round(t1 - t0, 2), tiempos=tiempos, hits=hits, miss=miss)))
'''
    p = subprocess.run([sys.executable, '-c', hijo, ref, AQUI], capture_output=True, text=True, timeout=1800)
    try: z = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception: z = dict(ok=[False], hits=0, miss=-1, import_s=None, tiempos=None, err=p.stderr[-600:])
    di("proceso NUEVO: lee la cache (0 compilaciones) y reproduce 3 corridas del original bit a bit (ORG eco=None; ORG VIDA esc 90; ORG VIDA esc 270)",
       all(z['ok']) and len(z['ok']) == 3 and z['miss'] == 0 and z['hits'] > 0,
       f"identicas {z['ok']}; funciones cargadas de la cache {z['hits']}, compiladas {z['miss']}; import {z['import_s']} s; "
       f"corridas {z['tiempos']} s" + (f" · {z.get('err')}" if z.get('err') else ''))
finally:
    shutil.rmtree(tmp)

# ================================================================================================ (V)
seccion('(V) ACELERACION (mismo mundo, mismo proceso; la maquina corre otros procesos: tiempos con carga)')
for et, (T, ta, tb, cm) in VEL.items():
    out(f"  {et} con FAMB_ORG_ECO: T={T}, {cm:.1f} cuerpos de media · original {T / ta:.0f} pasos/s "
        f"({ta / T / cm * 1e6:.1f} us por cuerpo y paso) · gemelo {T / tb:.0f} pasos/s ({tb / T / cm * 1e6:.2f} us por cuerpo y paso) · x{ta / tb:.0f}")
out(f"tiempo {round(time.time() - T00)} s")
out(f"RESULTADO: {OK[0]}/{OK[1]}")
SAL.close()
